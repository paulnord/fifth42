#!/usr/bin/env python3
"""Paired prune/progression scaling at 32000 and 128000, one CPU and a 1200-second cap."""
from datetime import datetime, timezone
from pathlib import Path
import ctypes
import fcntl
import hashlib
import importlib.metadata
import itertools
import json
import os
import platform
import resource
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
import benchmark_ada as base

BOUNDS = [32000,128000]
REPEATS = 3
MAX_NODES = 500_000_000
MAX_PATCHES = 150_000

def worker(config):
    run,source = Path(config['run']),Path(config['scratch'])
    result = dict(status='running',bounds=BOUNDS,repeats=REPEATS,cases=[],controls=[],
                  max_nodes=MAX_NODES,max_patches=MAX_PATCHES,per_call_wall_guard_seconds=300)
    current = None
    def save():base.write_json(run/'scaling-results.json',result)
    def event(kind,**data):
        with (run/'events.jsonl').open('a') as stream:
            stream.write(json.dumps(dict(event=kind,**data))+'\n')
    def remaining(cap=300):
        seconds = config['deadline_monotonic']-time.monotonic()-10
        if seconds<1:raise TimeoutError('Overall deadline reached')
        return min(cap,seconds)
    try:
        t=time.perf_counter()
        sys.path[:0]=[str(source),str(source/'compiled_experiment')]
        from fractions import Fraction
        import lattice5 as live
        import modular_filters as live_filter
        import benchmark_mpq as exp
        import fpylll,gmpy2
        versions={name:importlib.metadata.version(name) for name in base.PINS}
        if versions!=base.PINS or sys.version_info[:2]!=(3,12):
            raise RuntimeError('Pinned environment mismatch')
        result['environment']=dict(python=sys.version,packages=versions,
            fplll=fpylll.config.version,gmp=gmpy2.mp_version(),
            mpfr=gmpy2.mpfr_version(),mpc=gmpy2.mpc_version())
        engines={kind:exp.engine(kind) for kind in ['fraction','mpq']}
        result['cold_import_and_engine_seconds']=time.perf_counter()-t
        for l,f in engines.values():
            l.reduce_basis([[l.Q(int(i==j)) for j in range(3)] for i in range(3)],'fpylll')
        def isolation():
            if live.Q is not Fraction or live_filter.Q is not Fraction or live_filter.l is not live:
                raise RuntimeError('Default modules changed')
        def lattice(bound,targets=None,kind='mpq',mode='prune'):
            l,f=engines[kind]
            kwargs=dict(mode=mode,backend='fpylll',max_nodes=MAX_NODES,
                        max_patches=MAX_PATCHES,max_seconds=remaining())
            wall,cpu=time.perf_counter(),time.process_time()
            d=f.signed42_filtered(bound,**kwargs) if targets is None else f.search_targets_positive(bound,targets,**kwargs)
            metrics=dict(pipeline_seconds=time.perf_counter()-wall,
                         cpu_seconds=time.process_time()-cpu,search_seconds=float(d['stats']['seconds']))
            if not d['complete']:raise RuntimeError('Incomplete lattice result')
            isolation()
            return exp.normalize(d),metrics
        def cpu(binary,bound,target=42,filtered=True,cap=120):
            command=[binary,'--bound',str(bound),'--target',str(target),
                     '--filter','mod11' if filtered and target==42 else 'none']
            before=resource.getrusage(resource.RUSAGE_CHILDREN);wall=time.perf_counter()
            p=subprocess.run(command,capture_output=True,text=True,timeout=remaining(cap),
                             preexec_fn=base.parent_death_signal)
            process_wall=time.perf_counter()-wall;after=resource.getrusage(resource.RUSAGE_CHILDREN)
            if p.returncode:raise RuntimeError('Exact CPU program failed: '+p.stderr)
            d=json.loads(p.stdout)
            if (d['bound']!=bound or d['target']!=target or d['row_start']!=0
                    or d['row_stop']!=d['total_rows']):raise RuntimeError('CPU coverage metadata mismatch')
            if any(any(abs(x)>bound for x in h) or sum(x**5 for x in h)!=target for h in d['hits']):
                raise RuntimeError('CPU exact residual or bound mismatch')
            metrics=dict(pipeline_seconds=d['setup_seconds']+d['search_seconds'],
                setup_seconds=d['setup_seconds'],search_seconds=d['search_seconds'],
                process_wall_seconds=process_wall,
                cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime)
            return d,metrics,command
        def canon(d):return {tuple(sorted(h)) for h in d['hits']}
        def comparable(d):
            d=json.loads(json.dumps(d));d['stats'].pop('seconds');d.pop('mode',None);return d
        # Nonempty controls independently check both arithmetic paths and both CPU binaries.
        for bound,targets in [(34,[12,384]),(100,[2951])]:
            expected=live.direct_positive(1,bound,lambda c:max(targets),lambda r,c:r in targets)
            if not expected:raise RuntimeError('Empty control oracle')
            controls=dict(bound=bound,targets=targets,positive_oracle=sorted(expected),lattice={})
            for kind in ['fraction','mpq']:
                d,m=lattice(bound,targets,kind)
                if set(map(tuple,d['hits']))!=expected:raise RuntimeError('Nonempty lattice control mismatch')
                controls['lattice'][kind]=d
            if comparable(controls['lattice']['fraction'])!=comparable(controls['lattice']['mpq']):
                raise RuntimeError('Control counters differ across arithmetic paths')
            for target in targets:
                oracle=live.signed_reference(bound,target)
                if not oracle:raise RuntimeError('Empty signed control oracle')
                for binary in [config['direct_binary'],config['oracle_binary']]:
                    d,m,cmd=cpu(binary,bound,target,False)
                    if canon(d)!=oracle:raise RuntimeError('Nonempty CPU control mismatch')
            for kind in ['fraction','mpq']:
                candidate,_=lattice(bound,targets,kind,mode='progression')
                if set(map(tuple,candidate['hits']))!=expected or comparable(candidate)!=comparable(controls['lattice'][kind]):
                    raise RuntimeError('Progression control result/counter mismatch')
            result['controls'].append(controls);save();event('controls_passed',bound=bound,targets=targets)

        def geometry_records(kind,bound):
            l,f=engines[kind];cmin=1
            while cmin<=bound:
                cmax=min(2*cmin-1,bound)
                if l.Q(42,cmin**5)<=l.Q(9049,50000):
                    count=max(1,l.ceil(l.Q(9*cmin,20)))
                    for i in range(count):
                        remaining()
                        p=l.make_patch(cmin,cmax,l.Q(9*i,10*count),l.Q(9*(i+1),10*count),42)
                        a=p.basis();b,u=l.reduce_basis(a,'fpylll');mu,norms=l.gram_schmidt(b)
                        yield exp.normalize([vars(p),a,b,u,mu,norms])
                cmin*=2
        # Check this independent implementation against Python on signed targets,
        # including zeros, negative values, repeated coordinates, and nonempty hits.
        oracle_controls = []
        for bound in (0, 1, 2, 10):
            for target in (-384, -42, -12, -3, -1, 0, 1, 3, 12, 42, 384):
                expected = live.signed_reference(bound, target)
                d, m, cmd = cpu(config['oracle_binary'], bound, target, False)
                if canon(d) != expected:
                    raise RuntimeError('Independent signed oracle control failed')
                oracle_controls.append(dict(bound=bound, target=target, hits=sorted(expected)))
        # Compare with each saved, unfiltered arbitrary-precision GMP oracle.
        archived = base.WORKSPACE/'scaling-runs/20261105T185107Z-db2av0ga'
        archive_report = json.loads((archived/'report.json').read_text())
        archive_checks = []
        for case in archive_report['results']['cases']:
            p = archived/case['oracle']['result_file']
            if base.sha(p) != case['oracle']['sha256']:
                raise RuntimeError('Archived GMP oracle hash mismatch')
            expected = canon(json.loads(p.read_text())['result'])
            d, m, cmd = cpu(config['oracle_binary'], case['bound'], filtered=False)
            if canon(d) != expected:
                raise RuntimeError('Independent oracle differs from archived GMP')
            archive_checks.append(dict(bound=case['bound'], archived_gmp_sha256=base.sha(p),
                                       oracle_equal=True, metrics=m))
        result['independent_oracle_controls'] = oracle_controls
        result['archived_gmp_oracle_crosschecks'] = archive_checks
        save();event('independent_oracle_verified', python_cases=len(oracle_controls),
                     archived_gmp_bounds=[c['bound'] for c in archive_checks])
        (run/'oracles').mkdir();(run/'trials').mkdir()
        for bound in BOUNDS:
            remaining()
            current=dict(bound=bound,target=42,complete=False,phase='independent_oracle',
                         samples={'mpq_prune':[],'mpq_progression':[]},orders=[])
            result['cases'].append(current);save();event('step_started',bound=bound)
            d,m,cmd=cpu(config['oracle_binary'],bound,filtered=False,cap=180)
            oracle=canon(d);path=run/'oracles'/f'B{bound}-signed-unfiltered.json'
            base.write_json(path,dict(command=cmd,result=d,metrics=m,complete=True))
            current['oracle']=dict(kind='independent exhaustive sorted signed native128 CPU, no modular filter',
                hits=sorted(oracle),result_file=str(path.relative_to(run)),sha256=base.sha(path),**m)
            current['phase']='geometry';save();event('oracle_passed',bound=bound,seconds=m['process_wall_seconds'])
            t=time.perf_counter();digest=hashlib.sha256();patches=0;sentinel=object()
            for a,b in itertools.zip_longest(geometry_records('fraction',bound),geometry_records('mpq',bound),fillvalue=sentinel):
                if a is sentinel or b is sentinel or a!=b:raise RuntimeError('Exact geometry differs')
                patches+=1
                if patches>MAX_PATCHES:raise RuntimeError('Geometry patch guard exceeded')
                digest.update(json.dumps(a,sort_keys=True).encode());digest.update(b'\n')
            current['geometry']=dict(exact_fraction_mpq_equal=True,patches=patches,
                sha256=digest.hexdigest(),serialization='one sorted normalized JSON record plus LF per patch',
                verification_seconds=time.perf_counter()-t)
            current['phase']='paired_repeats';save()
            for repeat in range(REPEATS):
                order=['mpq_prune','mpq_progression'] if repeat%2==0 else ['mpq_progression','mpq_prune']
                paired_results={}
                current['orders'].append(order)
                for variant in order:
                    d,m=lattice(bound,mode='prune' if variant=='mpq_prune' else 'progression')
                    hits=set(map(tuple,d['signed_hits']));paired_results[variant]=d
                    if hits!=oracle:raise RuntimeError('Independent exact oracle mismatch: '+variant)
                    rel=f'trials/B{bound}-repeat{repeat+1}-{variant}.json'
                    base.write_json(run/rel,dict(bound=bound,repeat=repeat+1,variant=variant,
                        metrics=m,oracle_equal=True,result=d))
                    current['samples'][variant].append(dict(repeat=repeat+1,**m,
                        oracle_equal=True,result_file=rel,result_sha256=base.sha(run/rel)))
                    save()
                if comparable(paired_results['mpq_prune'])!=comparable(paired_results['mpq_progression']):
                    raise RuntimeError('Prune/progression results or conservative counters differ')
                event('round_complete',bound=bound,repeat=repeat+1,
                      pipeline_seconds={v:current['samples'][v][-1]['pipeline_seconds'] for v in order})
            current['medians']={}
            for variant,samples in current['samples'].items():
                if len(samples)!=REPEATS:raise RuntimeError('Missing paired repeat')
                current['medians'][variant]={k:statistics.median(s[k] for s in samples)
                    for k in samples[0] if k.endswith('_seconds')}
            a,b=current['medians']['mpq_prune'],current['medians']['mpq_progression']
            current['prune_over_progression_pipeline']=a['pipeline_seconds']/b['pipeline_seconds']
            current['prune_over_progression_pipeline_recheck']=a['pipeline_seconds']/b['pipeline_seconds']
            current.update(complete=True,phase='complete',all_oracles_equal=True)
            save();event('step_complete',bound=bound,medians=current['medians'],
                         prune_over_progression_pipeline=current['prune_over_progression_pipeline'])
        isolation();result.update(status='passed',default_modules_preserved=True);save()
        event('finished',status='passed');return 0
    except BaseException as error:
        expected=isinstance(error,(TimeoutError,subprocess.TimeoutExpired)) or type(error).__name__=='BudgetExceeded'
        result.update(status='stopped_at_guard' if expected else 'failed',
                      error=type(error).__name__+': '+str(error),traceback=traceback.format_exc())
        save();event('finished',status=result['status'],error=result['error'])
        traceback.print_exc();return 2 if expected else 1

