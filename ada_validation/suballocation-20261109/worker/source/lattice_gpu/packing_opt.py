"""Packing-only alternative; preserves every canonical certificate byte."""
from dataclasses import fields
import hashlib
import json
import scaling_core as core

_FIELDS=tuple(field.name for field in fields(core.Task))

def task_payload(task):
    # Task and all its nested data are immutable primitive tuples/integers.
    # JSON encodes these exactly as the recursive asdict() copy does.
    return json.dumps({name:getattr(task,name) for name in _FIELDS},
                      sort_keys=True,separators=(',',':')).encode()

def task_digest(task):
    return hashlib.sha256(task_payload(task)).hexdigest()

def assemble(bound,cap,specifications,direct,tasks,certificates):
    core.checked_tasks(specifications,tasks)
    if len(certificates)!=len(tasks) or any(len(x)!=64 for x in certificates):
        raise ValueError('Missing exact patch certificates')
    if any(task_digest(task)!=digest for task,digest in zip(tasks,certificates)):
        raise ValueError('Patch certificates do not identify the prepared immutable tasks')
    total=sum(t.points for t in tasks)
    if total>core.MAX_TOTAL_POINTS:raise ValueError('Full-domain coefficient allowance exhausted')
    groups=[];pending=[];points=0
    for task in tasks:
        if task.points>core.MAX_POINTS:raise ValueError('Single task cannot fit a packet')
        if pending and (len(pending)==core.MAX_TASKS or points+task.points>core.MAX_POINTS):
            groups.append(core.encode_batch(pending,cap));pending=[];points=0
        pending.append(task);points+=task.points
    if pending:groups.append(core.encode_batch(pending,cap))
    hits=[]
    for lo,hi in direct:
        for c in range(lo,hi+1):
            for b in range(1,c):
                for a in range(1,b+1):
                    r=a**5+b**5-c**5
                    if abs(r)<=cap:hits.append((a,b,c,r))
    digest=hashlib.sha256(('\n'.join(certificates)+'\n').encode()).hexdigest()
    return core.VerifiedPlan(bound,cap,tuple(groups),tuple(sorted(set(hits))),len(tasks),total,digest)
