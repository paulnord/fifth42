from pathlib import Path
import hashlib,json,math,subprocess,time
R=Path(__file__).resolve().parent;PY='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python';DEADLINE=1794351600
def write(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def main():
 assert json.loads((R/'evidence/runtime-validation.json').read_bytes())['status']=='passed'
 pending=Path(json.loads((R/'pending-configuration.json').read_bytes())['config'])
 assert json.loads((pending.parent/'evidence/runtime-validation.json').read_bytes())['status']=='passed'
 share=Path('/mnt/nfs_share/cabbage-extended-publishing-20261109');share.mkdir(mode=0o700,parents=True,exist_ok=True)
 write(R/'collector-settings.json',dict(host='cabbage',output=str(share),stop_epoch=DEADLINE,active_configuration=str(R/'active-configuration.json'),controller_state=str(R/'controller-state.json')))
 names=['controller.py','release.py','units.py','seal_previous.py','parallel_audit.py','stop_controller.py','collector.py','collector-settings.json','production-config.json','pending-configuration.json']
 for root in [R,pending.parent]:
  m=root/'worker/release-manifest.json';names += [str((m.parent/name).relative_to(R)) for name in json.loads(m.read_bytes())['files']]
  names += [str(p.relative_to(R)) for p in [root/'production-config.json',root/'worker/base-config.json',m]]
 files={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in sorted(set(names))}
 write(R/'controller-manifest.json',dict(status='frozen',deadline=DEADLINE,files=files))
 for name in files:(R/name).chmod(0o400 if not name.endswith(('scaling_gpu','gmp_reference')) else 0o500)
 (R/'controller-manifest.json').chmod(0o400)
 d=Path('/home/pnord/.config/systemd/user');remaining=math.floor(DEADLINE+1800-time.time())
 common=f'WorkingDirectory={R}\nUMask=0077\nNice=19\nEnvironment=PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1\nRestart=no\nRuntimeMaxSec={remaining}\n'
 controller='cabbage-extended-controller-20261109.service';timer='cabbage-extended-controller-20261109-deadline.timer';deadline=timer.replace('.timer','.service');collector='cabbage-extended-collector-20261109.service'
 units={controller:f'[Unit]\nDescription=Cabbage authorized production through 10 November 17:00 Central\n[Service]\nType=exec\n{common}ExecStart={PY} -B -u {R}/controller.py\nKillMode=mixed\nTimeoutStopSec=12\nStandardOutput=append:{R}/controller.stdout.log\nStandardError=append:{R}/controller.stderr.log\n',
  deadline:f'[Unit]\nDescription=Independent overnight compute stop\n[Service]\nType=oneshot\nExecStart={PY} -B {R}/stop_controller.py\nTimeoutStartSec=30\nRestart=no\n',
  timer:f'[Unit]\nDescription=Stop Cabbage before tomorrow 17:00 Central\n[Timer]\nOnCalendar=2026-11-10 22:59:50 UTC\nAccuracySec=100ms\nRandomizedDelaySec=0\nPersistent=false\nUnit={deadline}\n',
  collector:f'[Unit]\nDescription=Cabbage overnight production collector\n[Service]\nType=exec\n{common}ExecStart={PY} -B -u {R}/collector.py\nKillMode=mixed\nTimeoutStopSec=3\nStandardOutput=append:{R}/collector.stdout.log\nStandardError=append:{R}/collector.stderr.log\n'}
 for name,content in units.items():(d/name).write_text(content)
 write(R/'evidence/controller-unit-files.json',units)
 subprocess.run(['systemctl','--user','daemon-reload'],check=True)
 subprocess.run(['systemctl','--user','start',timer],check=True)
 subprocess.run(['systemctl','--user','is-active',timer],check=True)
 subprocess.run(['systemctl','--user','start',collector],check=True)
 subprocess.run(['systemctl','--user','start',controller],check=True)
 print('Controller, independent stop timer and collector started.')
if __name__=='__main__':main()
