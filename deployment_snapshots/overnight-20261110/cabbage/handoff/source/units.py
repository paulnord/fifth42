"""Create only this run's bounded user services and independent stop timer."""
from pathlib import Path
from datetime import datetime,timezone
import json,math,subprocess,time
R=Path(__file__).resolve().parent;W=R/'worker';PY='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python'
def call(*args):return subprocess.check_output(['systemctl','--user',*args],text=True,timeout=20)
def state(name):
 return dict(x.split('=',1) for x in call('show',name,'-p','ActiveState','-p','SubState','-p','MainPID','-p','Result','-p','ExecMainStatus').splitlines() if '=' in x)
def install(config_path):
 import hashlib
 config_path=Path(config_path).resolve();c=json.loads(config_path.read_bytes());R=Path(c['manifest']).parent.parent;W=R/'worker';d=Path('/home/pnord/.config/systemd/user');d.mkdir(parents=True,exist_ok=True)
 service=c['service_name'];deadline=c['deadline_service_name'];cleanup=c['cleanup_service_name'];timer=deadline.replace('.service','.timer')
 stop=datetime.fromtimestamp(c['stop_epoch']-10,timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
 common=f'WorkingDirectory={R}\nNice=19\nUMask=0077\nEnvironment=PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 SCALING_LATTICE_SOURCE={W}/source/lattice_prototype\nRestart=no\n'
 files={service:f'[Unit]\nDescription=Cabbage buffered continuation\n[Service]\nType=exec\n{common}ExecStart={PY} -B -u {W}/cabbage_supervisor.py --config {config_path}\nKillMode=mixed\nTimeoutStopSec=8\nRuntimeMaxSec={max(1,math.floor(c["stop_epoch"]-time.time()))}\nStandardOutput=append:{Path(c["output"]).parent}/service.stdout.log\nStandardError=append:{Path(c["output"]).parent}/service.stderr.log\n',
 deadline:f'[Unit]\nDescription=Stop only {service} before its absolute deadline\n[Service]\nType=oneshot\nExecStart=/usr/bin/systemctl --user stop {service}\nTimeoutStartSec=9\nRestart=no\n',
 timer:f'[Unit]\nDescription=Independent Cabbage deadline timer\n[Timer]\nOnCalendar={stop}\nAccuracySec=100ms\nRandomizedDelaySec=0\nPersistent=false\nUnit={deadline}\n',
 cleanup:f'[Unit]\nDescription=Finish verified Cabbage replica without resuming compute\n[Service]\nType=exec\n{common}ExecStart={PY} -B -u {W}/finalize_replica.py --config {config_path} --config-sha256 {hashlib.sha256(config_path.read_bytes()).hexdigest()} --wait\nKillMode=mixed\nTimeoutStopSec=3\nRuntimeMaxSec={max(1,math.floor(c["stop_epoch"]+1800-time.time()))}\nStandardOutput=append:{Path(c["output"]).parent}/final-copy.stdout.log\nStandardError=append:{Path(c["output"]).parent}/final-copy.stderr.log\n'}
 for name,content in files.items():(d/name).write_text(content)
 call('daemon-reload')
 return c,files
def start(config_path):
 c,files=install(config_path);call('start',c['cleanup_service_name']);call('start',c['deadline_service_name'].replace('.service','.timer'))
 assert state(c['cleanup_service_name'])['ActiveState']=='active'
 assert state(c['deadline_service_name'].replace('.service','.timer'))['ActiveState']=='active'
 call('start',c['service_name']);return c,files
