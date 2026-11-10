"""Deadline-bounded service supervisor using ADA's unchanged resource helper."""
import argparse
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source/lattice_gpu'))
import overnight_search as night
import policy
import transition_resources

PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
FROZEN_BENCHMARK=Path('/home/pnord/fifth42-low64-review-20261106/handoff/bundle/fifth42-coordinator-20261105/lattice_gpu/benchmark.py')
OLD_SERVICE='fifth-lattice-overnight-20261105.service'


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def service_and_process_checks(config,require_own=False):
    command=['systemctl','--user','show',OLD_SERVICE,'--property=LoadState,ActiveState,SubState,MainPID']
    result=subprocess.run(command,capture_output=True,text=True,check=True,timeout=5)
    state=dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
    policy.require(state.get('LoadState') in ('loaded','not-found') and state.get('ActiveState')=='inactive' and
                   state.get('SubState')=='dead' and state.get('MainPID')=='0','Previous service is not inactive/dead')
    result=subprocess.run(['ps','-eo','pid=,args='],capture_output=True,text=True,check=True,timeout=5)
    for line in result.stdout.splitlines():
        if any(name in line for name in ('overnight_service.py','overnight_search.py','github_status.py')):
            raise RuntimeError('Previous search/publisher process present: '+line.strip())
    result=subprocess.run(['systemctl','--user','list-units','--type=service','--state=active,activating',
                           '--plain','--no-legend','fifth*'],capture_output=True,text=True,check=True,timeout=5)
    allowed={config['service_name'],config['deadline_service_name'],*config.get('allowed_maintenance_units',[])}
    for line in result.stdout.splitlines():
        if line.strip() and line.split()[0] not in allowed:
            raise RuntimeError('Another active fifth service: '+line.strip())
    if require_own:
        result=subprocess.run(['systemctl','--user','show',config['service_name'],'--property=MainPID',
                                '--value'],capture_output=True,text=True,check=True,timeout=5)
        policy.require(int(result.stdout.strip())==os.getpid(),'Supervisor must run in its declared user service')


def stop_owned(child,grace=5):
    # Give the sole journal owner a chance to finish a commit before stopping its group.
    if child.poll() is None:
        child.send_signal(signal.SIGTERM)
        until=time.monotonic()+grace
        while child.poll() is None and time.monotonic()<until:time.sleep(.05)
    try:os.killpg(child.pid,0)
    except ProcessLookupError:pass
    else:
        try:os.killpg(child.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        until=time.monotonic()+1
        while time.monotonic()<until:
            try:os.killpg(child.pid,0)
            except ProcessLookupError:break
            time.sleep(.05)
        else:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
    child.wait(timeout=3)


def gpu_process_checks(child):
    result=subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],
                          capture_output=True,text=True,check=True,timeout=5)
    for line in result.stdout.splitlines():
        if not line.strip():continue
        pid=int(line.strip())
        try:group=os.getpgid(pid)
        except ProcessLookupError:continue
        policy.require(group==child.pid,'Unrelated GPU process detected: '+str(pid))


