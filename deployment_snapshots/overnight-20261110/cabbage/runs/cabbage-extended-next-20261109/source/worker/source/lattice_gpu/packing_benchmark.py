#!/usr/bin/env python3
"""Packing-only paired comparison with fresh preparation on every timed pass."""
import argparse
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parent
BOUNDS=(8000,32000)
REPEATS=5
WORKERS=16

def worker(config):
    import scaling_core as core
    import packing_opt as optimized
    from engine_session import EngineSession
    import benchmark as helpers
    run=Path(config['run']);deadline=config['deadline_monotonic']
    selected=config['physical_cpus'][:WORKERS];host_only=config['host_only']
    source=ROOT/'lattice_prototype';core.initialize(source)
    result=dict(status='running',experiment='packing-only',host_only=host_only,repeats=REPEATS,
        workers=WORKERS,bounds=list(BOUNDS),width=2,bits=48,cases=[],controls=[],
        fresh_geometry_every_timed_variant=True,preparation_reuse_benchmark=False,
        certificate_hash_format_unchanged=True,engine_packet_format_unchanged=True,
        gpu_request_wall_seconds=0,
        warm_definition='fresh preparation and certification, existing persistent engines and worker pool',
        cold_definition='fresh worker pool and engine; includes startup, fresh preparation, exact output checks and shutdown; excludes report-file writes')
    context=multiprocessing.get_context('spawn');signatures={};pool=cpu=gpu=None
    def save():helpers.write_json(run/'results.json',result)
    def event(name,**data):
        with (run/'events.jsonl').open('a') as stream:stream.write(json.dumps(dict(event=name,**data))+'\n')
    def remaining(cap=120):
        left=deadline-time.monotonic()-8
        if left<1:raise TimeoutError('600-second packing comparison allowance exhausted')
        return min(left,cap)
    def charge(seconds):
        result['gpu_request_wall_seconds']+=seconds
        if result['gpu_request_wall_seconds']>120:raise TimeoutError('GPU request/startup allowance exhausted')
    def start_pool(warm):
        os.sched_setaffinity(0,set(selected));start=time.perf_counter()
        p=context.Pool(WORKERS,initializer=core.initialize,initargs=(source,selected))
        if warm:
            known=set()
            while len(known)<WORKERS:
                known.update(pid for pid,_ in p.map(core.worker_identity,range(WORKERS*2),1))
                if time.perf_counter()-start>60:
                    p.terminate();p.join();raise TimeoutError('Worker warmup failed')
        return p,time.perf_counter()-start
    def start_engine(backend):
        if backend=='gpu':os.sched_setaffinity(0,{selected[0]})
        else:os.sched_setaffinity(0,set(selected))
        command=[str(ROOT/'bin'/('scaling_gpu' if backend=='gpu' else 'scaling_cpu'))]
        if backend!='gpu':command+=['--threads',str(WORKERS)]
        session=EngineSession(command,backend,deadline)
        if backend=='gpu':charge(session.startup_seconds)
        os.sched_setaffinity(0,set(selected))
        return session
    def oracle(bound,cap):
        command=[str(ROOT/'bin/scaling_oracle'),str(bound),str(cap)]
        p=subprocess.run(command,text=True,capture_output=True,timeout=remaining())
        if p.returncode:raise RuntimeError('Independent exact oracle failed: '+p.stderr)
        data=json.loads(p.stdout)
        if data.get('complete') is not True or data['bound']!=bound or data['cap']!=cap:
            raise RuntimeError('Oracle domain mismatch')
        hits={tuple(h) for h in data['hits']}
        if any(not 1<=a<=b<c<=bound or a**5+b**5-c**5!=r or abs(r)>cap for a,b,c,r in hits):
            raise RuntimeError('Oracle exact residual mismatch')
        helpers.write_json(run/'oracles'/f'B{bound}-cap{cap}.json',data)
        return hits
    def prepare(p,bound,cap,variant):
        start=time.perf_counter();specifications,direct=core.specs(bound,cap)
        tasks=p.map(core.prepare_task,specifications,32)
        preparation=time.perf_counter()-start
        start=time.perf_counter();tokens=p.map(core.certify_task,tasks,32)
        certification=time.perf_counter()-start
        start=time.perf_counter()
        plan=(core.assemble if variant=='baseline' else optimized.assemble)(bound,cap,specifications,direct,tasks,tokens)
        packing=time.perf_counter()-start
        return plan,dict(prepare_seconds=preparation,certificate_seconds=certification,
            packing_seconds=packing,total_preparation_seconds=preparation+certification+packing)
    def check_identity(plan):
        key=(plan.bound,plan.cap)
        signature=dict(certificate_sha256=plan.certificate_sha256,tasks=plan.tasks,points=plan.points,
            packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in plan.batches],
            direct_hits=plan.direct_hits)
        if key in signatures and signatures[key]!=signature:
            raise RuntimeError('Packing comparison changed geometry, certificates or packet bytes')
        signatures[key]=signature
        return signature
    def execute(session,plan,expected):
        rpc=verification=engine=kernel=0.;hits=set(plan.direct_hits);outputs=[]
        for batch in plan.batches:
            data,wall=session.run(batch.packet,timeout=remaining())
            if session.backend=='gpu':charge(wall)
            rpc+=wall;start=time.perf_counter()
            hits|=core.decode_batch(batch,data,session.backend)
            verification+=time.perf_counter()-start
            engine+=data['engine_seconds'];kernel+=data['kernel_seconds'];outputs.append(data)
        if hits!=expected:raise RuntimeError('Complete exact hit set differs from independent oracle')
        return dict(request_wall_seconds=rpc,output_verification_seconds=verification,
            engine_seconds=engine,kernel_seconds=kernel,cached_packet_seconds=rpc+verification),outputs,hits
    def record(case,variant,backend,repeat,plan,metrics,outputs,hits):
        path=run/'trials'/f"{case['regime']}-B{case['bound']}-R{repeat+1}-{variant}-{backend}.json"
        helpers.write_json(path,dict(regime=case['regime'],bound=case['bound'],variant=variant,backend=backend,
            repeat=repeat+1,metrics=metrics,oracle_equal=True,exact_hits=sorted(hits),batches=outputs,
            certificate_sha256=plan.certificate_sha256))
        case['samples'].setdefault(variant,{}).setdefault(backend,[]).append(dict(repeat=repeat+1,
            **metrics,result_file=str(path.relative_to(run)),sha256=helpers.sha(path)))
        save()
    def summarize(case):
        medians={}
        for variant,backends in case['samples'].items():
            medians[variant]={}
            for backend,rows in backends.items():
                if len(rows)!=REPEATS:raise RuntimeError('A complete comparison requires five paired repeats')
                medians[variant][backend]={key:statistics.median(r[key] for r in rows)
                    for key in rows[0] if key.endswith('_seconds')}
        case.update(medians=medians,complete=True,phase='complete');save()
        event('case_complete',regime=case['regime'],bound=case['bound'],medians=medians)
    try:
        pool,pool_startup=start_pool(True);cpu=start_engine('emulated')
        if not host_only:gpu=start_engine('gpu')
        result['warm_startup_seconds']=dict(pool=pool_startup,cpu=cpu.startup_seconds,
            gpu=None if gpu is None else gpu.startup_seconds)
        for bound,cap in ((34,384),(100,2951)):
            expected=oracle(bound,cap)
            if not expected:raise RuntimeError('Nonempty control returned no hits')
            plans={}
            for variant in ('baseline','optimized'):
                plan,_=prepare(pool,bound,cap,variant);plans[variant]=plan;check_identity(plan)
                execute(cpu,plan,expected)
                if gpu is not None:execute(gpu,plan,expected)
            if plans['baseline']!=plans['optimized']:raise RuntimeError('Complete control plans differ')
            result['controls'].append(dict(bound=bound,cap=cap,exact_hits=sorted(expected),passed=True))
            save();event('control_passed',bound=bound,cap=cap)
        expected_by_bound={bound:oracle(bound,42) for bound in BOUNDS}
        for bound in BOUNDS:
            case=dict(regime='persistent_engines',host_workers=WORKERS,bound=bound,complete=False,
                phase='paired_repeats',samples={},orders=[])
            result['cases'].append(case);save()
            for repeat in range(REPEATS):
                order=('baseline','optimized') if repeat%2==0 else ('optimized','baseline')
                case['orders'].append(list(order))
                for variant in order:
                    remaining();plan,timing=prepare(pool,bound,42,variant)
                    case['identity']=check_identity(plan)
                    backends=[('cpu',cpu)]+([] if gpu is None else [('cuda',gpu)])
                    if repeat%2:backends.reverse()
                    for backend,session in backends:
                        metrics,raw,hits=execute(session,plan,expected_by_bound[bound]);metrics.update(timing)
                        metrics['end_to_end_seconds']=timing['total_preparation_seconds']+metrics['cached_packet_seconds']
                        record(case,variant,backend,repeat,plan,metrics,raw,hits)
                event('round_complete',regime=case['regime'],bound=bound,repeat=repeat+1)
            summarize(case)
        cpu.close();cpu=None
        if gpu is not None:gpu.close();gpu=None
        pool.close();pool.join();pool=None
        # Actual cold one-pass lifetimes are measured separately, with a fresh
        # pool, fresh engine and fresh geometry for every timed variant.
        for bound in BOUNDS:
            case=dict(regime='cold_one_pass',host_workers=WORKERS,bound=bound,complete=False,
                phase='paired_repeats',samples={},orders=[])
            result['cases'].append(case);save()
            for repeat in range(REPEATS):
                order=('baseline','optimized') if repeat%2==0 else ('optimized','baseline')
                case['orders'].append(list(order))
                for variant in order:
                    remaining();start=time.perf_counter();cold_pool=session=None
                    try:
                        cold_pool,pool_creation=start_pool(False)
                        backend='cpu' if host_only else 'cuda'
                        session=start_engine('emulated' if host_only else 'gpu')
                        startup=time.perf_counter()-start
                        plan,timing=prepare(cold_pool,bound,42,variant);case['identity']=check_identity(plan)
                        metrics,raw,hits=execute(session,plan,expected_by_bound[bound]);metrics.update(timing)
                        shutdown=time.perf_counter();session.close();session=None
                        cold_pool.close();cold_pool.join();cold_pool=None
                        metrics.update(cold_startup_seconds=startup,shutdown_seconds=time.perf_counter()-shutdown,
                            cold_one_pass_seconds=time.perf_counter()-start)
                        record(case,variant,backend,repeat,plan,metrics,raw,hits)
                    finally:
                        if session is not None:session.close()
                        if cold_pool is not None:cold_pool.terminate();cold_pool.join()
                event('round_complete',regime=case['regime'],bound=bound,repeat=repeat+1)
            summarize(case)
        result.update(status='passed',all_geometry_and_packet_bytes_equal=True)
        save();event('finished',status='passed');return 0
    except BaseException as error:
        result.update(status='stopped_at_guard' if isinstance(error,(TimeoutError,subprocess.TimeoutExpired)) else 'failed',
            error=f'{type(error).__name__}: {error}',traceback=traceback.format_exc())
        save();event('finished',status=result['status'],error=result['error']);return 2
    finally:
        if cpu is not None:cpu.close()
        if gpu is not None:gpu.close()
        if pool is not None:pool.terminate();pool.join()

def main():
    if sys.flags.optimize:raise SystemExit('Run exact checks without python -O')
    if len(sys.argv)==3 and sys.argv[1]=='--worker':return worker(json.loads(Path(sys.argv[2]).read_text()))
    import scaling
    scaling.WORKERS=(WORKERS,);scaling.REPEATS=REPEATS;scaling.WALL_LIMIT=600
    scaling.NEW_FILES=(*scaling.NEW_FILES,'packing_benchmark.py','packing_opt.py','tests/test_packing.py')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wait',action='store_true')
    parser.add_argument('--host-only',action='store_true')
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args();args.worker_entry='packing_benchmark.py';args.run_group='packing-runs';args.packing='paired'
    try:return scaling.coordinator(args)
    except (RuntimeError,TimeoutError,subprocess.TimeoutExpired) as error:
        print(json.dumps(dict(status='deferred',error=str(error),automatic_resume=False),indent=2));return 3

if __name__=='__main__':raise SystemExit(main())