def coordinator():
    started=time.monotonic();deadline=started+1200
    os.nice(19);os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
             NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    locks=base.lock_paths()
    gpu_lock=Path('/home/pnord/fifth-lattice-gpu/validation.lock')
    if gpu_lock.is_file():locks.append(gpu_lock)
    busy=base.blockers(locks)
    if busy:print('Deferred: '+', '.join(busy));return 3
    lease=(base.WORKSPACE/'cpu-benchmark.lock').open('a+')
    try:fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:print('Another CPU benchmark is active');return 3
    expected=json.loads((base.WORKSPACE/'published-sha256.json').read_text())
    if base.package_hashes()!=expected:raise RuntimeError('Tested package changed')
    directory=base.WORKSPACE/'scaling-runs';directory.mkdir(exist_ok=True)
    run=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'),dir=directory))
    scratch=run/'scratch/lattice_prototype';scratch.parent.mkdir();shutil.copytree(base.SOURCE,scratch)
    (run/'code').mkdir()
    for p in [Path(__file__),Path(base.__file__),base.WORKSPACE/'signed_oracle.cpp']:shutil.copyfile(p,run/'code'/p.name)
    (run/'direct-source').mkdir();native_hashes={}
    for name in ['search_cpu.cpp','search_common.hpp','exact.hpp']:
        p=base.PRODUCTION/'src'/name;shutil.copyfile(p,run/'direct-source'/name);native_hashes[name]=base.sha(p)
    initial_status=subprocess.check_output(['git','-C',str(base.PRODUCTION),'status','--short','--branch'],text=True)
    report=dict(status='running',started_utc=datetime.now(timezone.utc).isoformat(),run=str(run),
        requested_bounds=BOUNDS,repeats=REPEATS,hard_wall_cap_seconds=1200,max_nodes=MAX_NODES,
        max_patches=MAX_PATCHES,per_lattice_call_guard_seconds=300,
        execution='one logical CPU, nice 19, native threads 1, 2 GiB/process',
        source_commit='91bb89b0ff49974e9458faf19015908e44b85cb8',
        native_source_commit=subprocess.check_output(['git','-C',str(base.PRODUCTION),'rev-parse','HEAD'],text=True).strip(),
        native_source_sha256=native_hashes,host=platform.node(),platform=platform.platform(),
        frozen_code_sha256={p.name:base.sha(p) for p in (run/'code').iterdir()},
        commands=[],gpu_execution=False,automatic_resume=False,
        oracle='independently written exact signed __int128 search, x<=y<=z, no modular filters; validated against Python and archived unfiltered GMP',
        timing_definition='warm GMP/fpylll preparation + search, paired prune versus progression; native CPU used only for controls',
        node_budget_note='Explicit finite allowances: 500 million nodes, 150000 patches; extended 300-second trial and 1200-second overall guards, fail-closed.')
    base.write_json(run/'report.json',report);print('RUN_DIRECTORY '+str(run),flush=True)
    offset=0
    def relay():
        nonlocal offset
        path=run/'events.jsonl'
        if not path.is_file():return
        with path.open() as stream:
            stream.seek(offset)
            while True:
                position=stream.tell();line=stream.readline()
                if not line:break
                if not line.endswith('\n'):stream.seek(position);break
                print('PROGRESS '+line.strip(),flush=True)
            offset=stream.tell()
    def execute(name,command,cap,worker_command=False):
        t=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN);p=None
        try:
            with (run/(name+'.stdout.txt')).open('x') as out,(run/(name+'.stderr.txt')).open('x') as err:
                p=subprocess.Popen(command,cwd=scratch,env=env,stdout=out,stderr=err,
                    start_new_session=True,preexec_fn=base.parent_death_signal)
                while p.poll() is None:
                    relay()
                    if (run/'STOP').exists():raise RuntimeError('User stop requested')
                    if time.monotonic()>=min(t+cap,deadline-5):raise TimeoutError('Extended 1200-second sweep budget reached')
                    busy=base.blockers(locks,True)
                    if busy:raise RuntimeError('Yielding to active work: '+', '.join(busy))
                    time.sleep(.25)
            relay();after=resource.getrusage(resource.RUSAGE_CHILDREN)
            row=dict(name=name,command=command,exit_code=p.returncode,
                     wall_seconds=time.monotonic()-t,
                     cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime)
            report['commands'].append(row);base.write_json(run/'report.json',report)
            if p.returncode and not(worker_command and p.returncode==2):raise RuntimeError(name+' failed')
            return p.returncode
        finally:
            if p is not None and p.poll() is None:
                os.killpg(p.pid,signal.SIGTERM)
                try:p.wait(timeout=2)
                except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    try:
        compiler='/usr/bin/g++-13';report['compiler']=subprocess.check_output([compiler,'--version'],text=True).splitlines()[0]
        native=run/'direct-native';oracle=run/'oracle-signed'
        flags=['-O3','-std=c++17','-Wall','-Wextra','-Wconversion']
        execute('compile-native',[compiler,*flags,str(run/'direct-source/search_cpu.cpp'),'-o',str(native)],30)
        execute('compile-oracle',[compiler,*flags,str(run/'code/signed_oracle.cpp'),'-o',str(oracle)],30)
        report['binary_sha256']={'native':base.sha(native),'oracle':base.sha(oracle)}
        (run/'pip-freeze.txt').write_text(subprocess.check_output([str(base.PYTHON),'-m','pip','freeze'],text=True,env=env))
        config=dict(run=str(run),scratch=str(scratch),direct_binary=str(native),oracle_binary=str(oracle),deadline_monotonic=deadline)
        base.write_json(run/'config.json',config)
        code=execute('scaling-worker',[str(base.PYTHON),str(run/'code/scaling_progression_ada.py'),'--worker',str(run/'config.json')],1190,True)
        report['status']='passed' if code==0 else 'stopped_at_guard'
    except BaseException as error:
        report.update(status='budget_stopped' if isinstance(error,TimeoutError) else 'failed_or_yielded',
                      error=type(error).__name__+': '+str(error))
        print(report['error'],flush=True)
    finally:
        path=run/'scaling-results.json'
        if path.is_file():report['results']=json.loads(path.read_text())
        report['elapsed_seconds']=time.monotonic()-started
        report['finished_utc']=datetime.now(timezone.utc).isoformat()
        report['published_package_unchanged']=base.package_hashes()==expected
        report['production_sources_unchanged']=all(base.sha(base.PRODUCTION/'src'/n)==h for n,h in native_hashes.items())
        report['production_status_unchanged']=subprocess.check_output(['git','-C',str(base.PRODUCTION),'status','--short','--branch'],text=True)==initial_status
        report['completed_bounds']=[c['bound'] for c in report.get('results',{}).get('cases',[]) if c.get('complete')]
        base.write_json(run/'report.json',report);lease.close()
        print('REPORT '+str(run/'report.json')+' STATUS '+report['status'],flush=True)
    return 0 if report['status']=='passed' else 2

if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Run exact benchmark/oracle checks without python -O')
    if len(sys.argv)==3 and sys.argv[1]=='--worker':raise SystemExit(worker(json.loads(Path(sys.argv[2]).read_text())))
    if len(sys.argv)!=1:raise SystemExit('Usage: scaling_progression_ada.py [--worker CONFIG]')
    raise SystemExit(coordinator())
