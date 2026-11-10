"""Forward-only packed/prefetched continuation; one GPU owner and journal writer."""
import argparse
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback

ROOT=Path(__file__).resolve().parent
GPU=ROOT/'source/lattice_gpu'
SOURCE=ROOT/'source/lattice_prototype'
sys.path.insert(0,str(GPU))
import adapter_runtime as adapter
import coordinator_benchmark as benchmark
import coordinator_pipeline as pipeline
from bounded_prefetch import BoundedPrefetch
import overnight_search as night
import packing_opt
import scaling_core as core
import policy
import runtime_initialize
import width_coverage
import buffered_pipeline
import scheduling
from durable_mirror import Replicator


class LivePool:
    def __init__(self,pool,config,output,stop_event,preparation_stage=None):
        self.pool,self.config,self.output,self.stop_event=pool,config,output,stop_event
        self.preparation_stage=preparation_stage

    def map(self,function,items,chunksize):
        if self.preparation_stage is not None and function is width_coverage.prepare_segment:
            return self.preparation_stage.dispatch(self.pool,list(items),
                check=lambda:policy.remaining(self.config,self.stop_event,self.output,30))
        pids=tuple(worker.pid for worker in self.pool._pool)
        pending=self.pool.map_async(function,items,self.config['dispatch_chunksize'] if function is width_coverage.prepare_segment else chunksize)
        began=time.monotonic()
        while True:
            left=policy.remaining(self.config,self.stop_event,self.output,30)
            if tuple(worker.pid for worker in self.pool._pool)!=pids or any(not worker.is_alive() for worker in self.pool._pool):
                raise RuntimeError('Preparation worker died or was replaced')
            if time.monotonic()-began>=30:raise TimeoutError('Preparation map exceeded 30 seconds')
            try:return pending.get(timeout=min(.25,left))
            except mp.TimeoutError:pass


class PreparationPacer:
    def __init__(self,config,output,stop_event):
        self.config,self.output,self.stop_event=config,output,stop_event
        self.seconds=0.

    def wait(self):
        began=time.monotonic()
        try:
            while True:
                policy.remaining(self.config,self.stop_event,self.output)
                if os.getloadavg()[0]<self.config['prep_load_ceiling']:return
                self.stop_event.wait(.2)
        finally:
            elapsed=time.monotonic()-began
            if elapsed>.01:self.seconds+=elapsed


def windows(config,last):
    size=config['chunk_patches']
    for first in range(config['initial_patch'],last,size):
        yield pipeline.Window(config['shell_lo'],config['shell_hi'],first,min(first+size,last),
                              config['width'],config['bits'],config['cap'],config.get('geometry_policy','baseline'))


def brute(bound,cap):
    powers=[n**5 for n in range(bound+1)]
    return {(a,b,c,powers[a]+powers[b]-powers[c]) for c in range(1,bound+1)
            for b in range(1,c) for a in range(1,b+1) if abs(powers[a]+powers[b]-powers[c])<=cap}


def independent(batch,output,config,stop_event):
    timeout=policy.remaining(config,stop_event,output,20)
    process=subprocess.run([str(ROOT/'bin/gmp_reference')],input=batch.packet,text=True,
                           capture_output=True,timeout=timeout)
    process.check_returncode();reference=json.loads(process.stdout)
    pipeline.validate_response_types(reference)
    decoded=core.decode_batch(batch,reference,'emulated')
    return reference,decoded


