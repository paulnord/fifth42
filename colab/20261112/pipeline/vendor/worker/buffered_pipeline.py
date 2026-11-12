"""Isolated experiments: retain checked immutable bytes and buffer durable writes.

Scientific certificates, native packets, coverage units and candidate checks are
unchanged. Only the committed journal state is durable; pending records are not.
"""
from dataclasses import dataclass,fields
import hashlib
import json
import os
from pathlib import Path
import queue
import sys
import threading
import time
import weakref

ROOT=Path(__file__).resolve().parent
WORKER=ROOT if (ROOT/'source/lattice_gpu').is_dir() else ROOT/'worker'
sys.path[:0]=[str(WORKER),str(WORKER/'source/lattice_gpu')]
import coordinator_pipeline as pipeline
import overnight_search as night
import packing_opt
import scaling_core as core
import width_coverage as coverage

FIELDS=tuple(field.name for field in fields(core.Task))
_SEALS={}
_SEAL_LOCK=threading.Lock()


def require(ok,message):
    if not ok:raise ValueError(message)


def immutable(value):
    if type(value) in (int,str):return
    require(type(value) is tuple,'Cached task contains mutable or unsupported fields')
    for item in value:immutable(item)


@dataclass(frozen=True)
class Seal:
    reference:object
    tasks:tuple
    snapshots:tuple
    payloads:tuple
    specifications:tuple
    spans:tuple
    window:tuple
    geometry:str
    certificate:str


def cache_size():
    with _SEAL_LOCK:return len(_SEALS)


def register(chunk,tasks,snapshots,payloads):
    key=id(chunk)
    def release(reference):
        with _SEAL_LOCK:
            old=_SEALS.get(key)
            if old is not None and old.reference is reference:_SEALS.pop(key)
    reference=weakref.ref(chunk,release)
    seal=Seal(reference,tuple(tasks),tuple(snapshots),tuple(payloads),
              chunk.window.explicit_specs,chunk.window.spans,tuple(chunk.window.identity().items()),
              chunk.geometry_sha256,chunk.plan.certificate_sha256)
    with _SEAL_LOCK:_SEALS[key]=seal


def prepare_cached(pool,window,group_limit):
    require(window.width==8 and group_limit in (1,2,4,8,16),'Unsupported grouping')
    args=[(window.lo,window.hi,first,min(first+group_limit,window.last),window.bits,window.cap,window.geometry_policy)
          for first in range(window.first,window.last,group_limit)]
    rows=[row for part in pool.map(coverage.prepare_segment,args,8) for row in part]
    specs=tuple(row[5] for row in rows);tasks=[row[0] for row in rows];tokens=[row[1] for row in rows]
    spans=tuple((row[3],row[4]) for row in rows)
    view=coverage.Window(window.lo,window.hi,window.first,window.last,8,window.bits,window.cap,window.geometry_policy,group_limit,specs,spans)
    core.checked_tasks(specs,tasks)
    require(len(tokens)==len(tasks) and all(len(token)==64 for token in tokens),'Missing exact certificates')
    geometry=hashlib.sha256();payload_bytes=0;payloads=[];snapshots=[]
    for task,token in zip(tasks,tokens):
        require(type(task) is core.Task,'Unexpected task type')
        payload=packing_opt.task_payload(task)
        require(hashlib.sha256(payload).hexdigest()==token,'Canonical task differs from exact certificate')
        snapshot=tuple(getattr(task,name) for name in FIELDS);immutable(snapshot)
        payloads.append(payload);snapshots.append(snapshot)
        geometry.update(payload);geometry.update(b'\n');payload_bytes+=len(payload)+1
    total=sum(t.points for t in tasks)
    # Coefficient positions are enumeration work, not resident arrays. Bound
    # the prepared objects by the original integer cells and verify their exact
    # partition; native task/packet limits remain independently enforced.
    require(0<len(tasks)<=window.last-window.first,'Invalid physical task count')
    cursor=window.first
    for left,right in spans:
        require(left==cursor and left<right<=window.last,'Invalid physical partition')
        cursor=right
    require(cursor==window.last,'Incomplete physical partition')
    groups=[];pending=[];points=0
    for task in tasks:
        require(task.points<=core.MAX_POINTS,'Task cannot fit native packet')
        if pending and (len(pending)==core.MAX_TASKS or points+task.points>core.MAX_POINTS):
            groups.append(core.encode_batch(pending,window.cap));pending=[];points=0
        pending.append(task);points+=task.points
    if pending:groups.append(core.encode_batch(pending,window.cap))
    certificate=hashlib.sha256(('\n'.join(tokens)+'\n').encode()).hexdigest()
    plan=core.VerifiedPlan(window.hi,window.cap,tuple(groups),(),len(tasks),total,certificate)
    payload_bytes+=sum(len(batch.packet.encode()) for batch in groups)
    chunk=pipeline.PreparedChunk(view,plan,tuple((task.id,token,task.points) for task,token in zip(tasks,tokens)),
                                 geometry.hexdigest(),payload_bytes,{},tuple(row[2] for row in rows))
    register(chunk,tasks,snapshots,payloads)
    return chunk


