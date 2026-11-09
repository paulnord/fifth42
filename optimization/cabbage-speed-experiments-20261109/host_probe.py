"""Finite fresh-work trials against the copied adaptive saved-root pipeline."""
import argparse,hashlib,json,multiprocessing as mp,os,statistics,sys,time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'source/lattice_prototype'
sys.path.insert(0,str(ROOT/'source/lattice_gpu'))
import scaling_core as core,overnight_search as night,coordinator_pipeline as pipeline
import coordinator_packing,packing_opt,exact_host_opt,precision_policy
from adapter_runtime import open_session,normalized_counts,normalized_hits,verify_workers
from bounded_prefetch import BoundedPrefetch

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def initialize(source,cpus,variant):
    mode=variant if variant in ('roots','inverse','combined') else 'reference'
    exact_host_opt.initialize(source,cpus,mode)
    if mode!='reference':
        core.prepare_task=exact_host_opt.prepare_task
        core.certify_task=exact_host_opt.certify_task
    if variant in ('serializer','combined_serializer'):
        if variant=='combined_serializer':
            exact_host_opt._MODE='combined'
            import exact_root_opt
            exact_root_opt.install_on_private_lattice(core.lattice()) if core.lattice() in exact_root_opt._PRIVATE else None
        core.task_digest=packing_opt.task_digest
    if variant=='warm':
        lattice=core.lattice();original=lattice.reduce_basis;previous=None
        def reduction(a,backend='reference'):
            nonlocal previous
            if backend!='fpylll':return original(a,backend)
            seed=a if previous is None else lattice.matmul(previous,a)
            b,v=original(seed,backend)
            u=v if previous is None else lattice.matmul(v,previous)
            if abs(lattice.det3(u))!=1 or lattice.matmul(u,a)!=b:raise ValueError('Warm transform certificate')
            previous=u
            return b,u
        lattice.reduce_basis=reduction

class Pool:
    def __init__(self,p,deadline):self.p,self.deadline=p,deadline
    def map(self,f,items,chunksize):return self.p.map_async(f,items,chunksize).get(timeout=max(.001,self.deadline-time.monotonic()))

