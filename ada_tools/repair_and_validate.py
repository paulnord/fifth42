#!/usr/bin/env python3
"""Install pinned wheels in the isolated venv, then run the bounded handoff."""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
PYTHON = ROOT / 'venv/bin/python'
SOURCE = Path('/home/pnord/fifth42-lattice-optimizations-91bb89b/lattice_prototype')

def blockers():
    problems=[]
    latest=Path('/home/pnord/four133-eight-hour/jobs/latest.json')
    if latest.is_file():
        job=Path(json.loads(latest.read_text())['job'])
        state=json.loads((job/'progress.json').read_text())
        if state.get('status') in ('starting','running') or state.get('active_workers'):
            problems.append('four133 active')
    fifth=Path('/home/pnord/fifth42')
    for p in fifth.glob('*/runs/*/job.json'):
        state=json.loads(p.read_text())
        if state.get('status') in ('starting','running','validating','searching','calibrating','stopping'):
            problems.append('production job active: '+str(p))
    for base in [fifth/'runs',fifth/'extended/runs',fifth/'optimization/runs',
                 Path('/home/pnord/four133-eight-hour/jobs')]:
        if not base.is_dir(): continue
        for p in base.rglob('*'):
            if not p.is_file() or 'lock' not in p.name.lower(): continue
            try:
                with p.open('rb') as stream:
                    fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    fcntl.flock(stream,fcntl.LOCK_UN)
            except BlockingIOError:
                problems.append('busy lock: '+str(p))
    if os.getloadavg()[0]>2:
        problems.append('one-minute load exceeds 2')
    return problems

def child_limits():
    os.nice(19)
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheelhouse',type=Path,help='Use only wheels already in this local directory')
    parser.add_argument('--check-only',action='store_true',help='Check dependencies; do not install or run tests')
    args=parser.parse_args()
    if args.wheelhouse and not args.wheelhouse.is_dir():
        parser.error('The wheel directory does not exist')
    busy=blockers()
    if busy:
        print('Deferred: '+', '.join(busy));return 3
    if args.check_only:
        return subprocess.call([sys.executable,str(ROOT/'run_bounded.py'),'--require-complete'],
                               env=dict(os.environ,LATTICE_DEPENDENCIES_CHECK_ONLY='1'))
    runs=ROOT/'dependency-repair-runs';runs.mkdir(exist_ok=True)
    out=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'),dir=runs))
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
             NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    command=[str(PYTHON),'-m','pip','install','--disable-pip-version-check','--no-input',
             '--only-binary=:all:','--retries','0','--timeout','10']
    if args.wheelhouse:
        command+=['--no-index','--find-links',str(args.wheelhouse.resolve())]
    else:
        command+=['--index-url','https://pypi.org/simple']
    for name in ['requirements-sympy.txt','requirements-fpylll.txt','compiled_experiment/requirements.txt']:
        command+=['-r',str(SOURCE/name)]
    record={'status':'installing','command':command,'environment':str(PYTHON.parent.parent),
            'started_utc':datetime.now(timezone.utc).isoformat(),'larger_search_started':False}
    (out/'report.json').write_text(json.dumps(record,indent=2)+'\n')
    process=None;started=time.monotonic();next_resource_check=started+2
    try:
        with (out/'pip-stdout.txt').open('x') as stdout,(out/'pip-stderr.txt').open('x') as stderr:
            process=subprocess.Popen(command,stdout=stdout,stderr=stderr,env=env,
                start_new_session=True,preexec_fn=child_limits)
            while process.poll() is None:
                if time.monotonic()-started>180:
                    raise TimeoutError('Dependency installation exceeded 180 seconds')
                if time.monotonic()>=next_resource_check:
                    busy=blockers()
                    if busy:raise RuntimeError('Production resumed: '+', '.join(busy))
                    next_resource_check=time.monotonic()+2
                time.sleep(0.5)
        record['pip_exit_code']=process.returncode
        if process.returncode:
            record['status']='dependency_install_failed'
            record['stderr']=(out/'pip-stderr.txt').read_text()
            print(record['stderr'],end='')
            return 3
        record['status']='dependencies_installed'
    except BaseException as error:
        record.update(status='stopped_or_failed',error=type(error).__name__+': '+str(error))
        return 3
    finally:
        if process is not None and process.poll() is None:
            os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL);process.wait()
        record['wall_seconds']=time.monotonic()-started
        (out/'report.json').write_text(json.dumps(record,indent=2)+'\n')
        print('Dependency report: '+str(out/'report.json'),flush=True)
    return subprocess.call([sys.executable,str(ROOT/'run_bounded.py'),'--require-complete'],env=env)

if __name__=='__main__':
    sys.exit(main())