def validate_cached(chunk):
    with _SEAL_LOCK:seal=_SEALS.get(id(chunk))
    require(seal is not None and seal.reference() is chunk,'Plan has no in-process checked-data seal')
    require(tuple(chunk.window.identity().items())==seal.window and chunk.window.explicit_specs==seal.specifications and
            chunk.window.spans==seal.spans,'Cached logical/physical window changed')
    tasks=tuple(task for batch in chunk.plan.batches for task in batch.tasks)
    require(len(tasks)==len(seal.tasks),'Cached physical task count changed')
    core.checked_tasks(chunk.window.specifications(),tasks)
    for task,original,snapshot in zip(tasks,seal.tasks,seal.snapshots):
        require(task is original and tuple(getattr(task,name) for name in FIELDS)==snapshot,'Task changed after canonical validation')
    expected=tuple((task.id,hashlib.sha256(payload).hexdigest(),task.points) for task,payload in zip(tasks,seal.payloads))
    require(expected==chunk.patches and chunk.plan.tasks==len(tasks),'Cached certificates do not match task manifest')
    require(chunk.plan.points==sum(task.points for task in tasks),'Cached total point count changed')
    for batch in chunk.plan.batches:
        require(core.encode_batch(batch.tasks,chunk.window.cap)==batch,'Native packet differs from exact tasks')
    require(not chunk.plan.direct_hits,'Unmanifested direct work')
    require(chunk.geometry_sha256==seal.geometry and chunk.plan.certificate_sha256==seal.certificate,'Cached plan digests changed')


def encode_record_once(previous,record):
    payload=dict(record,previous_sha256=previous)
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    digest=hashlib.sha256(raw).hexdigest()
    # Field order of the outer JSON line is immaterial. Its hashed payload stays
    # byte-identical to the original canonical encoding after sha256 is removed.
    return raw[:-1]+b',"sha256":"'+digest.encode()+b'"}\n',digest


def advance(state,record,digest,offset):
    return dict(state,next_patch=record['window']['last'],chunks=state['chunks']+1,
                points=state['points']+record['points'],
                patches=state['patches']+record['window']['last']-record['window']['first'],
                physical_tasks=state.get('physical_tasks',0)+len(record['patches']),
                hits=sorted(set(map(tuple,state['hits']))|set(map(tuple,record['hits']))),
                journal_offset=offset,journal_sha256=digest)


class BufferedJournal(coverage.TrialJournal):
    """One owner, bounded pending records; checkpoint advances only after fsync."""
    def __init__(self,directory,identity,window,*,records=8,max_bytes=8*1024**2,max_age=.25,single_encode=True):
        super().__init__(directory,identity,window)
        require(type(records) is int and 1<=records<=64 and 0<max_bytes<=16*1024**2 and 0<max_age<=1,'Invalid buffer bounds')
        self.max_records,self.max_bytes,self.max_age=records,max_bytes,max_age
        self.encoder=encode_record_once if single_encode else night.encode_record
        self.pending=[];self.pending_bytes=0;self.head=dict(self.state);self.pending_since=None
        self.flush_count=0;self.flush_seconds=0.;self.peak_pending_records=0;self.peak_pending_bytes=0

    def commit(self,record):
        if self.lock.closed:raise RuntimeError('Journal is closed')
        if self.poisoned:raise RuntimeError('Failed durable write: explicit recovery required')
        if threading.get_ident()!=self.owner:raise RuntimeError('Only journal owner may accept records')
        self._validate(record,self.head['next_patch'])
        raw,digest=self.encoder(self.head['journal_sha256'],dict(record,sequence=self.head['chunks']+1))
        require(len(raw)<=self.max_bytes,'One record exceeds buffer budget')
        if self.pending_bytes+len(raw)>self.max_bytes:self.flush()
        if not self.pending:self.pending_since=time.monotonic()
        self.pending.append(raw);self.pending_bytes+=len(raw)
        self.head=advance(self.head,record,digest,self.head['journal_offset']+len(raw))
        self.peak_pending_records=max(self.peak_pending_records,len(self.pending))
        self.peak_pending_bytes=max(self.peak_pending_bytes,self.pending_bytes)
        if len(self.pending)>=self.max_records or time.monotonic()-self.pending_since>=self.max_age:self.flush()

    def flush(self):
        if not self.pending:return
        if self.poisoned:raise RuntimeError('Uncertain durable state; explicit recovery required')
        if threading.get_ident()!=self.owner:raise RuntimeError('Only journal owner may flush')
        began=time.monotonic()
        try:
            with self.journal.open('ab') as stream:
                stream.write(b''.join(self.pending));stream.flush();os.fsync(stream.fileno());offset=stream.tell()
            require(offset==self.head['journal_offset'],'Buffered journal offset mismatch')
            night.atomic_json(self.checkpoint,self.head)
        except BaseException:
            self.poisoned=True;raise
        self.state=dict(self.head);self.pending=[];self.pending_bytes=0;self.pending_since=None
        self.flush_count+=1;self.flush_seconds+=time.monotonic()-began

    def close(self):
        try:
            if not self.lock.closed and not self.poisoned:self.flush()
        finally:self.lock.close()


