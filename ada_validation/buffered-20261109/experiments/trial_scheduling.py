"""Matched finite pipeline trial. TEST_ONLY; no production ledger writes."""
import argparse,hashlib,json,multiprocessing as mp,os
from pathlib import Path
import resource,subprocess,sys,time
import buffered_pipeline as buffering
import scheduling
import adapter_runtime as adapter
import audit_grouped
from bounded_prefetch import BoundedPrefetch
import coordinator_pipeline as pipeline
import overnight_search as night
import runtime_initialize
import scaling_core as core
import width_coverage as coverage
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
VARIANTS={
 'baseline':dict(cache=False,journal='baseline'),
 'encode_once':dict(cache=False,journal='buffer',records=1,single_encode=True),
 'cache':dict(cache=True,journal='baseline'),
 'buffer8':dict(cache=False,journal='buffer',records=8,single_encode=False),
 'cache_buffer8':dict(cache=True,journal='buffer',records=8,single_encode=True),
 'cache_buffer32':dict(cache=True,journal='buffer',records=32,single_encode=True),
 'cache_async8':dict(cache=True,journal='async',records=8),
 'cache_ram':dict(cache=True,journal='ram')}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--variant',choices=VARIANTS,required=True)
    parser.add_argument('--workers',type=int,choices=(4,8,16),default=16);parser.add_argument('--first',type=int,required=True)
    parser.add_argument('--patches',type=int,default=32768);parser.add_argument('--group-limit',type=int,choices=(1,2,4),default=2)
    parser.add_argument('--map-chunksize',type=int,choices=(2,4,8),default=8);parser.add_argument('--prep-windows',type=int,choices=(1,2,4),default=1)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();opts=VARIANTS[args.variant]
    assert 0<args.patches<=65536 and args.first+args.patches<=11250000001
    args.output.mkdir(mode=0o700,parents=True,exist_ok=False);os.nice(19);cpus=tuple(range(args.workers));os.sched_setaffinity(0,set(cpus))
    startup=time.monotonic();runtime_initialize.initialize(W/'source/lattice_prototype')
    if opts['cache']:pipeline.validate_chunk=buffering.validate_cached
    pool=mp.get_context('spawn').Pool(args.workers,initializer=runtime_initialize.initialize,initargs=(W/'source/lattice_prototype',cpus))
    engine=journal=stream=None;started=None
    try:
        warmed={};until=time.monotonic()+15
        while len(warmed)<args.workers:
            assert time.monotonic()<until,'Pool did not warm'
            warmed.update(pool.map(core.worker_identity,range(4*args.workers),1))
        adapter.verify_workers(warmed,cpus)
        engine=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+120)
        trial='TEST_ONLY_'+args.output.name;whole=coverage.Window(100000000001,200000000000,args.first,args.first+args.patches,8,222,42,'adaptive',args.group_limit)
        identity=dict(trial=trial,source_identity=hashlib.sha256((ROOT/'experiment-manifest-r3.json').read_bytes()).hexdigest())
        kind=opts['journal']
        if kind=='baseline':journal=coverage.TrialJournal(args.output,identity,whole)
        elif kind=='buffer':journal=buffering.BufferedJournal(args.output,identity,whole,records=opts['records'],single_encode=opts['single_encode'])
        elif kind=='async':journal=buffering.AsyncJournal(args.output,identity,whole,records=opts['records'])
        else:journal=buffering.MemoryJournal(identity,whole)
        def windows():
            for first in range(args.first,whole.last,256):
                yield pipeline.Window(whole.lo,whole.hi,first,min(first+256,whole.last),8,222,42,'adaptive')
        dispatch=scheduling.DispatchPool(pool,args.map_chunksize)
        def prepare_many(windows):return scheduling.prepare_many(dispatch,windows,args.group_limit,opts['cache'])
        stream=scheduling.ReadyQueue(windows(),prepare_many,batch=args.prep_windows,ready_limit=3,active_limit=1)
        signatures=hashlib.sha256();hits=set();stages={};kernel=0.;audits=0;total_points=0;physical=0;commit_seconds=0.;peak_payload=0
        accepted_chunks=0;max_pending=0;started=time.monotonic();startup_seconds=started-startup
        with stream:
            for chunk in stream:
                if time.monotonic()-started>110:raise TimeoutError('Finite test exceeded resource deadline')
                signatures.update(json.dumps(dict(patches=chunk.patches,geometry=chunk.geometry_sha256,certificate=chunk.plan.certificate_sha256,
                     packets=[hashlib.sha256(batch.packet.encode()).hexdigest() for batch in chunk.plan.batches],specs=chunk.window.explicit_specs,spans=chunk.window.spans),sort_keys=True,separators=(',',':')).encode())
                record=coverage.add_coverage(pipeline.execute_chunk(chunk,pipeline.OwnedEngine(engine),trial=trial,coordinator=0,timeout=20),chunk,args.group_limit)
                record['independent_gmp_audited']=accepted_chunks%128==0
                if record['independent_gmp_audited']:
                    folder=args.output/'independent-audits';folder.mkdir(exist_ok=True)
                    for index,(batch,receipt) in enumerate(zip(chunk.plan.batches,record['batches'])):
                        done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=20)
                        ref=json.loads(done.stdout);pipeline.validate_response_types(ref)
                        assert adapter.normalized_counts(batch,ref)==list(map(tuple,receipt['native_counts']))
                        assert adapter.normalized_hits(batch,ref)==list(map(tuple,receipt['native_hit_records']))
                        night.atomic_json(folder/f'{accepted_chunks+1:08d}-{index}.json',ref)
                    audits+=1
                began=time.monotonic();journal.commit(record);commit_seconds+=time.monotonic()-began
                accepted_chunks+=1;max_pending=max(max_pending,accepted_chunks-journal.state['chunks'])
                hits.update(map(tuple,record['hits']));total_points+=record['points'];physical+=len(record['patches']);peak_payload=max(peak_payload,chunk.payload_bytes)
                for name,value in record['stages'].items():
                    slot=stages.setdefault(name,dict(wall_seconds=0.,thread_cpu_seconds=0.))
                    slot['wall_seconds']+=value['wall_seconds'];slot['thread_cpu_seconds']+=value['thread_cpu_seconds']
                kernel+=sum(receipt['kernel_seconds'] or 0. for receipt in record['batches'])
                stream.ack(chunk)
        began=time.monotonic();journal.close();commit_seconds+=time.monotonic()-began
        elapsed=time.monotonic()-started;state=dict(journal.state);snapshot=stream.snapshot()
        assert state['next_patch']==whole.last and state['patches']==args.patches and state['points']==total_points and state['physical_tasks']==physical
        maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if kind!='ram':
            captured=json.loads((args.output/'checkpoint.json').read_bytes());assert captured==state
            audit=audit_grouped.audit_suffix(args.output,dict(checkpoint=dict(next_patch=args.first),config=dict(group_limit=args.group_limit,gmp_audit_period=128)),captured,'fresh',128)
            with coverage.TrialJournal(args.output,identity,whole) as recovered:assert recovered.state==state
            recovery=True
        else:
            previous='0'*64
            for index,raw in enumerate(journal.data.splitlines(),1):
                row=json.loads(raw);digest=row.pop('sha256');assert hashlib.sha256(audit_grouped.stable(row)).hexdigest()==digest
                assert row['previous_sha256']==previous and row['sequence']==index;previous=digest
            assert previous==state['journal_sha256'];audit=None;recovery=False
        metrics=dict(flush_count=getattr(journal,'flush_count',None),peak_pending_bytes=getattr(journal,'peak_pending_bytes',None))
        if kind=='async':metrics=dict(flush_count=journal.journal.flush_count,peak_pending_bytes=journal.journal.peak_pending_bytes,peak_queued_records=journal.peak_queued_records)
        result=dict(status='passed',TEST_ONLY=True,variant=args.variant,workers=args.workers,first=args.first,patches=args.patches,group_limit=args.group_limit,
              steady_seconds=elapsed,startup_seconds=startup_seconds,map_chunksize=args.map_chunksize,prep_windows=args.prep_windows,patches_per_second=args.patches/elapsed,points=total_points,physical_tasks=physical,
              hits=sorted(hits),signatures_sha256=signatures.hexdigest(),kernel_seconds=kernel,stages=stages,commit_seconds=commit_seconds,
              audit_count=audits,queue=snapshot,maximum_uncommitted_chunks=max_pending,peak_prepared_payload_bytes=peak_payload,
              parent_maxrss_kib=maxrss,journal=metrics,journal_bytes=state['journal_offset'],recovery_passed=recovery,
              durable=kind!='ram',durable_journal_closed_before_timing_end=kind!='ram',production_coverage=False)
        (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status','variant','workers','steady_seconds','patches_per_second','maximum_uncommitted_chunks','durable')}),flush=True)
    finally:
        if stream:stream.close()
        if journal:journal.close()
        if engine:engine.close()
        pool.terminate();pool.join()
if __name__=='__main__':main()
