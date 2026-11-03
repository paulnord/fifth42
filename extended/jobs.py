#!/usr/bin/env python3
"""Launch an approved bounded search in an independent session with durable logs."""
import argparse
from datetime import datetime,timezone
import fcntl
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

import run
from check_idle import ensure_idle

ROOT=Path(__file__).resolve().parent

def ticks(pid):
    try:return Path(f'/proc/{pid}/stat').read_text().split(') ',1)[1].split()[19]
    except (OSError,IndexError):return None

def alive(pid,stamp):
    try:state=Path(f'/proc/{pid}/stat').read_text().split(') ',1)[1].split()[0]
    except (OSError,IndexError):return False
    return state!='Z' and stamp is not None and ticks(pid)==stamp

def descendants(parent):
    """Identify only this runner's descendants, including separate engine sessions."""
    parents={}
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            fields=path.read_text().split(') ',1)[1].split()
            parents[int(path.parent.name)]=(int(fields[1]),fields[19])
        except (OSError,ValueError,IndexError):continue
    found={};todo=[parent]
    while todo:
        p=todo.pop()
        for pid,(ppid,stamp) in parents.items():
            if ppid==p and pid not in found:found[pid]=stamp;todo.append(pid)
    return found

def terminate(child,known):
    known.update(descendants(child.pid))
    if child.poll() is None:child.send_signal(signal.SIGTERM)
    try:code=child.wait(timeout=10)
    except subprocess.TimeoutExpired:
        known.update(descendants(child.pid));child.kill();code=child.wait()
    # A crashed/unresponsive runner may leave its engine in another OS session.
    # PID start times prevent a stale entry from targeting a reused process ID.
    for pid,stamp in known.items():
        if alive(pid,stamp):
            try:os.kill(pid,signal.SIGKILL)
            except ProcessLookupError:pass
    return code

def launch(directory,command,seconds,run_directory):
    """Generic launcher; CLI below supplies only the validated search command."""
    directory=Path(directory).resolve()
    directory.mkdir(parents=True,exist_ok=False)
    config={'created_utc':run.now(),'command':command,'wall_seconds':seconds,
            'run_directory':str(Path(run_directory).resolve()),'cwd':str(ROOT)}
    run.atomic_json(directory/'config.json',config)
    with (directory/'search.log').open('ab') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'_worker',str(directory)],
                           cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,
                           start_new_session=True,close_fds=True)
    info={'worker_pid':p.pid,'worker_start_ticks':ticks(p.pid),'job':str(directory),
          'log':str(directory/'search.log'),'pid_namespace':os.readlink('/proc/self/ns/pid')}
    run.atomic_json(directory/'launcher.json',info)
    # Reap if this launching process stays alive; a daemon thread never keeps
    # the launching terminal/process alive and does not own the detached job.
    threading.Thread(target=p.wait,daemon=True).start()
    return info

def worker(directory):
    directory=Path(directory)
    config=json.loads((directory/'config.json').read_text())
    signal.signal(signal.SIGHUP,signal.SIG_IGN)
    stopped=False
    child=None
    known_children={}
    def stop(signum,frame):
        nonlocal stopped
        stopped=True
        if child is not None and child.poll() is None:
            known_children.update(descendants(child.pid));child.send_signal(signal.SIGTERM)
    signal.signal(signal.SIGTERM,stop)
    signal.signal(signal.SIGINT,stop)
    info={'worker_pid':os.getpid(),'worker_start_ticks':ticks(os.getpid()),
          'status':'starting','started_utc':run.now(),'wall_seconds':config['wall_seconds']}
    run.atomic_json(directory/'job.json',info)
    reason='finished'
    try:
        with (ROOT/'runs/.gpu-job.lock').open('a') as lease:
            try:fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise RuntimeError('Another detached extended job owns the GPU lease') from None
            if stopped:raise RuntimeError('Stopped before engine launch')
            child=subprocess.Popen(config['command'],cwd=config['cwd'],stdin=subprocess.DEVNULL)
            info.update(status='running',runner_pid=child.pid,runner_start_ticks=ticks(child.pid))
            run.atomic_json(directory/'job.json',info)
            print(json.dumps({'event':'started',**info}),flush=True)
            try:code=child.wait(timeout=config['wall_seconds'])
            except subprocess.TimeoutExpired:
                reason='time_budget_exhausted'
                code=terminate(child,known_children)
            if stopped:reason='stopped_by_user'
            for pid,stamp in known_children.items():
                if alive(pid,stamp):
                    try:os.kill(pid,signal.SIGKILL)
                    except ProcessLookupError:pass
            state_path=Path(config['run_directory'])/'state.json'
            complete=False
            if state_path.exists():
                state=json.loads(state_path.read_text());run.coverage(state)
                complete=state['next_row']==state['total_rows']
                info.update(rows_committed=state['next_row'],total_rows=state['total_rows'],
                            verified_candidates=sum(len(c['hits']) for c in state['chunks']))
            info.update(status='complete' if complete else 'partial' if state_path.exists() and code==0 else 'failed',
                        exit_code=code,reason=reason,finished_utc=run.now())
    except BaseException as e:
        if child is not None and child.poll() is None:
            terminate(child,known_children)
        info.update(status='failed',error=str(e),finished_utc=run.now())
    run.atomic_json(directory/'job.json',info)
    print(json.dumps({'event':'ended',**info}),flush=True)

