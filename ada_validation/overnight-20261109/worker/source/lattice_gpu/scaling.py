#!/usr/bin/env python3
"""Bounded multicore preparation and persistent CPU/CUDA scaling tests."""
import argparse
from dataclasses import asdict
from datetime import datetime,timezone
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
import traceback

ROOT=Path(__file__).resolve().parent
GPU_ROOT=Path('/home/pnord/fifth-lattice-gpu')
CPU_ROOT=Path('/home/pnord/fifth-lattice-optimizations-ada-20261105')
PINNED_PYTHON=CPU_ROOT/'venv/bin/python'
BOUNDS=(8000,32000)
WORKERS=(1,2,4,8,16)
REPEATS=3
WALL_LIMIT=1200
GPU_LIMIT=120
NEW_FILES=('scaling.py','scaling_core.py','engine_session.py','scaling.mk','scaling_oracle.cpp',
    'src/stream_io.hpp','src/scaling_cpu.cpp','src/scaling_gpu.cu','tests/test_scaling.py',
    'packing_opt.py','tests/test_packing.py')

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module);return module

def physical_cpus():
    found={}
    for cpu in sorted(os.sched_getaffinity(0)):
        topology=Path('/sys/devices/system/cpu')/f'cpu{cpu}'/'topology'
        key=((topology/'physical_package_id').read_text().strip(),(topology/'core_id').read_text().strip())
        found.setdefault(key,cpu)
    return list(found.values())[:16]

def packing_assembler(mode):
    if mode=='baseline':
        import scaling_core
        return scaling_core.assemble
    if mode=='optimized':
        import packing_opt
        return packing_opt.assemble
    raise ValueError('Unknown packing mode')

