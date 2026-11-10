"""Stage a validated controller; --start-services explicitly installs and starts."""
from pathlib import Path
import argparse,hashlib,json,math,os,subprocess,time
import units as worker_units

R=Path(__file__).resolve().parent
PY='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python'
DEADLINE=1794438000
CONTROLLER='cabbage-extended-controller-20261109.service'
UNIT_DIR=Path('/home/pnord/.config/systemd/user')
PUBLISH_DIR=Path('/mnt/nfs_share/cabbage-extended-publishing-20261109')

def write(p,x):
 p=Path(p)
 if p.exists():p.unlink()
 p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def render_units():
 remaining=max(1,math.floor(DEADLINE+1800-time.time()))
 common=f'WorkingDirectory={R}\nUMask=0077\nNice=19\nEnvironment=PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1\nRestart=no\nRuntimeMaxSec={remaining}\n'
 timer='cabbage-extended-controller-20261109-deadline.timer';deadline=timer.replace('.timer','.service');collector='cabbage-extended-collector-20261109.service'
 files={CONTROLLER:f'[Unit]\nDescription=Cabbage authorized production through 11 November 17:00 Central\n[Service]\nType=exec\n{common}ExecStart={PY} -B -u {R}/controller.py\nKillMode=mixed\nTimeoutStopSec=960\nStandardOutput=append:{R}/controller.stdout.log\nStandardError=append:{R}/controller.stderr.log\n',
  deadline:f'[Unit]\nDescription=Independent overnight compute stop\n[Service]\nType=oneshot\nExecStart={PY} -B {R}/stop_controller.py\nTimeoutStartSec=1000\nRestart=no\n',
  timer:f'[Unit]\nDescription=Stop Cabbage before 11 November 17:00 Central\n[Timer]\nOnCalendar=2026-11-11 22:59:50 UTC\nAccuracySec=100ms\nRandomizedDelaySec=0\nPersistent=false\nUnit={deadline}\n',
  collector:f'[Unit]\nDescription=Cabbage overnight production collector\n[Service]\nType=exec\n{common}ExecStart={PY} -B -u {R}/collector.py\nKillMode=mixed\nTimeoutStopSec=3\nStandardOutput=append:{R}/collector.stdout.log\nStandardError=append:{R}/collector.stderr.log\n'}
 return files,timer,collector

def main(start_services=False,clear_stop_intent=False):
 assert json.loads((R/'evidence/runtime-validation.json').read_bytes())['status']=='passed'
 tested=json.loads((R/'evidence/controller-validation.json').read_bytes())
 assert tested['status']=='passed'
 for name in ['controller.py','test_controller.py','stop_controller.py','install_controller.py']:
  assert tested['files'][name]==sha(R/name),'Controller changed since regression tests: '+name
 settings=json.loads((R/'controller-settings.json').read_bytes()) if (R/'controller-settings.json').exists() else {}
 consumed=settings.get('pending_consumed',False)
 assert type(consumed) is bool,'pending_consumed must be boolean'
 retired=settings.get('retire_timers',[])
 assert isinstance(retired,list) and all(isinstance(name,str) and name.endswith('.timer') and not any(ch.isspace() for ch in name) and '/' not in name for name in retired),'retire_timers must name explicit timer units'
 roots=[R]
 if not consumed:
  pending=Path(json.loads((R/'pending-configuration.json').read_bytes())['config'])
  assert json.loads((pending.parent/'evidence/runtime-validation.json').read_bytes())['status']=='passed'
  roots.append(pending.parent)
 share=PUBLISH_DIR
 write(R/'collector-settings.json',dict(host='cabbage',output=str(share),stop_epoch=DEADLINE,active_configuration=str(R/'active-configuration.json'),controller_state=str(R/'controller-state.json')))
 names=['controller.py','release.py','units.py','seal_previous.py','parallel_audit.py','stop_controller.py','install_controller.py','test_controller.py','collector.py','collector-settings.json','production-config.json']
 for optional in ['pending-configuration.json','controller-settings.json']:
  if (R/optional).exists():names.append(optional)
 for root in roots:
  m=root/'worker/release-manifest.json';names += [str((m.parent/name).relative_to(R)) for name in json.loads(m.read_bytes())['files']]
  names += [str(p.relative_to(R)) for p in [root/'production-config.json',root/'worker/base-config.json',m]]
 files={name:sha(R/name) for name in sorted(set(names))}
 write(R/'controller-manifest.json',dict(status='frozen',deadline=DEADLINE,files=files))
 for name in files:(R/name).chmod(0o400 if not name.endswith(('scaling_gpu','gmp_reference')) else 0o500)
 (R/'controller-manifest.json').chmod(0o400)
 rendered,timer,collector=render_units();stage=R/'staged-systemd';stage.mkdir(exist_ok=True)
 for name,content in rendered.items():(stage/name).write_text(content)
 write(R/'evidence/controller-unit-files.json',rendered)
 if not start_services:
  print('Controller units staged. No services installed or started.');return 0
 assert time.time()<DEADLINE-10,'Production deadline already reached'
 current=worker_units.state(CONTROLLER)
 assert current.get('ActiveState')=='inactive' and current.get('MainPID')=='0','Prior controller must be inactive with MainPID=0'
 marker=R/'stop-request.json'
 prior_intent=marker.read_bytes() if marker.exists() else None
 assert prior_intent is None or clear_stop_intent,'Stop intent remains; explicit --clear-stop-intent required for authorized restart'
 for name in sorted(set(retired+[timer])):subprocess.run(['systemctl','--user','stop',name],check=True,timeout=20)
 d=UNIT_DIR;d.mkdir(parents=True,exist_ok=True)
 for name,content in rendered.items():(d/name).write_text(content)
 subprocess.run(['systemctl','--user','daemon-reload'],check=True)
 if prior_intent is not None:
  assert marker.read_bytes()==prior_intent,'A new stop request arrived during installation'
  marker.unlink();fd=os.open(R,os.O_RDONLY|os.O_DIRECTORY)
  try:os.fsync(fd)
  finally:os.close(fd)
 assert not marker.exists(),'A stop request arrived during installation'
 share.mkdir(mode=0o700,parents=True,exist_ok=True)
 subprocess.run(['systemctl','--user','start',timer],check=True)
 subprocess.run(['systemctl','--user','is-active',timer],check=True)
 subprocess.run(['systemctl','--user','start',collector],check=True)
 subprocess.run(['systemctl','--user','start',CONTROLLER],check=True)
 print('Controller, independent stop timer and collector started.');return 0

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--start-services',action='store_true');parser.add_argument('--clear-stop-intent',action='store_true');args=parser.parse_args()
 raise SystemExit(main(args.start_services,args.clear_stop_intent))