def controls(pool,engine,config,output,stop_event):
    reports=[]
    for bound,cap in ((34,42),(100,2951)):
        policy.remaining(config,stop_event,output)
        specs,direct=core.specs(bound,cap,8)
        rows=pool.map(pipeline.prepare_certified,specs,8)
        plan=packing_opt.assemble(bound,cap,specs,direct,[r[0] for r in rows],[r[1] for r in rows])
        expected=brute(bound,cap);policy.require(expected,'Nonempty control was empty')
        hits=set(plan.direct_hits)
        for batch in plan.batches:
            reference,reference_hits=independent(batch,output,config,stop_event)
            response,_=engine.run(batch.packet,timeout=policy.remaining(config,stop_event,output))
            pipeline.validate_response_types(response);hits.update(core.decode_batch(batch,response,'gpu'))
            policy.require(adapter.normalized_counts(batch,response)==adapter.normalized_counts(batch,reference),
                           'Nonempty control count mismatch')
            policy.require(adapter.normalized_hits(batch,response)==adapter.normalized_hits(batch,reference),
                           'Nonempty control full-record mismatch')
        policy.require(hits==expected,'Fresh exhaustive nonempty control failed')
        reports.append(dict(bound=bound,cap=cap,hits=sorted(hits),full_oracle_equal=True))
    night.atomic_json(output/'controls.json',dict(status='passed',cases=reports))


