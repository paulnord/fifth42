#!/usr/bin/env python3
"""Certified patch-width sweep followed by actual cold one-pass confirmation."""
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
WIDTHS=(2,4,8)
WORKERS=16
REPEATS=5

def rotated_widths(repeat):
    values=list(WIDTHS[repeat%len(WIDTHS):]+WIDTHS[:repeat%len(WIDTHS)])
    return list(reversed(values)) if repeat%2 else values

def worker(config):
    import scaling_core as core
    import packing_opt
    import benchmark as helpers
    from engine_session import EngineSession
    run=Path(config['run']);deadline=config['deadline_monotonic']
    selected=config['physical_cpus'][:WORKERS];host_only=config['host_only']
    source=ROOT/'lattice_prototype';core.initialize(source)
    result=dict(status='running',experiment='certified-width-sweep',workers=WORKERS,
        bounds=list(BOUNDS),widths=list(WIDTHS),repeats=REPEATS,packing='optimized',bits=48,
        fresh_geometry_every_timed_variant=True,host_only=host_only,cases=[],controls=[],orders=[],
        gpu_request_wall_seconds=0,domain='1 <= a <= b < c <= bound, abs(a^5+b^5-c^5) <= 42')
    context=multiprocessing.get_context('spawn');pool=cpu=gpu=None;identities={}
    def save():helpers.write_json(run/'results.json',result)
    def event(name,**data):
        with (run/'events.jsonl').open('a') as stream:stream.write(json.dumps(dict(event=name,**data))+'\n')
    def remaining(cap=120):
        left=deadline-time.monotonic()-8
        if left<1:raise TimeoutError('Width comparison wall allowance exhausted')
        return min(cap,left)
    def charge(seconds):
        result['gpu_request_wall_seconds']+=seconds
        if result['gpu_request_wall_seconds']>120:raise TimeoutError('GPU request allowance exhausted')
    def start_pool(warm):
        os.sched_setaffinity(0,set(selected));p=context.Pool(WORKERS,initializer=core.initialize,initargs=(source,selected))
        if warm:
            seen=set();began=time.monotonic()
            while len(seen)<WORKERS:
                seen.update(pid for pid,_ in p.map(core.worker_identity,range(WORKERS*2),1))
                if time.monotonic()-began>60:
                    p.terminate();p.join();raise TimeoutError('Worker warmup failed')
        return p
    def engine(backend):
        os.sched_setaffinity(0,{selected[0]} if backend=='cuda' else set(selected))
        command=[str(ROOT/'bin'/('scaling_gpu' if backend=='cuda' else 'scaling_cpu'))]
        if backend=='cpu':command+=['--threads',str(WORKERS)]
        session=EngineSession(command,'gpu' if backend=='cuda' else 'emulated',deadline)
        if backend=='cuda':charge(session.startup_seconds)
        os.sched_setaffinity(0,set(selected));return session
    def oracle(bound,cap):
        p=subprocess.run([str(ROOT/'bin/scaling_oracle'),str(bound),str(cap)],capture_output=True,text=True,timeout=remaining())
        if p.returncode:raise RuntimeError('Independent oracle failed: '+p.stderr)
        data=json.loads(p.stdout)
        if not data.get('complete') or (data['bound'],data['cap'])!=(bound,cap):raise RuntimeError('Oracle metadata mismatch')
        hits={tuple(h) for h in data['hits']}
        if any(not 1<=a<=b<c<=bound or a**5+b**5-c**5!=r or abs(r)>cap for a,b,c,r in hits):
            raise RuntimeError('Oracle exact hit mismatch')
        helpers.write_json(run/'oracles'/f'B{bound}-cap{cap}.json',data);return hits
    def prepare(p,bound,cap,width):
        start=time.perf_counter();specs,direct=core.specs(bound,cap,width)
        tasks=p.map(core.prepare_task,specs,32);preparation=time.perf_counter()-start
        start=time.perf_counter();tokens=p.map(core.certify_task,tasks,32);certification=time.perf_counter()-start
        start=time.perf_counter();plan=packing_opt.assemble(bound,cap,specs,direct,tasks,tokens);packing=time.perf_counter()-start
        identity=dict(certificate_sha256=plan.certificate_sha256,tasks=plan.tasks,points=plan.points,
            packets=[hashlib.sha256(batch.packet.encode()).hexdigest() for batch in plan.batches])
        key=(bound,cap,width)
        if key in identities and identities[key]!=identity:raise RuntimeError('Same-width certified geometry changed across repeats')
        identities[key]=identity
        return plan,dict(prepare_seconds=preparation,certificate_seconds=certification,packing_seconds=packing,
            total_preparation_seconds=preparation+certification+packing),identity
    def execute(session,plan,expected):
        rpc=verification=engine_time=kernel=0.;outputs=[];hits=set(plan.direct_hits)
        for batch in plan.batches:
            raw,wall=session.run(batch.packet,timeout=remaining())
            if session.backend=='gpu':charge(wall)
            rpc+=wall;start=time.perf_counter();hits|=core.decode_batch(batch,raw,session.backend)
            verification+=time.perf_counter()-start;engine_time+=raw['engine_seconds'];kernel+=raw['kernel_seconds'];outputs.append(raw)
        if hits!=expected:raise RuntimeError('Complete exact result differs from independent oracle')
        return dict(request_wall_seconds=rpc,output_verification_seconds=verification,engine_seconds=engine_time,
            kernel_seconds=kernel),outputs,hits
    def record(case,backend,repeat,plan,metrics,raw,hits):
        path=run/'trials'/f"{case['regime']}-B{case['bound']}-W{case['width']}-R{repeat+1}-{backend}.json"
        helpers.write_json(path,dict(bound=case['bound'],width=case['width'],backend=backend,repeat=repeat+1,
            regime=case['regime'],metrics=metrics,batches=raw,exact_hits=sorted(hits),oracle_equal=True,
            certificate_sha256=plan.certificate_sha256))
        case['samples'].setdefault(backend,[]).append(dict(repeat=repeat+1,**metrics,
            result_file=str(path.relative_to(run)),sha256=helpers.sha(path)));save()
    def summarize(case):
        if case.get('status')=='stopped_at_guard':return
        if any(len(rows)!=REPEATS for rows in case['samples'].values()):raise RuntimeError('Missing width repeat')
        case['medians']={backend:{key:statistics.median(row[key] for row in rows)
            for key in rows[0] if key.endswith('_seconds')} for backend,rows in case['samples'].items()}
        case.update(complete=True,status='passed');save()
        event('case_complete',regime=case['regime'],bound=case['bound'],width=case['width'],medians=case['medians'])
    try:
        pool=start_pool(True);cpu=engine('cpu')
        if not host_only:gpu=engine('cuda')
        for bound,cap in ((34,384),(100,2951)):
            expected=oracle(bound,cap)
            if not expected:raise RuntimeError('Empty nonempty control')
            for width in WIDTHS:
                plan,_,_=prepare(pool,bound,cap,width);execute(cpu,plan,expected)
                if gpu is not None:execute(gpu,plan,expected)
            result['controls'].append(dict(bound=bound,cap=cap,widths=list(WIDTHS),exact_hits=sorted(expected),passed=True))
            save();event('control_passed',bound=bound)
        expected_by_bound={bound:oracle(bound,42) for bound in BOUNDS}
        for bound in BOUNDS:
            cases={width:dict(regime='persistent_engines',host_workers=WORKERS,bound=bound,width=width,
                complete=False,status='running',samples={}) for width in WIDTHS}
            result['cases'].extend(cases.values());save()
            for repeat in range(REPEATS):
                order=rotated_widths(repeat);result['orders'].append(dict(bound=bound,repeat=repeat+1,widths=order))
                for width in order:
                    case=cases[width]
                    if case['status']=='stopped_at_guard':continue
                    remaining()
                    try:plan,timing,identity=prepare(pool,bound,42,width)
                    except ValueError as error:
                        if width==2 or str(error) not in ('Patch point allowance mismatch','Full-domain coefficient allowance exhausted',
                            'Single task cannot fit a packet','Integer transform can overflow'):raise
                        case.update(status='stopped_at_guard',error=str(error));save();event('width_guard',bound=bound,width=width,error=str(error));continue
                    case['identity']=identity
                    backends=[('cpu',cpu)]+([] if gpu is None else [('cuda',gpu)])
                    if repeat%2:backends.reverse()
                    for backend,session in backends:
                        metrics,raw,hits=execute(session,plan,expected_by_bound[bound]);metrics.update(timing)
                        metrics['end_to_end_seconds']=timing['total_preparation_seconds']+metrics['request_wall_seconds']+metrics['output_verification_seconds']
                        record(case,backend,repeat,plan,metrics,raw,hits)
                event('round_complete',bound=bound,repeat=repeat+1)
            for case in cases.values():summarize(case)
        candidates=[(case['medians'][backend]['end_to_end_seconds'],case['width'],backend)
            for case in result['cases'] if case['bound']==32000 and case['complete']
            for backend in case['medians']]
        seconds,width,backend=min(candidates)
        result['selection']=dict(bound=32000,width=width,backend=backend,
            persistent_end_to_end_seconds=seconds,rule='lowest complete 32000 persistent pipeline median',
            workers=WORKERS,packing='optimized',bits=48)
        warm_winners={2,width}
        for name in ('cpu','cuda'):
            choices=[row for row in candidates if row[2]==name]
            if choices:warm_winners.add(min(choices)[1])
        cpu.close();cpu=None
        if gpu is not None:gpu.close();gpu=None
        pool.close();pool.join();pool=None
        cold_cases={w:dict(regime='cold_one_pass',host_workers=WORKERS,bound=32000,width=w,
            complete=False,status='running',samples={}) for w in sorted(warm_winners)}
        result['cases'].extend(cold_cases.values());save();event('warm_selection',**result['selection'])
        for repeat in range(REPEATS):
            order=sorted(warm_winners,reverse=bool(repeat%2))
            for width in order:
                backends=['cpu']+([] if host_only else ['cuda'])
                if repeat%2:backends.reverse()
                for backend in backends:
                    remaining();start=time.perf_counter();cold_pool=session=None
                    try:
                        cold_pool=start_pool(False);session=engine(backend);startup=time.perf_counter()-start
                        plan,timing,identity=prepare(cold_pool,32000,42,width);cold_cases[width]['identity']=identity
                        metrics,raw,hits=execute(session,plan,expected_by_bound[32000]);metrics.update(timing)
                        shutdown=time.perf_counter();session.close();session=None;cold_pool.close();cold_pool.join();cold_pool=None
                        metrics.update(cold_startup_seconds=startup,shutdown_seconds=time.perf_counter()-shutdown,
                            cold_one_pass_seconds=time.perf_counter()-start)
                        record(cold_cases[width],backend,repeat,plan,metrics,raw,hits)
                    finally:
                        if session is not None:session.close()
                        if cold_pool is not None:cold_pool.terminate();cold_pool.join()
        for case in cold_cases.values():summarize(case)
        result.update(status='passed',all_exact_oracles_equal=True,
            guarded_cases=[dict(bound=c['bound'],width=c['width'],error=c['error']) for c in result['cases'] if c['status']=='stopped_at_guard'])
        save();helpers.write_json(run/'selection.json',result['selection']);event('finished',status='passed');return 0
    except BaseException as error:
        result.update(status='stopped_at_guard' if isinstance(error,(TimeoutError,subprocess.TimeoutExpired)) else 'failed',
            error=f'{type(error).__name__}: {error}',traceback=traceback.format_exc());save();event('finished',status=result['status'],error=result['error']);return 2
    finally:
        if cpu is not None:cpu.close()
        if gpu is not None:gpu.close()
        if pool is not None:pool.terminate();pool.join()

def main():
    if sys.flags.optimize:raise SystemExit('Exact checks require ordinary Python')
    if len(sys.argv)==3 and sys.argv[1]=='--worker':return worker(json.loads(Path(sys.argv[2]).read_text()))
    import scaling
    scaling.WORKERS=(WORKERS,);scaling.BOUNDS=BOUNDS;scaling.REPEATS=REPEATS;scaling.WALL_LIMIT=600
    scaling.NEW_FILES=(*scaling.NEW_FILES,'width_benchmark.py','tests/test_widths.py')
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ('wait','host-only','check-only'):parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args();args.worker_entry='width_benchmark.py';args.run_group='width-runs';args.packing='optimized'
    try:return scaling.coordinator(args)
    except (RuntimeError,TimeoutError,subprocess.TimeoutExpired) as error:
        print(json.dumps(dict(status='deferred',error=str(error),automatic_resume=False),indent=2));return 3

if __name__=='__main__':raise SystemExit(main())
