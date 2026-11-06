#!/usr/bin/env python3
"""Fail-closed manual ADA gate. No auto-wait, restart, publication or remote access."""
import argparse, importlib.util, json, os, signal, subprocess, sys, time
from pathlib import Path
sys.dont_write_bytecode=True

def stop_group(child):
    # A successful/failed group leader can exit before its compiler/engine children.
    # Keep leases until the entire owned group is gone, not merely child.wait().
    def alive():
        try:os.killpg(child.pid,0);return True
        except ProcessLookupError:return False
    if alive():
        try:os.killpg(child.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        deadline=time.monotonic()+3
        while alive() and time.monotonic()<deadline:
            child.poll();time.sleep(.05)
        if alive():
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
    child.wait(timeout=3)

def finished_service(service):
    r=subprocess.run(['systemctl','--user','show',service,
        '--property=LoadState,ActiveState,SubState'],capture_output=True,text=True,timeout=5)
    state=dict(line.split('=',1) for line in r.stdout.splitlines() if '=' in line)
    if r.returncode or state.get('LoadState')!='loaded' or state.get('ActiveState')!='inactive' or state.get('SubState')!='dead':
        raise RuntimeError('Overnight service is not verifiably loaded/inactive/dead: '+json.dumps(state))
    r=subprocess.run(['ps','-eo','pid=,args='],capture_output=True,text=True,check=True,timeout=5)
    for line in r.stdout.splitlines():
        pid,_,args=line.strip().partition(' ')
        if pid==str(os.getpid()):continue
        if any(name in args for name in ['overnight_service.py','overnight_search.py','github_status.py']):
            raise RuntimeError('Search or final publisher process is still present: '+line.strip())

def main():
    def stop(signum,frame):raise RuntimeError('Guard stop signal received')
    signal.signal(signal.SIGTERM,stop)
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle',type=Path,required=True)
    p.add_argument('--service',default='fifth-lattice-overnight-20261105.service')
    p.add_argument('--seconds',type=int,default=180)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--check-only',action='store_true')
    p.add_argument('command',nargs=argparse.REMAINDER)
    a=p.parse_args()
    if not 1<=a.seconds<=600:p.error('seconds must be between 1 and 600')
    command=a.command[1:] if a.command[:1]==['--'] else a.command
    if not a.check_only and not command:p.error('Supply a bounded command after --')
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    report=dict(status='deferred',command=command,automatic_resume=False,remote_launch=False)
    handles=[];child=None;began=time.monotonic()
    try:
        finished_service(a.service)
        root=a.bundle.resolve()
        subprocess.run(['sha256sum','--status','-c','SHA256SUMS'],cwd=root,check=True,timeout=30)
        path=root/'fifth42-coordinator-20261105/lattice_gpu/benchmark.py'
        spec=importlib.util.spec_from_file_location('handoff_frozen_benchmark',path)
        helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
        guard=helpers.resources() # Current existing ADA resource guard; no copied replacement.
        busy=helpers.hardware_blockers()
        if busy:raise RuntimeError('; '.join(busy))
        handles,leased=helpers.acquire_leases(guard,False)
        finished_service(a.service);helpers.idle_gpu()
        report['held_leases']=[h.name for h in handles]
        report['gpu_identity']=subprocess.check_output(['nvidia-smi','--query-gpu=name,uuid,driver_version,compute_cap',
            '--format=csv,noheader'],text=True,timeout=5).strip()
        if a.check_only:
            report['status']='preflight_passed_leases_released';return 0
        report['status']='running';start=time.monotonic();os.nice(19)
        with (out/'stdout.txt').open('x') as stdout,(out/'stderr.txt').open('x') as stderr:
            child=subprocess.Popen(command,stdout=stdout,stderr=stderr,start_new_session=True,
                preexec_fn=guard.parent_death_signal,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',
                CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
                NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1'))
            while child.poll() is None:
                if time.monotonic()-start>=a.seconds:raise TimeoutError('Manual test wall budget reached')
                finished_service(a.service)
                busy=guard.blockers([path for path in guard.lock_paths() if path not in leased],True)
                if busy:raise RuntimeError('Yielding to production: '+', '.join(busy))
                time.sleep(.5)
        report['exit_code']=child.returncode
        if child.returncode:raise RuntimeError('Test command failed; inspect stdout.txt and stderr.txt')
        report['status']='passed';return 0
    except (Exception,KeyboardInterrupt) as error:
        report['error']=f'{type(error).__name__}: {error}'
        if report['status']=='running':report['status']='failed_or_interrupted'
        return 3
    finally:
        signal.signal(signal.SIGTERM,signal.SIG_IGN)
        signal.signal(signal.SIGINT,signal.SIG_IGN)
        cleanup_failed=False
        try:
            if child:stop_group(child)
        except Exception as error:
            cleanup_failed=True;report['status']='cleanup_failed'
            report['cleanup_error']=f'{type(error).__name__}: {error}'
        finally:
            for handle in handles:handle.close()
        report['wall_seconds']=time.monotonic()-began
        (out/'guard-report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
        if cleanup_failed:return 3

if __name__=='__main__':raise SystemExit(main())
