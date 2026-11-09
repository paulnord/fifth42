"""Inspect or launch the prepared weekend service and its independent stop timer."""
import argparse
from datetime import datetime,timezone
import fcntl
import json
import math
from pathlib import Path
import subprocess
import time

import policy

ROOT=Path(__file__).resolve().parent
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'


def commands(config,now=None):
    now=time.time() if now is None else now
    # Allow eight seconds for systemd's final group cleanup, plus timer precision.
    cleanup_epoch=config['stop_epoch']-10
    runtime=math.floor(cleanup_epoch-now)
    policy.require(runtime>=60,'Too little time remains before the fixed Monday deadline')
    stop=datetime.fromtimestamp(cleanup_epoch,timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    timer=['systemd-run','--user','--unit='+config['deadline_service_name'].removesuffix('.service'),
        '--collect','--service-type=oneshot','--on-calendar='+stop,
        '--timer-property=AccuracySec=1s','--timer-property=RandomizedDelaySec=0',
        '--timer-property=Persistent=no','/usr/bin/systemctl','--user','stop',config['service_name']]
    service=['systemd-run','--user','--unit='+config['service_name'].removesuffix('.service'),
        '--collect','--service-type=exec','--description=Sixteen-worker fifth-power weekend continuation',
        '--property=RuntimeMaxSec='+str(runtime),'--property=TimeoutStopSec=8s',
        '--property=KillMode=mixed','--property=Restart=no','--property=Nice=19',
        '--property=CPUAffinity=0-15','--property=UMask=0077','--working-directory='+str(ROOT),
        '--property=StandardOutput=append:'+str(ROOT/'service.stdout.log'),
        '--property=StandardError=append:'+str(ROOT/'service.stderr.log'),
        '--setenv=PYTHONDONTWRITEBYTECODE=1','--setenv=PYTHONUNBUFFERED=1',
        '--setenv=CUDA_VISIBLE_DEVICES=0',PYTHON,'-B','-u',str(ROOT/'search_supervisor.py'),
        '--config',str(ROOT/'config.json')]
    return dict(stop_local=config['stop_local'],cleanup_starts_utc=stop,
                runtime_max_seconds=runtime,timer=timer,service=service)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--launch',action='store_true',help='Start the reviewed service; default only checks readiness')
    args=parser.parse_args()
    with (ROOT/'launcher.lock').open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        config=policy.load_config(ROOT/'config.json')
        policy.require(not Path(config['output']).exists(),'Actual run already exists; prepare a fresh continuation')
        policy.require(not (ROOT/'launch.json').exists(),'A launch attempt is already recorded; inspect it before proceeding')
        report=json.loads((ROOT/'preparation-report.json').read_text())
        policy.require(report['status']=='ready','Preparation has not passed')
        policy.require(report['manifest_sha256']==config['manifest_sha256'] and
                       report['config_sha256']==policy.digest(ROOT/'config.json'),'Prepared configuration changed')
        subprocess.run([PYTHON,'-B',str(ROOT/'search_supervisor.py'),'--config',str(ROOT/'config.json'),
                        '--check-only'],check=True,timeout=60)
        plan=commands(config)
        if not args.launch:
            print(json.dumps(dict(status='ready_not_launched',**plan),indent=2));return 0
        record=dict(started_utc=policy.utc(),stop_local=config['stop_local'],
                    resume_cursor=config['initial_patch'],commands=[],status='launching')
        timer_name=config['deadline_service_name'].removesuffix('.service')+'.timer'
        timer_armed=False
        try:
            for kind in ('timer','service'):
                # Recalculate the relative runtime immediately before service creation.
                invocation=commands(config)[kind]
                result=subprocess.run(invocation,capture_output=True,text=True,timeout=20)
                record['commands'].append(dict(kind=kind,command=invocation,exit_code=result.returncode,
                                               stdout=result.stdout,stderr=result.stderr))
                result.check_returncode()
                if kind=='timer':
                    timer_armed=True
                    subprocess.run(['systemctl','--user','is-active','--quiet',timer_name],check=True,timeout=5)
            record['status']='service_started'
        except BaseException as exc:
            record.update(status='launch_failed',error=f'{type(exc).__name__}: {exc}')
            if timer_armed:
                # Stop only units created for this immutable, unique run.
                subprocess.run(['systemctl','--user','stop',config['service_name'],timer_name],
                               capture_output=True,timeout=15)
            raise
        finally:
            with (ROOT/'launch.json').open('x') as stream:
                json.dump(record,stream,indent=2);stream.write('\n')
        print(json.dumps(record,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
