#!/usr/bin/env python3
"""Transport-only microbenchmark using REAL production packet encoder/validator.
Synthetic tasks are NOT mathematically certified and MUST NOT be searched.
Accept a pinned archived worker directory; no production module is modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time
from dataclasses import fields
from sealed_packets import PacketSeals


def fixture(b, count):
    c=b.core
    ident=((1,0,0),(0,1,0),(0,0,1))
    rational=tuple(tuple((x,1) for x in row) for row in ident)
    tasks=tuple(c.Task(i,100,199,(i,10000),(i+1,10000),42,48,ident,(1,1,1),27,rational,rational) for i in range(count))
    payloads=tuple(b.packing_opt.task_payload(t) for t in tasks)
    tokens=tuple(hashlib.sha256(p).hexdigest() for p in payloads)
    specs=tuple((t.id,t.cmin,t.cmax,t.left,t.right,t.cap,t.bits) for t in tasks)
    spans=tuple((i,i+1) for i in range(count))
    window=b.coverage.Window(100,199,0,count,8,48,42,'baseline',1,specs,spans)
    batch=c.encode_batch(tasks,42)
    digest=hashlib.sha256(b''.join(p+b'\n' for p in payloads)).hexdigest()
    cert=hashlib.sha256(('\n'.join(tokens)+'\n').encode()).hexdigest()
    plan=c.VerifiedPlan(199,42,(batch,),(),count,27*count,cert)
    chunk=b.pipeline.PreparedChunk(window,plan,tuple((t.id,k,t.points) for t,k in zip(tasks,tokens)),digest,len(batch.packet),{},())
    snapshots=tuple(tuple(getattr(t,f.name) for f in fields(t)) for t in tasks)
    b.register(chunk,tasks,snapshots,payloads)
    return chunk


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--worker',type=Path,required=True)
    p.add_argument('--output',type=Path,default=Path('packet-results.json'))
    p.add_argument('--tasks',type=int,default=1024)
    p.add_argument('--repeats',type=int,default=20)
    a=p.parse_args()
    if not 1<=a.tasks<=4096 or not 2<=a.repeats<=1000:p.error('bounded tasks/repeats required')
    sys.path.insert(0,str(a.worker.resolve()))
    import buffered_pipeline as b
    chunk=fixture(b,a.tasks)
    seals=PacketSeals(b.validate_cached)
    start=time.perf_counter();seals.seal(chunk);setup=time.perf_counter()-start
    rows=[]
    for i in range(a.repeats):
        for label,fn in ((('baseline',b.validate_cached),('sealed',seals.validate)) if i%2==0 else (('sealed',seals.validate),('baseline',b.validate_cached))):
            t=time.perf_counter();fn(chunk);rows.append(dict(repeat=i,variant=label,seconds=time.perf_counter()-t))
    # Independent controls against actual production dataclasses.
    original=chunk.plan.batches[0].packet
    object.__setattr__(chunk.plan.batches[0],'packet',original+'# changed\n')
    rejected=[]
    for name,fn in [('baseline',b.validate_cached),('sealed',seals.validate)]:
        try:fn(chunk)
        except ValueError:rejected.append(name)
    object.__setattr__(chunk.plan.batches[0],'packet',original)
    if rejected!=['baseline','sealed']:raise RuntimeError('corruption control failed')
    med={k:statistics.median(r['seconds'] for r in rows if r['variant']==k) for k in ('baseline','sealed')}
    result=dict(scope='SYNTHETIC transport validation only; NO scientific certification, GPU, coverage or pipeline speedup',tasks=a.tasks,seal_setup_seconds=setup,median_seconds=med,baseline_over_sealed=med['baseline']/med['sealed'],corruption_rejected=rejected,trials=rows)
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='trials'},indent=2))
if __name__=='__main__':main()
