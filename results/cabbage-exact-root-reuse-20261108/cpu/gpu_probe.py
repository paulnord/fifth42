"""Scratch-only production-path validation and local durable CPU pipeline timing."""
import argparse
import bisect
import hashlib
import importlib.metadata
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
VARIANT=os.environ.get('ROOT_REUSE_VARIANT','baseline')
if VARIANT not in ('baseline','candidate'):raise ValueError('Invalid isolated variant')
SOURCE=ROOT/VARIANT/'source/lattice_prototype'
GPU=ROOT/VARIANT/'source/lattice_gpu'
sys.path.insert(0,str(GPU))
import adapter_runtime
from bounded_prefetch import BoundedPrefetch
import coordinator_pipeline as pipeline
import engine_session
import overnight_search as night
import packing_opt
import scaling_core as core


# Scratch-only instrumentation: preserve every exact native count/hit and timing.
import atexit
GPU_RESPONSES=[]
OriginalSession=engine_session.EngineSession
class RecordedSession(OriginalSession):
    def __init__(self,*args,**kwargs):
        active=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True).strip()
        if active: raise RuntimeError('GPU resource conflict: '+active)
        super().__init__(*args,**kwargs)
        self.gpu_pid=self.process.pid
    def run(self,packet,timeout=30):
        active=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True).strip().splitlines()
        if any(int(pid)!=self.gpu_pid for pid in active):
            self.close()
            raise RuntimeError('GPU resource conflict: '+str(active))
        response,wall=super().run(packet,timeout=min(timeout,30))
        GPU_RESPONSES.append(dict(packet_sha256=hashlib.sha256(packet.encode()).hexdigest(),wall_seconds=wall,response=response))
        return response,wall
engine_session.EngineSession=RecordedSession
atexit.register(lambda:Path(os.environ['GPU_LOG']).write_text(json.dumps(GPU_RESPONSES,indent=2)+'\n'))

def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(stable(x)).hexdigest()

def oracle(bound,cap):
    powers=[i**5 for i in range(bound+1)];hits=set()
    for c in range(1,bound+1):
      for b in range(1,c):
        target=powers[c]-powers[b]
        lo=bisect.bisect_left(powers,target-cap,1,b+1)
        hi=bisect.bisect_right(powers,target+cap,lo,b+1)
        for a in range(lo,hi):hits.add((a,b,c,powers[a]+powers[b]-powers[c]))
    return hits

