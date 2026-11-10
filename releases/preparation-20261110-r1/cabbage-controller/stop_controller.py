"""Persist stop intent before stopping compute; verify final cleanup, never resume."""
from pathlib import Path
import json,subprocess,time
import controller

R=Path(__file__).resolve().parent
CONTROLLER='cabbage-extended-controller-20261109.service'
STOP_TIMEOUT=980

def main():
 # Close the rollover race before the worker stop becomes visible.
 controller.atomic(R/'stop-request.json',dict(requested_epoch=time.time(),reason='Independent stop interface'))
 until=time.monotonic()+STOP_TIMEOUT
 def remaining():
  seconds=until-time.monotonic()
  if seconds<=0:raise TimeoutError('Controller stop/final verification exceeded allowance')
  return seconds
 binding=R/'active-configuration.json';c=None;path=None
 if binding.exists():
  row=json.loads(binding.read_bytes());path=Path(row['config'])
  controller.require(controller.release.sha(path)==row['config_sha256'],'Active configuration changed')
  c=json.loads(path.read_bytes())
  subprocess.run(['systemctl','--user','stop',c['service_name']],check=True,timeout=min(20,remaining()))
 subprocess.run(['systemctl','--user','stop',CONTROLLER],check=True,timeout=remaining())
 if c:controller.wait_for_completion(c,path,timeout=remaining())
 return 0

if __name__=='__main__':raise SystemExit(main())
