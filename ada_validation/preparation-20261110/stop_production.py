"""Persist stop intent before stopping the controller and current compute."""
import json,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent
def main():
 (R/'STOP_CONTROLLER').write_text('Explicit production stop intent\n')
 subprocess.run(['systemctl','--user','stop','ada-preparation-rotation-20261110.service'],check=True,timeout=20)
 for _ in range(2):
  p=R/'rotation-state.json'
  active=json.loads(p.read_bytes())['active'] if p.exists() else dict(worker=str(R/'worker'),service='ada-preparation-20261110.service')
  (Path(active['worker'])/'STOP').touch()
  subprocess.run(['systemctl','--user','stop',active['service']],check=True,timeout=15);time.sleep(.5)
if __name__=='__main__':main()