class AsyncJournal:
    """A bounded queue feeds one journal-owning thread; only its state is durable."""
    def __init__(self,directory,identity,window,*,records=8,queue_records=8):
        require(1<=queue_records<=16,'Invalid writer queue bound')
        self.directory,self.identity,self.window=directory,identity,window
        self.records=records;self.queue=queue.Queue(queue_records);self.ready=threading.Event()
        self.error=None;self.state=None;self.journal=None;self.closed=False
        self.peak_queued_records=0;self.max_item_bytes=2*1024**2
        self.thread=threading.Thread(target=self.run,name='buffered-journal-owner',daemon=True)
        self.thread.start()
        if not self.ready.wait(10):raise TimeoutError('Journal owner did not start')
        self.check()

    def check(self):
        if self.error:raise RuntimeError('Asynchronous journal failed') from self.error

    def run(self):
        journal=None
        try:
            journal=BufferedJournal(self.directory,self.identity,self.window,records=self.records)
            self.journal=journal;self.state=dict(journal.state);self.ready.set()
            while True:
                try:item=self.queue.get(timeout=.05)
                except queue.Empty:
                    if journal.pending_since is not None and time.monotonic()-journal.pending_since>=journal.max_age:
                        journal.flush();self.state=dict(journal.state)
                    continue
                if item is None:break
                journal.commit(json.loads(item));self.state=dict(journal.state)
            journal.close();self.state=dict(journal.state)
        except BaseException as exc:self.error=exc;self.ready.set()
        finally:
            if journal and not journal.lock.closed:
                try:journal.close();self.state=dict(journal.state)
                except BaseException as exc:self.error=exc

    def put(self,item):
        while True:
            self.check()
            try:self.queue.put(item,timeout=.05);break
            except queue.Full:continue
        self.peak_queued_records=max(self.peak_queued_records,self.queue.qsize())

    def commit(self,record):
        if self.closed:raise RuntimeError('Journal is closed')
        self.check()
        raw=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
        require(len(raw)<=self.max_item_bytes,'Asynchronous record exceeds immutable queue budget')
        self.put(raw)

    def close(self):
        if self.closed:return
        self.closed=True
        try:self.put(None)
        finally:
            self.thread.join(20)
            if self.thread.is_alive():raise TimeoutError('Journal owner did not drain')
            self.check()


class MemoryJournal:
    """Volatile upper-bound experiment. This provides NO durable coverage."""
    def __init__(self,identity,window,max_bytes=16*1024**2):
        self.validator=object.__new__(coverage.TrialJournal)
        self.validator.identity,self.validator.window=identity,window
        self.state=dict(identity=identity,window=window.identity(),next_patch=window.first,chunks=0,
                        points=0,patches=0,hits=[],journal_offset=0,journal_sha256='0'*64,
                        completed_bound=None,coverage_schema=coverage.SCHEMA,physical_tasks=0)
        self.data=bytearray();self.max_bytes=max_bytes
    def commit(self,record):
        self.validator._validate(record,self.state['next_patch'])
        raw,digest=encode_record_once(self.state['journal_sha256'],dict(record,sequence=self.state['chunks']+1))
        require(len(self.data)+len(raw)<=self.max_bytes,'Volatile journal exceeds RAM budget')
        self.data.extend(raw);self.state=advance(self.state,record,digest,len(self.data))
    def close(self):pass