def status(directory):
    directory=Path(directory).resolve()
    config=json.loads((directory/'config.json').read_text())
    p=directory/'job.json'
    r=json.loads(p.read_text()) if p.exists() else {'status':'starting'}
    l=json.loads((directory/'launcher.json').read_text())
    r['worker_alive']=(alive(l['worker_pid'],l['worker_start_ticks'])
                       if l.get('pid_namespace')==os.readlink('/proc/self/ns/pid') else None)
    r['log']=str(directory/'search.log')
    checkpoint=Path(config['run_directory'])/'state.json'
    if checkpoint.exists():
        s=json.loads(checkpoint.read_text());run.coverage(s)
        r.update(rows_committed=s['next_row'],total_rows=s['total_rows'],
                 percent=round(100*s['next_row']/s['total_rows'],3),
                 complete=s['next_row']==s['total_rows'],
                 verified_candidates=sum(len(c['hits']) for c in s['chunks']))
    return r

def main():
    if len(sys.argv)==3 and sys.argv[1]=='_worker':
        worker(Path(sys.argv[2]));return
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='action',required=True)
    start=sub.add_parser('start')
    start.add_argument('--bound',type=int,required=True)
    start.add_argument('--hours',type=float,required=True)
    start.add_argument('--approve',action='store_true',help='Explicitly approve these bounds and resources')
    start.add_argument('--resume-run',type=Path,help='Resume an existing compatible checkpoint; no automatic retries')
    for parser in (start,sub.add_parser('status'),sub.add_parser('stop')):
        parser.add_argument('--job',type=Path,required=True)
    args=ap.parse_args()
    if args.action=='status':print(json.dumps(status(args.job),indent=2));return
    if args.action=='stop':
        l=json.loads((args.job/'launcher.json').read_text())
        if l.get('pid_namespace')!=os.readlink('/proc/self/ns/pid'):
            raise ValueError('Use a normal Ada terminal in the job process namespace to stop it')
        if not alive(l['worker_pid'],l['worker_start_ticks']):raise ValueError('Worker is no longer active; no signal sent')
        os.kill(l['worker_pid'],signal.SIGTERM)
        print('Stop requested; last committed coverage will be retained.');return
    if not args.approve:raise ValueError('Review bounds, time and resources, then supply --approve')
    if not 0<args.hours<=24 or not 0<=args.bound<=run.MAX_BOUND:raise ValueError('Invalid time or bound')
    if os.uname().nodename!='ada':raise ValueError('This launch is authorized only on ada')
    ensure_idle()
    run.gpu_gate()
    calibration=json.loads((ROOT/'runs/calibration.json').read_text())
    if not calibration.get('complete') or calibration.get('fingerprint')!=run.fingerprint('gpu'):
        raise ValueError('Run python3 calibrate.py first for these exact binaries')
    projected=calibration['rough_projected_70million_seconds']*(args.bound/70_000_000)**2
    if projected>args.hours*3600*.9:
        suggested=int(args.bound*math.sqrt(args.hours*3600*.85/projected)//1_000_000)*1_000_000
        raise ValueError(f'Calibration projects {projected/3600:.2f} hours; review a bound around {suggested:,} or a different budget before launch')
    if args.job.exists():raise ValueError('Job directory already exists; choose a new attempt directory')
    seconds=args.hours*3600
    if seconds<120:raise ValueError('Detached search budget must be at least two minutes')
    directory=args.resume_run.resolve() if args.resume_run else args.job.resolve()/'coverage'
    action='resume' if args.resume_run else 'new'
    cmd=[sys.executable,str(ROOT/'run.py'),action,'--run',str(directory),
         '--max-seconds',str(seconds-60),'--approved-long']
    if args.resume_run:
        s=json.loads((directory/'state.json').read_text());run.coverage(s)
        if s['config']['bound']!=args.bound or s['fingerprint']!=run.fingerprint('gpu'):
            raise ValueError('Resume bound/source/binary mismatch')
    else:cmd.extend(['--backend','gpu','--bound',str(args.bound),'--chunk-rows','65536'])
    print(json.dumps(launch(args.job,cmd,seconds,directory),indent=2))

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:
        print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