def independent(batch):
    p=subprocess.run([str(ROOT/'native/bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=20)
    result=json.loads(p.stdout);pipeline.validate_response_types(result)
    return result,core.decode_batch(batch,result,'emulated')

def full_plan(bound,cap):
    specs,direct=core.specs(bound,cap,8)
    rows=[pipeline.prepare_certified(spec) for spec in specs]
    return packing_opt.assemble(bound,cap,specs,direct,[r[0] for r in rows],[r[1] for r in rows])

def validate(output):
    night.initialize(SOURCE)
    cases=[]
    binaries=['scaling_gpu']
    for binary in binaries:
      with engine_session.EngineSession([str(ROOT/'candidate/source/lattice_gpu/bin'/binary)],'gpu',time.monotonic()+120) as session:
        for bound,cap in ((34,384),(100,2951),(1000,42)):
            plan=full_plan(bound,cap);expected=oracle(bound,cap);hits=set(plan.direct_hits)
            counts=[]
            for batch in plan.batches:
                response,_=session.run(batch.packet);pipeline.validate_response_types(response)
                found=core.decode_batch(batch,response,'gpu');hits|=found
                ref,ref_hits=independent(batch)
                if adapter_runtime.normalized_counts(batch,response)!=adapter_runtime.normalized_counts(batch,ref):raise ValueError('GMP count mismatch')
                if adapter_runtime.normalized_hits(batch,response)!=adapter_runtime.normalized_hits(batch,ref):raise ValueError('GMP full record mismatch')
                if found!=ref_hits:raise ValueError('GMP exact hit mismatch')
                counts.extend(adapter_runtime.normalized_counts(batch,response))
            if hits!=expected or not hits:raise ValueError('Nonempty independent small-domain oracle failed')
            cases.append(dict(binary=binary,bound=bound,cap=cap,points=plan.points,tasks=plan.tasks,hits=sorted(hits),
                              certificates=plan.certificate_sha256,packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in plan.batches],counts=counts))
        for first in (3000000000,3917103232,6250000000,10625000000,11250000000):
            window=pipeline.Window(100000000001,200000000000,first,min(first+4,11250000001),8,222,42,'adaptive')
            class SerialPool:
                def map(self,f,items,chunksize):return list(map(f,items))
            chunk=pipeline.prepare_chunk(SerialPool(),window,'packed')
            record=pipeline.execute_chunk(chunk,pipeline.OwnedEngine(session),trial='validation',coordinator=0)
            for batch in chunk.plan.batches:
                response,_=session.run(batch.packet)
                ref,ref_hits=independent(batch)
                if adapter_runtime.normalized_counts(batch,response)!=adapter_runtime.normalized_counts(batch,ref):raise ValueError('High GMP counts')
                if adapter_runtime.normalized_hits(batch,response)!=adapter_runtime.normalized_hits(batch,ref):raise ValueError('High GMP hits')
                if core.decode_batch(batch,response,'gpu')!=ref_hits:raise ValueError('High decode mismatch')
            cases.append(dict(binary=binary,window=window.identity(),points=chunk.plan.points,patches=chunk.patches,
                              geometry=chunk.geometry_sha256,certificates=chunk.plan.certificate_sha256,hits=record['hits']))
    result=dict(status='passed',variant=VARIANT,cases=cases,production_coverage=False,no_cuda=False,cuda_executed=True)
    output.write_text(json.dumps(result,indent=2)+'\n')

class DeadlinePool:
    def __init__(self,pool,deadline):self.pool,self.deadline=pool,deadline
    def map(self,f,items,chunksize):
        return self.pool.map_async(f,items,chunksize).get(timeout=max(.001,self.deadline-time.monotonic()))

def benchmark(output,first,patches,workers):
    output.mkdir(parents=True,exist_ok=False)
    began=time.perf_counter();cpus=tuple(sorted(os.sched_getaffinity(0))[:workers])
    if len(cpus)!=workers:raise ValueError('Not enough CPU affinity slots')
    os.sched_setaffinity(0,set(cpus));night.initialize(SOURCE)
    deadline=time.monotonic()+120
    window=pipeline.Window(100000000001,200000000000,first,first+patches,8,222,42,'adaptive')
    context=mp.get_context('spawn');pool=context.Pool(workers,initializer=night.initialize,initargs=(SOURCE,cpus))
    session=None
    try:
        bounded=DeadlinePool(pool,deadline);warmed={}
        while len(warmed)<workers:warmed.update(bounded.map(core.worker_identity,range(workers*4),1))
        adapter_runtime.verify_workers(warmed,cpus)
        session=engine_session.EngineSession([str(ROOT/'candidate/source/lattice_gpu/bin/scaling_gpu')],'gpu',deadline)
        engine=pipeline.OwnedEngine(session)
        work=[pipeline.Window(window.lo,window.hi,i,min(i+256,window.last),8,222,42,'adaptive') for i in range(first,window.last,256)]
        pipeline.verify_partition(window,work)
        identity=dict(trial=output.name,source_identity=digest({'variant':VARIANT,'source':hashlib.sha256((SOURCE/'compiled_experiment/lattice5_snapshot.py').read_bytes()).hexdigest()}))
        prepare=lambda item:pipeline.prepare_chunk(bounded,item,'packed',8)
        stream=BoundedPrefetch(work,prepare,estimate_size=lambda _:(8*1024**2,core.MAX_TOTAL_POINTS),
            max_outstanding=3,max_item_bytes=8*1024**2,max_item_points=core.MAX_TOTAL_POINTS,
            max_queued_bytes=24*1024**2,max_queued_points=3*core.MAX_TOTAL_POINTS,
            actual_size=lambda chunk:(chunk.payload_bytes,chunk.plan.points))
        rows=[];signatures=[];audit_seconds=0.;commit_seconds=0.;audits=0
        startup=time.perf_counter()-began;steady_start=time.perf_counter()
        with pipeline.TrialJournal(output/'journal',identity,window) as journal,stream:
          for index,chunk in enumerate(stream):
            record=pipeline.execute_chunk(chunk,engine,trial=identity['trial'],coordinator=0,timeout=30)
            if index%128==0:
                t=time.perf_counter();gmp_hits=set()
                for batch in chunk.plan.batches:
                    _,hits=independent(batch);gmp_hits|=hits
                if gmp_hits!=set(map(tuple,record['hits'])):raise ValueError('Periodic GMP mismatch')
                audit_seconds+=time.perf_counter()-t;audits+=1
            t=time.perf_counter();journal.commit(record);commit_seconds+=time.perf_counter()-t
            signatures.append(dict(window=chunk.window.identity(),patches=chunk.patches,geometry=chunk.geometry_sha256,
                                   certificates=chunk.plan.certificate_sha256,packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in chunk.plan.batches],hits=record['hits']))
            rows.append(dict(points=chunk.plan.points,preparation=chunk.stages,worker_seconds=chunk.worker_seconds,consumption=record['stages']))
          checkpoint=dict(journal.state)
        steady=time.perf_counter()-steady_start
        # Reopen and validate the exact durable prefix outside the timing window.
        with pipeline.TrialJournal(output/'journal',identity,window) as recovered:
            if recovered.state!=checkpoint:raise ValueError('Recovery changed committed prefix')
        t=time.perf_counter();session.close();session=None;pool.close();pool.join();shutdown=time.perf_counter()-t
        result=dict(status='passed',variant=VARIANT,window=window.identity(),workers=workers,cpus=cpus,
            startup_seconds=startup,steady_seconds=steady,shutdown_seconds=shutdown,total_seconds=time.perf_counter()-began,
            patches_per_second=patches/steady,points=checkpoint['points'],signatures_sha256=digest(signatures),
            exact_hits=checkpoint['hits'],independent_gmp_audits=audits,audit_seconds=audit_seconds,
            durable_commit_seconds=commit_seconds,rows=rows,queue=stream.snapshot(),
            journal_bytes=checkpoint['journal_offset'],recovery_passed=True,production_coverage=False,
            environment=dict(python=platform.python_version(),machine=platform.machine(),pins={p:importlib.metadata.version(p) for p in ('gmpy2','fpylll','cysignals','numpy','sympy')}),
            limitations=['CUDA 13.2 RTX 3060; identical enumeration binary for both host-source variants.','Local filesystem journal, not NFS/shared ledger.','Four allowed cloud CPUs; not Ada topology or hardware.','Services, supervisors, publishers, and storage limits are not launched.'])
        (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('variant','steady_seconds','patches_per_second','points','signatures_sha256')}),flush=True)
    finally:
        if session:session.close()
        pool.terminate();pool.join()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('operation',choices=['validate','benchmark']);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--first',type=int,default=3917103232);parser.add_argument('--patches',type=int,default=1024);parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.operation=='validate':validate(args.output)
    else:benchmark(args.output,args.first,args.patches,args.workers)
