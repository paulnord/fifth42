"""Encode canonical task data once in its certifying worker, then retain bytes.

Workers run the original exact certification. The parent hashes the returned
canonical bytes and reconstructs immutable Tasks directly from those bytes;
there is no second decimal re-encoding of large rational matrix integers.
"""
import hashlib,json,time
import buffered_pipeline as buffering
from buffered_pipeline import core,coverage,pipeline,packing_opt
import runtime_initialize
_CAPTURE=None

def capture_digest(task):
    global _CAPTURE
    payload=packing_opt.task_payload(task);digest=hashlib.sha256(payload).hexdigest()
    _CAPTURE=(task,payload,digest)
    return digest

def initialize(source,cpus=()):
    runtime_initialize.initialize(source,cpus)
    core.task_digest=capture_digest

def prepare_segment(args):
    global _CAPTURE
    lo,hi,first,last,bits,cap,geometry=args
    spec=coverage.specification(lo,hi,first,last,bits,cap,geometry)
    _CAPTURE=None
    try:task,token,timing=pipeline.prepare_certified(spec)
    except pipeline.GuardedPatch:
        if last-first==1:raise
        middle=first+(last-first)//2
        return prepare_segment((lo,hi,first,middle,bits,cap,geometry))+prepare_segment((lo,hi,middle,last,bits,cap,geometry))
    capture=_CAPTURE;_CAPTURE=None
    buffering.require(capture is not None and capture[0] is task and capture[2]==token,'Exact certifier did not capture canonical task bytes')
    return [(capture[1],token,timing,first,last,spec)]

def no_float(value):raise ValueError('Task payload contains noninteger numeric values')
def unique_object(pairs):
    result={}
    for key,value in pairs:
        buffering.require(key not in result,'Duplicate task field');result[key]=value
    return result

def tuples(value):
    if type(value) is list:return tuple(tuples(item) for item in value)
    buffering.require(type(value) in (int,str),'Task contains unsupported data types')
    return value

def decode(payload,certificate):
    buffering.require(type(payload) is bytes and hashlib.sha256(payload).hexdigest()==certificate,'Canonical worker bytes do not match exact certificate')
    data=json.loads(payload,parse_float=no_float,parse_constant=no_float,object_pairs_hook=unique_object)
    buffering.require(type(data) is dict and set(data)==set(buffering.FIELDS),'Task field schema changed')
    return core.Task(**{name:tuples(data[name]) for name in buffering.FIELDS})

def prepare_cached(pool,window,group_limit):
    buffering.require(window.width==8 and group_limit in (1,2,4),'Unsupported grouping')
    args=[(window.lo,window.hi,first,min(first+group_limit,window.last),window.bits,window.cap,window.geometry_policy)
          for first in range(window.first,window.last,group_limit)]
    rows=[row for part in pool.map(prepare_segment,args,8) for row in part]
    specs=tuple(row[5] for row in rows);payloads=tuple(row[0] for row in rows);tokens=[row[1] for row in rows]
    tasks=[decode(payload,token) for payload,token in zip(payloads,tokens)]
    spans=tuple((row[3],row[4]) for row in rows)
    view=coverage.Window(window.lo,window.hi,window.first,window.last,8,window.bits,window.cap,window.geometry_policy,group_limit,specs,spans)
    core.checked_tasks(specs,tasks)
    geometry=hashlib.sha256();size=0;snapshots=[]
    for task,payload in zip(tasks,payloads):
        buffering.require(coverage.night.native_safe(task),'Received task violates native safety bounds')
        snapshot=tuple(getattr(task,name) for name in buffering.FIELDS);buffering.immutable(snapshot);snapshots.append(snapshot)
        geometry.update(payload);geometry.update(b'\n');size+=len(payload)+1
    total=sum(task.points for task in tasks);buffering.require(total<=core.MAX_TOTAL_POINTS,'Coefficient allowance exhausted')
    groups=[];pending=[];points=0
    for task in tasks:
        buffering.require(task.points<=core.MAX_POINTS,'Task cannot fit native packet')
        if pending and (len(pending)==core.MAX_TASKS or points+task.points>core.MAX_POINTS):
            groups.append(core.encode_batch(pending,window.cap));pending=[];points=0
        pending.append(task);points+=task.points
    if pending:groups.append(core.encode_batch(pending,window.cap))
    certificate=hashlib.sha256(('\n'.join(tokens)+'\n').encode()).hexdigest()
    plan=core.VerifiedPlan(window.hi,window.cap,tuple(groups),(),len(tasks),total,certificate)
    size+=sum(len(batch.packet.encode()) for batch in groups)
    chunk=pipeline.PreparedChunk(view,plan,tuple((task.id,token,task.points) for task,token in zip(tasks,tokens)),geometry.hexdigest(),size,{},tuple(row[2] for row in rows))
    buffering.register(chunk,tasks,snapshots,payloads)
    return chunk
