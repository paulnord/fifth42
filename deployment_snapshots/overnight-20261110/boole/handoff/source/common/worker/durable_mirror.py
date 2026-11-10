"""Copy only committed journal prefixes; publish a checkpoint after readback.

The local journal is authoritative. An interrupted copy can leave extra bytes
on the replica, but never advances its checkpoint past verified durable bytes.
This module never truncates the source or acquires a search ownership lock.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import threading
import time


def atomic(path, value):
    path=Path(path);raw=json.dumps(value,sort_keys=True,indent=2).encode()+b'\n'
    temporary=path.with_name(path.name+f'.{os.getpid()}.{threading.get_ident()}.tmp')
    with temporary.open('wb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
    os.replace(temporary,path)
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)


def require(ok,message):
    if not ok:raise RuntimeError(message)


class PrefixMirror:
    def __init__(self,source,destination,identity):
        self.source,self.destination=Path(source),Path(destination)
        self.identity=identity
        require(self.source.resolve()!=self.destination.resolve(),'Replica equals source')
        self.destination.mkdir(mode=0o700,parents=True,exist_ok=True)
        parent_fd=os.open(self.destination.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(parent_fd)
        finally:os.close(parent_fd)
        self.lock=(self.destination/'replica.lock').open('a+')
        try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BaseException:self.lock.close();raise
        self.offset=0;self.hasher=hashlib.sha256();self.published=None
        cp=self.destination/'checkpoint.json'
        if cp.exists():
            state=json.loads(cp.read_bytes())
            require(state['identity']==identity,'Replica belongs to another run')
            self.offset=state['journal_offset']
            local=json.loads((self.source/'checkpoint.json').read_bytes())
            require(local['identity']==identity and local['journal_offset']>=self.offset,'Replica is ahead of its local authority')
            with (self.destination/'coverage.jsonl').open('rb') as stream,(self.source/'coverage.jsonl').open('rb') as source:
                left=self.offset
                while left:
                    data=stream.read(min(left,4*1024**2));require(data,'Replica prefix truncated')
                    require(source.read(len(data))==data,'Replica committed prefix differs from source')
                    self.hasher.update(data);left-=len(data)
            # A crash between checkpoint and receipt publication is recoverable:
            # the source comparison above verifies the whole published prefix.
            self.published=state

    def close(self):self.lock.close()

    def sync(self):
        captured_epoch=time.time()
        cp_path=self.source/'checkpoint.json'
        if not cp_path.exists():return None
        raw=cp_path.read_bytes();cp=json.loads(raw)
        require(cp['identity']==self.identity,'Local checkpoint identity changed')
        target=cp['journal_offset']
        require(type(target) is int and target>=self.offset,'Local committed prefix regressed')
        journal=self.destination/'coverage.jsonl'
        if not journal.exists():journal.touch(mode=0o600)
        require(journal.stat().st_size<=target,'Replica has bytes beyond the captured local prefix')
        # Re-read any unpublished tail left by a failed earlier copy. Validate it
        # against the immutable local prefix before publishing a checkpoint.
        staged=self.hasher.copy()
        with (self.source/'coverage.jsonl').open('rb') as source,journal.open('r+b') as replica:
            source.seek(self.offset);replica.seek(self.offset);left=target-self.offset
            while left:
                data=source.read(min(left,4*1024**2));require(data,'Local committed prefix truncated')
                existing=replica.read(len(data))
                require(existing==data[:len(existing)],'Unpublished replica tail differs from source')
                replica.seek(-len(existing),os.SEEK_CUR);replica.write(data)
                staged.update(data);left-=len(data)
            replica.flush();os.fsync(replica.fileno())
            source.seek(self.offset);replica.seek(self.offset);left=target-self.offset
            while left:
                size=min(left,4*1024**2)
                expected=source.read(size);actual=replica.read(size)
                require(len(expected)==size and actual==expected,'Replica readback mismatch')
                left-=size
        # Independent GMP evidence is copied before its matching checkpoint.
        audit_dir=self.source/'independent-audits'
        if audit_dir.exists():
            dest=self.destination/'independent-audits';dest.mkdir(mode=0o700,exist_ok=True)
            for path in sorted(audit_dir.glob('*.json')):
                if int(path.name.split('-')[0])<=cp['chunks']:
                    other=dest/path.name
                    if not other.exists():atomic(other,json.loads(path.read_bytes()))
                    require(json.loads(other.read_bytes())==json.loads(path.read_bytes()),'Independent audit replica mismatch')
        for name in ('controls.json','worker-affinities.json','run-config.json','run-manifest.json','status.json'):
            path=self.source/name
            if path.exists():atomic(self.destination/name,json.loads(path.read_bytes()))
        receipt=dict(status='verified',synced_epoch=time.time(),captured_epoch=captured_epoch,identity=self.identity,
                     committed_bytes=target,next_patch=cp['next_patch'],chunks=cp['chunks'],
                     journal_sha256=cp['journal_sha256'],raw_sha256=staged.hexdigest(),
                     checkpoint_sha256=hashlib.sha256(raw).hexdigest(),
                     method='append, fsync, byte readback, audit copies, checkpoint, receipt')
        # Preserve the exact captured checkpoint bytes, including formatting.
        temporary=self.destination/'checkpoint.copy.tmp'
        with temporary.open('wb') as stream:
            stream.write(raw);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,self.destination/'checkpoint.json')
        fd=os.open(self.destination,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        atomic(self.destination/'replica-state.json',receipt)
        self.offset=target;self.hasher=staged;self.published=cp
        return receipt


class Replicator:
    def __init__(self,source,destination,identity,interval=60):
        self.source=Path(source);self.destination=destination;self.identity=identity
        self.interval=interval;self.stop=threading.Event();self.wake=threading.Event()
        self.started=time.time();self.last_success=self.started;self.receipt=None;self.error=None
        self.thread=threading.Thread(target=self.run,daemon=True,name='committed-prefix-replica')

    def start(self):self.thread.start()
    def nudge(self):self.wake.set()
    def run(self):
        mirror=None
        try:
            while True:
                try:
                    if mirror is None:mirror=PrefixMirror(self.source,self.destination,self.identity)
                    receipt=mirror.sync()
                    if receipt:self.receipt=receipt;self.last_success=receipt['captured_epoch']
                    if self.stop.is_set():
                        receipt=mirror.sync()
                        if receipt:self.receipt=receipt;self.last_success=receipt['captured_epoch']
                    self.error=None
                except Exception as exc:self.error=f'{type(exc).__name__}: {exc}'
                atomic(self.source/'replication-health.json',dict(last_success_epoch=self.last_success,
                       updated_epoch=time.time(),receipt=self.receipt,error=self.error))
                if self.stop.is_set():break
                self.wake.wait(5 if self.error else self.interval);self.wake.clear()
        finally:
            if mirror:mirror.close()

    def finish(self,timeout=3):
        self.stop.set();self.wake.set();self.thread.join(timeout)
        return not self.thread.is_alive() and self.error is None