def independent(batch):
    import subprocess
    p=subprocess.run([str(ROOT/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=30)
    response=json.loads(p.stdout);pipeline.validate_response_types(response)
    return response,core.decode_batch(batch,response,'emulated')

def trial(args):
    output=Path(args.output);output.mkdir(exist_ok=False,parents=True)
    began=time.perf_counter();cpus=tuple(sorted(os.sched_getaffinity(0))[:args.workers]);os.sched_setaffinity(0,set(cpus))
    initialize(SOURCE,(),args.variant)
    deadline=time.monotonic()+180
    pool=mp.get_context('spawn').Pool(args.workers,initializer=initialize,initargs=(SOURCE,cpus,args.variant));session=None
    try:
        p=Pool(pool,deadline);warmed={}
        while len(warmed)<args.workers:warmed.update(p.map(core.worker_identity,range(args.workers*4),1))
        verify_workers(warmed,cpus)
        session=open_session(ROOT/'bin/scaling_gpu','gpu',deadline);engine=pipeline.OwnedEngine(session)
        if args.width==8:
            first=args.first;last=first+args.patches
        else:
            first=args.first;last=first+args.patches//(args.width//8)
        # Every width uses a custom exact nested ratio partition. Window IDs
        # are local; TrialJournal still binds all IDs, certificates and counts.
        whole=pipeline.Window(100000000001,200000000000,first,last,args.width,222,42,'adaptive')
        left=Fraction(args.ratio_num,args.ratio_den);span=Fraction(args.patches*8,whole.lo)
        def specs(window):
            l=core.lattice();n=last-first
            return tuple((i,whole.lo,whole.hi,tuple((left+span*Fraction(i-first,n)).as_integer_ratio()),
                          tuple((left+span*Fraction(i+1-first,n)).as_integer_ratio()),42,
                          precision_policy.geometry_bits(l,whole.lo,whole.hi,
                            l.Q(*(left+span*Fraction(i-first,n)).as_integer_ratio()),l.Q(*(left+span*Fraction(i+1-first,n)).as_integer_ratio()),42))
                         for i in range(window.first,window.last))
        # Patch only the isolated harness's specification provider, preserving
        # fresh task preparation and independent exact certification.
        pipeline.Window.specifications=specs
        chunk_patches=max(1,256//(args.width//8))
        work=[replace(whole,first=i,last=min(i+chunk_patches,last)) for i in range(first,last,chunk_patches)]
        identity=dict(trial=output.name,source_identity=digest(dict(variant=args.variant,width=args.width)))
        def prepare(w):
            return pipeline.prepare_chunk(p,w,'packed',args.map_chunksize)
        stream=BoundedPrefetch(work,prepare,estimate_size=lambda _:(8*1024**2,core.MAX_TOTAL_POINTS),
            max_outstanding=3,max_item_bytes=8*1024**2,max_item_points=core.MAX_TOTAL_POINTS,
            max_queued_bytes=24*1024**2,max_queued_points=3*core.MAX_TOTAL_POINTS,
            actual_size=lambda c:(c.payload_bytes,c.plan.points))
        startup=time.perf_counter()-began;start=time.perf_counter();records=[];signatures=[];durations=[];commit_seconds=0;audits=0
        with pipeline.TrialJournal(output/'journal',identity,whole) as journal,stream:
            for chunk in stream:
                record=pipeline.execute_chunk(chunk,engine,trial=output.name,coordinator=0,timeout=30)
                if not records:
                    for batch,receipt in zip(chunk.plan.batches,record['batches']):
                        ref,found=independent(batch)
                        if normalized_counts(batch,ref)!=list(map(tuple,receipt['native_counts'])):raise ValueError('GMP counts')
                        if normalized_hits(batch,ref)!=list(map(tuple,receipt['native_hit_records'])):raise ValueError('GMP hits')
                    audits+=1
                t=time.perf_counter();journal.commit(record);commit_seconds+=time.perf_counter()-t
                signatures.append(dict(geometry=chunk.geometry_sha256,patches=chunk.patches,
                                       packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in chunk.plan.batches]))
                records.append(record);durations.append(dict(preparation=chunk.stages,workers=chunk.worker_seconds))
            state=dict(journal.state)
        steady=time.perf_counter()-start
        with pipeline.TrialJournal(output/'journal',identity,whole) as recovered:
            if recovered.state!=state:raise ValueError('Durable recovery mismatch')
        result=dict(variant=args.variant,width=args.width,workers=args.workers,cpus=cpus,map_chunksize=args.map_chunksize,
                    first=first,patches=last-first,ratio_left=left.as_integer_ratio(),ratio_right=(left+span).as_integer_ratio(),
                    steady_seconds=steady,startup_seconds=startup,points=state['points'],hits=state['hits'],
                    signatures_sha256=digest(signatures),commit_seconds=commit_seconds,independent_audits=audits,
                    stages=durations,records=records,queue=stream.snapshot(),recovery_passed=True,production_coverage=False)
        (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('variant','width','steady_seconds','points','hits','signatures_sha256')}),flush=True)
    finally:
        if session:session.close()
        pool.terminate();pool.join()

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--variant',default='reference',choices=['reference','roots','inverse','combined','serializer','warm'])
    a.add_argument('--width',type=int,default=8,choices=[8,16,32,64,128]);a.add_argument('--patches',type=int,default=1024)
    a.add_argument('--first',type=int,default=0);a.add_argument('--ratio-num',type=int,default=3);a.add_argument('--ratio-den',type=int,default=10)
    a.add_argument('--workers',type=int,default=4);a.add_argument('--map-chunksize',type=int,default=8);a.add_argument('--output',required=True)
    trial(a.parse_args())
