#!/usr/bin/env python3
"""Prepare and run finite CUDA validation only when ADA is free. Never a search launcher."""
import argparse,fcntl,hashlib,importlib.util,json,os,resource,shutil,signal,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REVIEW=Path('${CPU_BASELINE_WORKSPACE}')
CODEFILES=('model.py','check_devices.py','validate.py','Makefile','UPSTREAM.json','COVERAGE.md','README.md','src/kernel.hpp','src/io.hpp','src/emulated.cpp','src/enumerate.cu','vendor/exact.hpp','reference/lattice5.py','reference/COVERAGE.md','tests/test_model.py','tests/test_preflight.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blockers(in_progress=False):
    spec=importlib.util.spec_from_file_location('lattice_cpu_validation_guard',REVIEW/'reproduce_ada.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    reasons=module.resource_blockers(in_progress)
    if not Path('/dev/nvidia0').exists():reasons.append('CUDA device is not accessible in this session; use a normal ADA terminal')
    return reasons
def baseline():
    names={'healy-1000.json','reference-healy-1000.json','signed42-1000.json','focused-large-controls.json','upstream-comparison.json'}
    for p in sorted((REVIEW/'validation-runs').glob('*/report.json'),reverse=True):
        d=json.loads(p.read_text())
        if d.get('status')!='passed' or d.get('source_commit')!='ddf28f04725b29b2f1d53b5d33c16379b0f66a20':continue
        if not d.get('copied_outputs_removed') or set(d.get('verified_fresh_outputs',{}))!=names:continue
        scratch=Path(d['scratch'])
        if all(sha(scratch/'results'/name)==d['regenerated_result_comparisons'][name]['reproduced_sha256'] for name in names):return d
    return None
def low_priority():os.nice(19);os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
def main():
    p=argparse.ArgumentParser();p.add_argument('--check-only',action='store_true');a=p.parse_args()
    reasons=blockers()
    if reasons or a.check_only:
        report=dict(status='deferred' if reasons else 'ready_to_validate',checked_utc=datetime.now(timezone.utc).isoformat(),blockers=reasons,build_started=False,gpu_validation_started=False,automatic_resume=False)
        (ROOT/'preflight.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 3 if reasons else 0
    lock=(ROOT/'validation.lock').open('a+')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise RuntimeError('Another lattice GPU validator is active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');run=ROOT/'validation-runs'/stamp;work=run/'workspace';work.mkdir(parents=True)
    for name in CODEFILES:
        target=work/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
    manifest={name:sha(work/name) for name in CODEFILES};(run/'source-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    start=time.monotonic();records=[];active=None;report={};gpu_leases=[]
    def execute(label,cmd,cwd):
        nonlocal active
        reasons=blockers()
        if reasons:raise RuntimeError('Deferred: '+', '.join(reasons))
        before=resource.getrusage(resource.RUSAGE_CHILDREN);t=time.monotonic()
        with (run/(label+'.stdout.txt')).open('x') as out,(run/(label+'.stderr.txt')).open('x') as err:
            active=subprocess.Popen(cmd,cwd=cwd,stdout=out,stderr=err,start_new_session=True,preexec_fn=low_priority,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0'))
            while active.poll() is None:
                if time.monotonic()-start>600:raise TimeoutError('Overall 600-second validation cap')
                reasons=blockers(in_progress=True)
                if reasons:raise RuntimeError('Yielding to production: '+', '.join(reasons))
                time.sleep(.5)
        code=active.returncode;active=None;after=resource.getrusage(resource.RUSAGE_CHILDREN)
        records.append(dict(label=label,command=cmd,exit_code=code,wall_seconds=time.monotonic()-t,child_cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime))
        if code:raise RuntimeError(f'{label} failed; inspect its saved output')
    try:
        cpu=baseline()
        if cpu is None:
            execute('cpu-baseline',[sys.executable,str(REVIEW/'reproduce_ada.py')],REVIEW);cpu=baseline()
        if cpu is None:raise RuntimeError('No passing, freshly generated CPU baseline')
        (work/'CPU_BASELINE.json').write_text(json.dumps(cpu,indent=2)+'\n')
        execute('host-tests',[sys.executable,'-m','unittest','discover','-s','tests','-v'],work)
        execute('build',['make','-j1','all'],work)
        # Reuse the existing search/benchmark leases; acquiring is nonblocking.
        repo=Path('${PRODUCTION_CHECKOUT}')
        for path in (repo/'extended/runs/.gpu-job.lock',repo/'runs/gpu-B35000000/.lock',repo/'extended/runs/gpu-B70000000/coverage/.lock',repo/'filtered/runs/benchmark.lock'):
            if not path.exists():continue
            handle=path.open('a');gpu_leases.append(handle);fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
        # Only compute processes are queried; do not disturb an occupied GPU.
        smi=shutil.which('nvidia-smi')
        if smi:
            check=subprocess.run([smi,'--query-compute-apps=pid','--format=csv,noheader'],capture_output=True,text=True,timeout=5)
            if check.returncode or check.stdout.strip():raise RuntimeError('GPU occupancy could not be established as idle')
        execute('device-correctness',[sys.executable,'check_devices.py','--output',str(run/'device-results')],work)
        result=json.loads((run/'device-results/report.json').read_text())
        if result['status']!='passed':raise RuntimeError('Device comparisons are incomplete')
        report=dict(status='passed',gpu_validation_started=True,device_report=str(run/'device-results/report.json'),speedup_demonstrated=False)
    except BaseException as error:report=dict(status='failed_or_deferred',error=f'{type(error).__name__}: {error}',speedup_demonstrated=False)
    finally:
        if active is not None and active.poll() is None:
            os.killpg(active.pid,signal.SIGTERM)
            try:active.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(active.pid,signal.SIGKILL);active.wait()
        report.update(commands=records,total_wall_seconds=time.monotonic()-start,source_sha256=manifest,automatic_resume=False)
        (run/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));lock.close()
        for handle in gpu_leases:handle.close()
    return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