def run(config):
    output=Path(config['output']);output.mkdir(parents=True,exist_ok=False)
    parent_fd=os.open(output.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(parent_fd)
    finally:os.close(parent_fd)
    stop_event=threading.Event()
    pacer=PreparationPacer(config,output,stop_event)
    signal.signal(signal.SIGTERM,lambda *_:stop_event.set())
    signal.signal(signal.SIGINT,lambda *_:stop_event.set())
    cpus=tuple(config['physical_cpus']);os.sched_setaffinity(0,set(cpus));runtime_initialize.initialize(SOURCE)
    policy.require(len(cpus)==config['workers'] and len({(Path(f'/sys/devices/system/cpu/cpu{c}/topology/core_id').read_text().strip(),
                         Path(f'/sys/devices/system/cpu/cpu{c}/topology/physical_package_id').read_text().strip()) for c in cpus})==config['workers'],
                   'Physical core allocation changed')
    fingerprint=hashlib.sha256(policy.stable(dict(manifest_sha256=config['manifest_sha256'],config=config)).encode()).hexdigest()
    started=time.monotonic();search_started=None;pool=engine=journal=stream=preparation_stage=None
    phase='validating';reason=None;error=None;audited=0;last_notice=0;claim_lock=None;replicator=None;accepted_chunks=0;replica_nudged=False
    zero=dict(next_patch=config['initial_patch'],patches=0,chunks=0,points=0,hits=[],journal_offset=0,journal_sha256='0'*64)

    def status(force=False):
        nonlocal last_notice
        if not force and time.monotonic()-last_notice<10:return
        state=journal.state if journal else zero
        elapsed=time.monotonic()-(search_started if search_started is not None else started)
        row=dict(status=phase,reason=reason,error=error,updated_utc=policy.utc(),run_id=config['run_id'],
             parent_run=config['parent_run'],source_identity=fingerprint,stop_local=config['stop_local'],stop_epoch=config['stop_epoch'],
             geometry_policy=config['geometry_policy'],
             ledger_root=config['ledger_root'],ledger_claim_sha256=config['ledger_claim_sha256'],
             initial_patch=config['initial_patch'],next_patch=state['next_patch'],patches=state['patches'],chunks=state['chunks'],
             coefficient_points=state['points'],hits=state['hits'],gmp_audited_chunks=audited,
             journal_offset=state['journal_offset'],journal_sha256=state['journal_sha256'],completed_bound=None,
             independent_oracle_verified_through=0,workers=config['workers'],backend='gpu',
             engine_pid=engine.process.pid if engine else None,worker_pid=os.getpid(),
             selected_interval=[config['initial_patch'],state['next_patch']],
             combined_selected_patches=config['parent_selected_patches']+state['patches'],
             search_seconds=elapsed,patches_per_second=state['patches']/max(elapsed,.001),
             preparation_pacing_seconds=pacer.seconds,preparation_load_ceiling=config['prep_load_ceiling'],
             prefetch=stream.snapshot() if stream else None,automatic_resume=False,publication=False,
             physical_tasks=state.get('physical_tasks',state['patches']),group_limit=config['group_limit'],
             journal_storage='local durable journal; verified periodic bulk replica',
             replication=replicator.receipt if replicator else None,
             replication_error=replicator.error if replicator else None,
             journal_buffer=dict(pending_chunks=journal.head['chunks']-journal.state['chunks'],pending_bytes=journal.pending_bytes,flush_count=journal.flush_count,flush_seconds=journal.flush_seconds) if journal else None,
             dispatch_chunksize=config['dispatch_chunksize'],canonical_task_cache=True,
             preparation_backend=config.get('preparation_backend','cpu'),
             preparation_windows=config.get('preparation_windows',16),
             gpu_preparation=preparation_stage.metrics if preparation_stage else None)
        night.atomic_json(output/'status.json',row);last_notice=time.monotonic()
        print(json.dumps({k:row[k] for k in ('status','next_patch','patches','chunks','gmp_audited_chunks','patches_per_second','reason','error')}),flush=True)

    def remaining(cap=30):return policy.remaining(config,stop_event,output,cap)

    try:
        store,claim=policy.validate_ledger(config)
        pending_lock=store.locked(store.root/'jobs'/config['ledger_job']/'journal.jsonl')
        pending_lock.__enter__()
        claim_lock=pending_lock
        night.atomic_json(output/'run-config.json',config)
        night.atomic_json(output/'run-manifest.json',json.loads(Path(config['manifest']).read_bytes()))
        replicator=Replicator(output,config['replica_output'],dict(trial=config['run_id'],source_identity=fingerprint),config['replica_interval_seconds'])
        replicator.start()
        status(True);remaining()
        preparation_backend=config.get('preparation_backend','cpu')
        policy.require(preparation_backend in ('cpu','gpu'),'Unsupported preparation backend')
        if preparation_backend=='gpu':
            # Optional: benchmarks favored this path for Ada's sampled region.
            # CPU remains the default; exact certification/fallback are unchanged.
            import gpu_preparation
            preparation_stage=gpu_preparation.GPUStage(config['workers'],
                capacity=config.get('preparation_gpu_capacity',128),
                require_lll=config.get('preparation_require_lll',False))
            initializer=gpu_preparation.initialize;initargs=preparation_stage.initargs(SOURCE,cpus)
        else:initializer=runtime_initialize.initialize;initargs=(SOURCE,cpus)
        pool=mp.get_context('spawn').Pool(config['workers'],initializer=initializer,initargs=initargs)
        limited=LivePool(pool,config,output,stop_event,preparation_stage)
        warmed={}
        while len(warmed)<config['workers']:warmed.update(limited.map(core.worker_identity,range(4*config['workers']),1))
        adapter.verify_workers(warmed,cpus)
        night.atomic_json(output/'worker-affinities.json',warmed)
        if preparation_stage:preparation_stage.start()
        engine=adapter.open_session(ROOT/'bin/scaling_gpu','gpu',time.monotonic()+remaining(config['stop_epoch']-time.time()))
        controls(limited,engine,config,output,stop_event);remaining()
        last=min(night.grid_count(config['shell_lo'],8),config['range_end'])
        if config.get('test_chunk_limit'):last=min(last,config['initial_patch']+config['chunk_patches']*config['test_chunk_limit'])
        whole=width_coverage.Window(config['shell_lo'],config['shell_hi'],config['initial_patch'],last,8,222,42,
                              config['geometry_policy'],config['group_limit'])
        pipeline.validate_chunk=buffered_pipeline.validate_cached
        journal=buffered_pipeline.BufferedJournal(output,dict(trial=config['run_id'],source_identity=fingerprint),whole,records=config['journal_buffer_records'],max_bytes=config['journal_buffer_bytes'],max_age=config['journal_buffer_max_age_seconds'])
        search_started=time.monotonic();phase='running';status(True)

        def prepare_many(batch):
            remaining()
            pacer.wait()
            for prepared in scheduling.prepare_many(limited,batch,config['group_limit'],cache=True):
                remaining()
                yield prepared
        stream=scheduling.BulkStream(windows(config,last),prepare_many,
            config.get('preparation_windows',16),ready_limit=config['ready_queue_limit'])
        with stream:
            for chunk in stream:
                remaining()
                policy.check_storage(config,output)
                record=pipeline.execute_chunk(chunk,pipeline.OwnedEngine(engine),trial=config['run_id'],
                                               coordinator=0,timeout=remaining())
                width_coverage.add_coverage(record,chunk,config['group_limit'])
                if time.time()-replicator.last_success>config['maximum_replica_lag_seconds']:
                    raise policy.RequestedStop('Verified replica has fallen behind its time budget')
                if accepted_chunks%config['gmp_audit_period']==0:
                    path=output/'independent-audits';path.mkdir(exist_ok=True)
                    for batch_index,(batch,receipt) in enumerate(zip(chunk.plan.batches,record['batches'])):
                        reference,found=independent(batch,output,config,stop_event)
                        policy.require(adapter.normalized_counts(batch,reference)==list(map(tuple,receipt['native_counts'])),
                                       'Periodic independent GMP count mismatch')
                        policy.require(adapter.normalized_hits(batch,reference)==list(map(tuple,receipt['native_hit_records'])),
                                       'Periodic independent GMP full-record mismatch')
                        night.atomic_json(path/f"{accepted_chunks+1:08d}-{batch_index}.json",reference)
                    record['independent_gmp_audited']=True
                else:record['independent_gmp_audited']=False
                # Ahead-prepared windows never advance this durable serial cursor.
                journal.commit(record)
                accepted_chunks+=1
                stream.ack(chunk)
                if journal.state['chunks'] and not replica_nudged:
                    replicator.nudge();replica_nudged=True
                if record['independent_gmp_audited']:audited+=1
                status()
                if config.get('test_chunk_limit') and accepted_chunks>=config['test_chunk_limit']:
                    reason='Bounded integration chunks completed';break
        phase='completed_test' if config.get('test_chunk_limit') else 'stopped'
        if reason is None:reason='Selected remaining shell endpoint reached'
    except policy.RequestedStop as exc:
        phase='stopped';reason=str(exc)
    except BaseException as exc:
        requested_stop=None
        if isinstance(exc,(TimeoutError,subprocess.TimeoutExpired)):
            # An RPC or GMP audit may use the last few milliseconds of the
            # remaining allowance. Its timeout must still be a clean deadline
            # stop, with that uncommitted chunk omitted from the durable prefix.
            try:remaining()
            except policy.RequestedStop as stop:requested_stop=str(stop)
        if requested_stop is not None:
            phase='stopped';reason=requested_stop
        else:
            phase='failed';error=f'{type(exc).__name__}: {exc}';reason='Failure: committed prefix preserved'
            (output/'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        if stream:stream.close()
        if engine:engine.close()
        if pool:pool.terminate();pool.join()
        if preparation_stage:
            try:preparation_stage.close()
            except BaseException as exc:
                phase='failed';reason='GPU preparation cleanup failed; committed prefix preserved';error=f'{type(exc).__name__}: {exc}'
        if journal:
            try:journal.close()
            except BaseException as exc:
                phase='failed';reason='Final journal flush failed; preserve the last committed prefix';error=f'{type(exc).__name__}: {exc}'
                (output/'failure-traceback.txt').write_text(traceback.format_exc())
        try:
            status(True)
            if replicator:replicator.finish()
        finally:
            if claim_lock:claim_lock.__exit__(None,None,None)
    return 2 if phase=='failed' else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--config',type=Path,required=True)
    args=parser.parse_args();raise SystemExit(run(policy.load_config(args.config)))