def worker(config):
    import scaling_core as core
    from engine_session import EngineSession
    helpers=load('_scaling_helpers',ROOT/'benchmark.py')
    run=Path(config['run']);source=ROOT/'lattice_prototype';deadline=config['deadline_monotonic']
    cpus=config['physical_cpus'];host_only=config['host_only']
    core.initialize(source)
    packing_mode=config.get('packing_mode','optimized')
    assemble=packing_assembler(packing_mode)
    result=dict(status='running',bounds=list(BOUNDS),worker_counts=list(WORKERS),repeats=REPEATS,
        host_only=host_only,packing_mode=packing_mode,cases=[],controls=[],gpu_request_wall_seconds=0,
        domain='1 <= a <= b < c <= bound, abs(a^5+b^5-c^5) <= 42',
        preparation='isolated GMP mpq + fpylll; exact immutable task certificates',
        limits=dict(bound=core.MAX_BOUND,tasks_per_packet=core.MAX_TASKS,points_per_packet=core.MAX_POINTS,
            points_per_patch=core.MAX_PATCH_POINTS,total_tasks=core.MAX_TOTAL_TASKS,total_points=core.MAX_TOTAL_POINTS),
        cpu_gpu_comparator='same coefficient boxes; direct target42 CPU/GPU also measured separately')
    def save():helpers.write_json(run/'results.json',result)
    def event(name,**data):
        with (run/'events.jsonl').open('a') as stream:stream.write(json.dumps(dict(event=name,**data))+'\n')
    def left(cap=300):
        seconds=deadline-time.monotonic()-8
        if seconds<1:raise TimeoutError('1200-second scaling allowance exhausted')
        return min(cap,seconds)
    def charge_gpu(seconds):
        result['gpu_request_wall_seconds']+=seconds
        if result['gpu_request_wall_seconds']>GPU_LIMIT:raise TimeoutError('120-second GPU request/startup allowance exhausted')
    def oracle(bound,cap):
        command=[str(ROOT/'bin/scaling_oracle'),str(bound),str(cap)]
        p=subprocess.run(command,capture_output=True,text=True,timeout=left())
        if p.returncode:raise RuntimeError('Independent positive oracle failed: '+p.stderr)
        data=json.loads(p.stdout)
        if data.get('complete') is not True or data['bound']!=bound or data['cap']!=cap:
            raise RuntimeError('Independent oracle metadata mismatch')
        expected={tuple(h) for h in data['hits']}
        for a,b,c,r in expected:
            if not 1<=a<=b<c<=bound or a**5+b**5-c**5!=r or abs(r)>cap:
                raise RuntimeError('Independent oracle exact residual mismatch')
        helpers.write_json(run/'oracles'/f'B{bound}-cap{cap}.json',data)
        return expected
    def prepare(bound,cap,pool=None):
        start=time.perf_counter();specifications,direct=core.specs(bound,cap)
        tasks=list(map(core.prepare_task,specifications)) if pool is None else pool.map(core.prepare_task,specifications,32)
        preparation=time.perf_counter()-start
        start=time.perf_counter()
        tokens=list(map(core.certify_task,tasks)) if pool is None else pool.map(core.certify_task,tasks,32)
        certification=time.perf_counter()-start
        start=time.perf_counter();plan=assemble(bound,cap,specifications,direct,tasks,tokens)
        packing=time.perf_counter()-start
        return plan,dict(prepare_seconds=preparation,certificate_seconds=certification,
            packing_seconds=packing,total_preparation_seconds=preparation+certification+packing)
    def enumerate_plan(session,plan,preparation,cold):
        hits=set(plan.direct_hits);outputs=[];rpc=verify=engine=kernel=0.
        for batch in plan.batches:
            response,seconds=session.run(batch.packet,timeout=left())
            if session.backend=='gpu':charge_gpu(seconds)
            rpc+=seconds
            start=time.perf_counter();hits|=core.decode_batch(batch,response,session.backend)
            verify+=time.perf_counter()-start
            engine+=response['engine_seconds'];kernel+=response['kernel_seconds'];outputs.append(response)
        metrics=dict(engine_seconds=engine,kernel_seconds=kernel,request_wall_seconds=rpc,
            output_verification_seconds=verify,cached_packet_seconds=rpc+verify,
            end_to_end_seconds=preparation+rpc+verify,cold_end_to_end_seconds=cold+preparation+rpc+verify)
        return hits,metrics,outputs
    def signed_hits(hits):
        return set(core.lattice().signed_reference(2,42))|{
            tuple(sorted((a,b,-c) if r==42 else (-a,-b,c))) for a,b,c,r in hits if abs(r)==42}
    def direct(bound,threads,expected,gpu=False,target=42):
        binary=ROOT/'bin'/('direct_gpu' if gpu else 'direct_cpu')
        command=[str(binary),'--bound',str(bound),'--target',str(target),'--filter',
            'mod11' if target==42 else 'none','--row-filters','25,31,61' if target==42 else 'none',
            '--variant','highword']
        if not gpu:command+=['--threads',str(threads)]
        start=time.perf_counter();p=subprocess.run(command,capture_output=True,text=True,timeout=left(60))
        seconds=time.perf_counter()-start
        if gpu:charge_gpu(seconds)
        if p.returncode:raise RuntimeError('Direct comparator failed: '+p.stderr)
        data=json.loads(p.stdout)
        hits={tuple(sorted(h)) for h in data['hits']}
        if data['bound']!=bound or data['target']!=target or data['row_start']!=0 or data['row_stop']!=data['total_rows'] or hits!=expected:
            raise RuntimeError('Direct comparator domain or oracle mismatch')
        if any(any(abs(x)>bound for x in h) or sum(x**5 for x in h)!=target for h in hits):
            raise RuntimeError('Direct comparator exact residual mismatch')
        return data,dict(search_seconds=data['search_seconds'],setup_seconds=data['setup_seconds'],process_wall_seconds=seconds)

    gpu=None;pool=None;cpu=None
    try:
        os.sched_setaffinity(0,{cpus[0]})
        if not host_only:
            gpu=EngineSession([str(ROOT/'bin/scaling_gpu')],'gpu',deadline)
            charge_gpu(gpu.startup_seconds);result['gpu_startup_seconds']=gpu.startup_seconds
            # A failed request must not leak candidates/counts into its successor.
            with EngineSession([str(ROOT/'bin/scaling_gpu'),'--capacity','1'],'gpu',deadline) as limited:
                charge_gpu(limited.startup_seconds)
                identity='LATTICE_GPU_V1 0 18098 1\n0 1 10 10 10 10 1 0 0 0 1 0 0 0 1\n'
                bad,t=limited.run(identity);charge_gpu(t)
                if bad.get('box_complete') is not False:raise RuntimeError('GPU capacity guard failed')
                good,t=limited.run('LATTICE_GPU_V1 0 42 0\n');charge_gpu(t)
                if good.get('box_complete') is not True or good['points_visited'] or good['hits']:
                    raise RuntimeError('GPU request state was not reset after failure')
        with EngineSession([str(ROOT/'bin/scaling_cpu_sanitize'),'--threads','2'],'emulated',deadline) as checked:
            for bound,cap in ((34,384),(100,2951)):
                expected=oracle(bound,cap)
                if not expected:raise RuntimeError('Nonempty control is empty')
                plan,timing=prepare(bound,cap)
                hits,metrics,_=enumerate_plan(checked,plan,timing['total_preparation_seconds'],checked.startup_seconds)
                if hits!=expected:raise RuntimeError('Sanitized control mismatch')
                if gpu is not None:
                    hits,metrics,_=enumerate_plan(gpu,plan,timing['total_preparation_seconds'],gpu.startup_seconds)
                    if hits!=expected:raise RuntimeError('CUDA nonempty control mismatch')
                for target in (12,):
                    expected_signed=core.lattice().signed_reference(bound,target)
                    direct(bound,2,expected_signed,target=target)
                    if gpu is not None:direct(bound,2,expected_signed,gpu=True,target=target)
                result['controls'].append(dict(bound=bound,cap=cap,exact_hits=sorted(expected),passed=True))
                save();event('control_passed',bound=bound,cap=cap)
        expected_by_bound={bound:oracle(bound,42) for bound in BOUNDS}
        canonical={}
        context=multiprocessing.get_context('spawn')
        for count in WORKERS:
            if count>len(cpus):raise RuntimeError('Requested physical CPU count unavailable')
            selected=cpus[:count];os.sched_setaffinity(0,set(selected));left()
            start=time.perf_counter();pool=context.Pool(count,initializer=core.initialize,initargs=(source,selected))
            identities={}
            while len(identities)<count:
                for pid,affinity in pool.map(core.worker_identity,range(count*2),1):identities[pid]=affinity
                if time.perf_counter()-start>60:raise TimeoutError('CPU worker warmup did not complete')
            pool_startup=time.perf_counter()-start
            cpu=EngineSession([str(ROOT/'bin/scaling_cpu'),'--threads',str(count)],'emulated',deadline)
            for bound in BOUNDS:
                case=dict(host_workers=count,bound=bound,complete=False,phase='prepare',
                    pool_startup_seconds=pool_startup,cpu_engine_startup_seconds=cpu.startup_seconds,
                    worker_affinities={str(k):list(v) for k,v in identities.items()},
                    samples={'cpu':[]},direct_samples={'cpu':[]},orders=[])
                if gpu is not None:case['samples']['cuda']=[];case['direct_samples']['gpu']=[]
                result['cases'].append(case);save();event('case_started',workers=count,bound=bound)
                for repeat in range(REPEATS):
                    left();plan,timing=prepare(bound,42,pool)
                    if bound in canonical and canonical[bound]!=plan.certificate_sha256:
                        raise RuntimeError('Parallel preparation changed exact patch geometry')
                    canonical[bound]=plan.certificate_sha256
                    case.update(phase='paired_engines',tasks=plan.tasks,coefficient_points=plan.points,
                        batches=len(plan.batches),certificate_sha256=plan.certificate_sha256)
                    if repeat==0 and count==WORKERS[0]:
                        helpers.write_json(run/'plans'/f'B{bound}.json',asdict(plan))
                    order=['cpu','cuda'] if gpu is not None and repeat%2==0 else (['cuda','cpu'] if gpu is not None else ['cpu'])
                    case['orders'].append(order)
                    for name in order:
                        session=cpu if name=='cpu' else gpu
                        cold=pool_startup+session.startup_seconds
                        hits,metrics,raw=enumerate_plan(session,plan,timing['total_preparation_seconds'],cold)
                        if hits!=expected_by_bound[bound]:raise RuntimeError('Independent positive-domain oracle mismatch')
                        metrics.update(timing)
                        path=run/'trials'/f'W{count}-B{bound}-R{repeat+1}-{name}.json'
                        helpers.write_json(path,dict(workers=count,bound=bound,repeat=repeat+1,backend=name,
                            metrics=metrics,exact_hits=sorted(hits),oracle_equal=True,batches=raw))
                        case['samples'][name].append(dict(repeat=repeat+1,**metrics,result_file=str(path.relative_to(run)),sha256=helpers.sha(path)))
                    expected_signed=signed_hits(expected_by_bound[bound])
                    for name in case['direct_samples']:
                        data,metrics=direct(bound,count,expected_signed,gpu=name=='gpu')
                        path=run/'direct-trials'/f'W{count}-B{bound}-R{repeat+1}-{name}.json'
                        helpers.write_json(path,dict(command_result=data,metrics=metrics,oracle_equal=True))
                        case['direct_samples'][name].append(dict(repeat=repeat+1,**metrics,result_file=str(path.relative_to(run)),sha256=helpers.sha(path)))
                    save();event('round_complete',workers=count,bound=bound,repeat=repeat+1)
                case['medians']={name:{key:statistics.median(s[key] for s in rows) for key in rows[0] if key.endswith('_seconds')}
                    for name,rows in case['samples'].items()}
                case['direct_medians']={name:{key:statistics.median(s[key] for s in rows) for key in rows[0] if key.endswith('_seconds')}
                    for name,rows in case['direct_samples'].items()}
                case.update(complete=True,phase='complete');save()
                event('case_complete',workers=count,bound=bound,medians=case['medians'],direct_medians=case['direct_medians'])
            cpu.close();cpu=None;pool.close();pool.join();pool=None
        result['status']='passed';save();event('finished',status='passed');return 0
    except BaseException as error:
        result.update(status='stopped_at_guard' if isinstance(error,(TimeoutError,subprocess.TimeoutExpired)) else 'failed',
            error=f'{type(error).__name__}: {error}',traceback=traceback.format_exc())
        save();event('finished',status=result['status'],error=result['error']);return 2
    finally:
        if cpu is not None:cpu.close()
        if gpu is not None:gpu.close()
        if pool is not None:pool.terminate();pool.join()