def resource_blockers(resources,locks,config):
    # The owner requested 16 physical workers for this isolated weekend job.
    # Replace only the original four-load running CPU budget; retain every
    # production, lock and memory check from the existing helper.
    busy=resources.blockers(locks,True)
    busy=[reason for reason in busy if reason!='CPU load exceeds idle threshold']
    if os.getloadavg()[0]>config['running_load_limit']:
        busy.append('CPU load exceeds weekend running budget')
    return busy


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args();config=policy.load_config(args.config)
    stopping=False
    def request(*_):
        nonlocal stopping
        stopping=True
    signal.signal(signal.SIGTERM,request);signal.signal(signal.SIGINT,request)
    handles=[];child=None;phase='deferred';error=None;last_report=last_checks=0;soft_sent=None
    cleanup_failed=False
    report=dict(service=config['service_name'],stop_local=config['stop_local'],stop_epoch=config['stop_epoch'],
                pid=os.getpid(),config=str(args.config),config_sha256=policy.digest(args.config),automatic_resume=False,
                publication=False,parent_cursor=config['initial_patch'])

    def save(force=False):
        nonlocal last_report
        if not force and time.monotonic()-last_report<5:return
        report.update(status=phase,error=error,updated_utc=policy.utc(),worker_pid=child.pid if child else None,
                      load_average=os.getloadavg())
        night.atomic_json(ROOT/('supervisor-preflight.json' if args.check_only else 'supervisor-report.json'),report)
        last_report=time.monotonic()

    try:
        service_and_process_checks(config,not args.check_only)
        helpers=module('afternoon_existing_benchmark',FROZEN_BENCHMARK)
        resources=helpers.resources()
        busy=helpers.hardware_blockers();policy.require(not busy,'; '.join(busy))
        handles,leased=transition_resources.acquire(helpers,resources,config)
        own=(ROOT/'coordinator.lock').open('a+');handles.append(own)
        fcntl.flock(own,fcntl.LOCK_EX|fcntl.LOCK_NB)
        service_and_process_checks(config,not args.check_only);helpers.idle_gpu();policy.validate_parent(config)
        policy.require(shutil.disk_usage(Path(config['output']).parent).free>=config['journal_limit_bytes']+config['minimum_free_disk_bytes'],
                       'Not enough disk space for the full weekend journal budget and reserve')
        audit=json.loads((ROOT/'parent-audit.json').read_text())
        policy.require(audit['status']=='passed' and audit['uncommitted_trailing_bytes']==0 and
                       audit['committed_chain_sha256']==config['parent_journal_sha256'],'Parent prefix audit is not valid')
        parent_journal=Path(config['parent_run'])/'coverage.jsonl'
        parent_before=parent_journal.stat()
        policy.validate_archive(config)
        policy.require(config['parent_journal_raw_sha256']==audit['committed_raw_sha256'],
                       'Verified archive does not match the full parent audit')
        parent_identity=(parent_before.st_dev,parent_before.st_ino,parent_before.st_size,
                         parent_before.st_mtime_ns,parent_before.st_ctime_ns)
        parent_after=parent_journal.stat()
        policy.require(parent_identity==(parent_after.st_dev,parent_after.st_ino,parent_after.st_size,
                                         parent_after.st_mtime_ns,parent_after.st_ctime_ns),'Parent journal changed during verification')
        report.update(held_leases=[h.name for h in handles],resource_helper_sha256=policy.digest(resources.__file__),
                      running_load_limit=config['running_load_limit'],idle_load_limit=2,minimum_free_memory_gib=4)
        if args.check_only:
            phase='preflight_passed_leases_released';save(True);return 0
        environment=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',
                          OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
                          NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1')
        with (ROOT/'worker.stdout.log').open('x') as stdout,(ROOT/'worker.stderr.log').open('x') as stderr:
            child=subprocess.Popen([PYTHON,'-B','-u',str(ROOT/'packed_worker.py'),'--config',str(args.config)],
                 stdout=stdout,stderr=stderr,env=environment,start_new_session=True,
                 preexec_fn=resources.parent_death_signal)
            phase='running';save(True)
            while child.poll() is None:
                now=time.time()
                if stopping or now>=config['stop_epoch']-8:
                    if soft_sent is None:
                        child.send_signal(signal.SIGTERM);soft_sent=time.monotonic();phase='stopping';save(True)
                    elif time.monotonic()-soft_sent>5:
                        raise TimeoutError('Worker exceeded graceful stop allowance')
                if now>=config['stop_epoch']:raise TimeoutError('Absolute hard stop reached')
                if (ROOT/'STOP').exists():stopping=True
                service_and_process_checks(config)
                busy=resource_blockers(resources,[p for p in resources.lock_paths() if p not in leased],config)
                if busy:raise RuntimeError('Resource guard requested stop: '+', '.join(busy))
                if time.monotonic()-last_checks>=5:
                    gpu_process_checks(child);policy.validate_parent(config);policy.validate_ledger(config);last_checks=time.monotonic()
                    policy.require(policy.digest(args.config)==report['config_sha256'],'Immutable run configuration changed')
                    stat=parent_journal.stat()
                    policy.require(parent_identity==(stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns),
                                   'Original overnight journal changed while continuing')
                save();time.sleep(.5)
        report['worker_exit_code']=child.returncode
        if child.returncode:raise RuntimeError('Worker failed; inspect worker logs and committed prefix')
        phase='finished';save(True);return 0
    except BaseException as exc:
        error=f'{type(exc).__name__}: {exc}';phase='guard_stopped' if child else 'deferred'
        return 3
    finally:
        signal.signal(signal.SIGTERM,signal.SIG_IGN);signal.signal(signal.SIGINT,signal.SIG_IGN)
        try:
            if child:stop_owned(child)
        except BaseException as exc:
            cleanup_failed=True;phase='cleanup_failed';error=f'{error}; cleanup: {type(exc).__name__}: {exc}'
        finally:
            for handle in handles:handle.close()
        report['leases_released']=True;save(True)
        if cleanup_failed:return 3


if __name__=='__main__':sys.exit(main())
