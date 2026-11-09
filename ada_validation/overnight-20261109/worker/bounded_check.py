"""Run a finite validation step with the weekend CPU budget and ordinary leases."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import time

import policy
import search_supervisor as guard

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('seconds',type=int)
    parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args()
    policy.require(args.name.replace('-','').isalnum() and 1<=args.seconds<=600,'Invalid finite validation allowance')
    command=args.command[1:] if args.command[:1]==['--'] else args.command
    policy.require(bool(command),'No validation command')
    config=policy.load_config(ROOT/'config.json')
    folder=ROOT/'steps'/args.name;folder.mkdir(parents=True,exist_ok=False)
    report=dict(status='deferred',command=command,seconds=args.seconds,automatic_resume=False)
    handles=[];child=None;began=time.monotonic()
    def stop(*_):raise RuntimeError('Bounded validation stop requested')
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    try:
        guard.service_and_process_checks(config)
        helpers=guard.module('weekend_validation_existing_benchmark',guard.FROZEN_BENCHMARK)
        resources=helpers.resources()
        policy.require(not helpers.hardware_blockers(),'CUDA hardware is unavailable')
        handles,leased=helpers.acquire_leases(resources,False)
        own=(ROOT/'coordinator.lock').open('a+');handles.append(own)
        fcntl.flock(own,fcntl.LOCK_EX|fcntl.LOCK_NB)
        guard.service_and_process_checks(config);helpers.idle_gpu()
        report.update(status='running',held_leases=[h.name for h in handles],running_load_limit=config['running_load_limit'])
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',
                 OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
                 NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1')
        os.nice(19)
        with (folder/'stdout.txt').open('x') as stdout,(folder/'stderr.txt').open('x') as stderr:
            child=subprocess.Popen(command,cwd=ROOT,stdout=stdout,stderr=stderr,env=env,
                                   start_new_session=True,preexec_fn=resources.parent_death_signal)
            while child.poll() is None:
                policy.require(time.monotonic()-began<args.seconds,'Bounded validation time exhausted')
                guard.service_and_process_checks(config)
                busy=guard.resource_blockers(resources,[p for p in resources.lock_paths() if p not in leased],config)
                policy.require(not busy,'Resource guard requested stop: '+', '.join(busy))
                guard.gpu_process_checks(child)
                time.sleep(.5)
        report['exit_code']=child.returncode
        policy.require(child.returncode==0,'Validation failed; inspect its captured output')
        report['status']='passed';return 0
    except BaseException as exc:
        report.update(status='failed',error=f'{type(exc).__name__}: {exc}');return 3
    finally:
        signal.signal(signal.SIGTERM,signal.SIG_IGN);signal.signal(signal.SIGINT,signal.SIG_IGN)
        try:
            if child:guard.stop_owned(child)
        finally:
            for handle in handles:handle.close()
            report.update(leases_released=True,wall_seconds=time.monotonic()-began,updated_utc=policy.utc())
            (folder/'guard-report.json').write_text(json.dumps(report,indent=2)+'\n')
            print(json.dumps(report,indent=2))


if __name__=='__main__':raise SystemExit(main())