def coordinator(args):
    helpers=load('_scaling_launch_helpers',GPU_ROOT/'benchmark.py');guard=helpers.resources()
    baseline=helpers.passing_validation()
    expected=json.loads((CPU_ROOT/'published-sha256.json').read_text())
    if guard.package_hashes()!=expected:raise RuntimeError('Pinned lattice package has changed')
    cpus=physical_cpus()
    if len(cpus)<16:raise RuntimeError('Scaling matrix requires 16 physical CPUs')
    hardware=[] if args.host_only else helpers.hardware_blockers()
    busy=guard.blockers(guard.lock_paths()+[CPU_ROOT/'cpu-benchmark.lock',GPU_ROOT/'validation.lock'])
    if args.check_only:
        print(json.dumps(dict(status='deferred' if hardware or busy else 'ready',blockers=hardware+busy,
            workers=list(WORKERS),bounds=list(BOUNDS),repeats=REPEATS,wall_limit_seconds=WALL_LIMIT,
            host_only=args.host_only,physical_cpus=cpus),indent=2));return 3 if hardware or busy else 0
    if hardware:raise RuntimeError('; '.join(hardware))
    handles,leased=helpers.acquire_leases(guard,args.wait)
    process=None
    try:
        if not args.host_only:helpers.idle_gpu()
        if shutil.disk_usage(GPU_ROOT).free<2*1024**3:raise RuntimeError('Less than 2 GiB artifact space available')
        os.nice(19);start=time.monotonic();deadline=start+WALL_LIMIT
        folder=GPU_ROOT/getattr(args,'run_group','scaling-runs');folder.mkdir(exist_ok=True)
        run=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'),dir=folder))
        work=run/'workspace';work.mkdir()
        names=list(dict.fromkeys([*baseline['source_sha256'],'benchmark.py',*NEW_FILES]))
        for name in names:
            destination=work/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(GPU_ROOT/name,destination)
        hashes={name:helpers.sha(work/name) for name in names}
        shutil.copytree(guard.SOURCE,work/'lattice_prototype')
        receipts=json.loads((guard.PRODUCTION/'cpu_parallel/runs/device-comparison.json').read_text())
        direct_sources={'cpu_parallel/bin/search_cpu':'direct_cpu','filtered/bin/search_gpu':'direct_gpu'}
        for relative,name in direct_sources.items():
            source=guard.PRODUCTION/relative
            if helpers.sha(source)!=receipts['fingerprint'][relative]:raise RuntimeError('Validated direct comparator changed: '+relative)
            (work/'bin').mkdir(exist_ok=True);shutil.copy2(source,work/'bin'/name)
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',
            MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1',CUDA_VISIBLE_DEVICES='0',
            ASAN_OPTIONS='detect_leaks=0',SCALING_LATTICE_SOURCE=str(work/'lattice_prototype'))
        report=dict(status='running',started_utc=datetime.now(timezone.utc).isoformat(),run=str(run),
            workers=list(WORKERS),bounds=list(BOUNDS),repeats=REPEATS,host_only=args.host_only,
            packing_mode=getattr(args,'packing','optimized'),
            hard_wall_limit_seconds=WALL_LIMIT,gpu_request_wall_limit_seconds=GPU_LIMIT,
            gpu_context_lifetime_limit_seconds=WALL_LIMIT,physical_cpus=cpus,
            source_sha256=hashes,baseline=baseline,lattice_package_sha256=expected,
            direct_binary_sha256={name:helpers.sha(work/'bin'/name) for name in direct_sources.values()},
            automatic_resume=False,commands=[],execution='up to 16 physical CPU cores, one GPU when enabled, nice 19, native threads 1')
        if not args.host_only:
            metadata=subprocess.run(['nvidia-smi','--query-gpu=name,driver_version,memory.total','--format=csv,noheader'],capture_output=True,text=True,timeout=5)
            if metadata.returncode:raise RuntimeError('GPU identity query failed')
            report['gpu_identity']=metadata.stdout.strip()
        helpers.write_json(run/'report.json',report);print('RUN_DIRECTORY '+str(run),flush=True)
        offset=0
        def relay():
            nonlocal offset
            path=run/'events.jsonl'
            if not path.exists():return
            with path.open() as stream:
                stream.seek(offset)
                while True:
                    position=stream.tell();line=stream.readline()
                    if not line:break
                    if not line.endswith('\n'):stream.seek(position);break
                    print('PROGRESS '+line.strip(),flush=True)
                offset=stream.tell()
        def execute(name,command):
            nonlocal process
            began=time.monotonic()
            with (run/(name+'.stdout.txt')).open('x') as output,(run/(name+'.stderr.txt')).open('x') as error:
                process=subprocess.Popen(command,cwd=work,env=env,stdout=output,stderr=error,
                    start_new_session=True,preexec_fn=guard.parent_death_signal)
                while process.poll() is None:
                    relay()
                    if (run/'STOP').exists():raise RuntimeError('User stop requested')
                    if time.monotonic()>deadline-4:raise TimeoutError(f'{WALL_LIMIT}-second scaling cap reached')
                    busy=guard.blockers([p for p in guard.lock_paths() if p not in leased],True)
                    busy=[x for x in busy if x!='CPU load exceeds idle threshold']
                    if os.getloadavg()[0]>len(cpus)+4:busy.append('CPU load exceeds the allocated scaling allowance')
                    if busy:raise RuntimeError('Yielding to production: '+', '.join(busy))
                    time.sleep(.25)
            relay();code=process.returncode;process=None
            report['commands'].append(dict(name=name,command=command,exit_code=code,wall_seconds=time.monotonic()-began))
            helpers.write_json(run/'report.json',report)
            if code:raise RuntimeError(name+' failed; inspect saved stderr and results')
        try:
            execute('build',['make','-f','scaling.mk','-j1','scaling-host' if args.host_only else 'scaling'])
            execute('host-tests',[str(PINNED_PYTHON),'-m','unittest','discover','-s','tests','-v'])
            report['binary_sha256']={p.name:helpers.sha(p) for p in (work/'bin').iterdir() if p.is_file()}
            config=dict(run=str(run),deadline_monotonic=deadline,physical_cpus=cpus,host_only=args.host_only,
                packing_mode=getattr(args,'packing','optimized'))
            helpers.write_json(run/'config.json',config)
            entry=getattr(args,'worker_entry','scaling.py')
            execute('scaling-worker',[str(PINNED_PYTHON),str(work/entry),'--worker',str(run/'config.json')])
            report['status']='passed'
        except BaseException as error:report.update(status='stopped_or_failed',error=f'{type(error).__name__}: {error}')
        finally:
            if process is not None and process.poll() is None:
                os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=2)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
            path=run/'results.json'
            if path.exists():report['results']=json.loads(path.read_text())
            report['elapsed_seconds']=time.monotonic()-start
            report['source_files_preserved']=all(helpers.sha(GPU_ROOT/name)==value for name,value in hashes.items())
            report['lattice_source_preserved']=guard.package_hashes()==expected
            report['direct_sources_preserved']=all(helpers.sha(guard.PRODUCTION/path)==report['direct_binary_sha256'][name] for path,name in direct_sources.items())
            if not all(report[k] for k in ('source_files_preserved','lattice_source_preserved','direct_sources_preserved')):report['status']='failed_source_identity'
            report['completed_cases']=[dict(workers=c['host_workers'],bound=c['bound']) for c in report.get('results',{}).get('cases',[]) if c['complete']]
            helpers.write_json(run/'report.json',report)
            print(json.dumps(dict(status=report['status'],report=str(run/'report.json'),completed_cases=report['completed_cases'],elapsed_seconds=report['elapsed_seconds']),indent=2))
        return 0 if report['status']=='passed' else 2
    finally:
        for handle in handles:handle.close()

def main():
    if sys.flags.optimize:raise SystemExit('Run exact scaling checks without python -O')
    if len(sys.argv)==3 and sys.argv[1]=='--worker':return worker(json.loads(Path(sys.argv[2]).read_text()))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wait',action='store_true',help='wait for the active benchmark/production leases')
    parser.add_argument('--host-only',action='store_true',help='run the multicore CPU matrix without GPU access')
    parser.add_argument('--packing',choices=('optimized','baseline'),default='optimized',
        help='certificate packing implementation (default: optimized; baseline preserves the previous implementation)')
    parser.add_argument('--check-only',action='store_true')
    try:return coordinator(parser.parse_args())
    except (RuntimeError,TimeoutError,subprocess.TimeoutExpired) as error:
        print(json.dumps(dict(status='deferred',error=str(error),automatic_resume=False),indent=2));return 3

if __name__=='__main__':raise SystemExit(main())
