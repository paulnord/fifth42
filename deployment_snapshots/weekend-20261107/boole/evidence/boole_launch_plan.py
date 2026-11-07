"""Review-only launch plan; does not reserve ranges or start services."""
import json,sys,time,math
from pathlib import Path
PYTHON='/home/pnord/boole-results-20261107/venv312/bin/python'
WORKER=Path('/home/pnord/boole-production-validation-20261107/worker')
c=json.loads(Path(sys.argv[1]).read_text());remaining=math.floor(c['stop_epoch']-10-time.time())
if remaining<60:raise RuntimeError('Insufficient time before absolute deadline')
service=c['service_name'];timer=c['deadline_service_name'].removesuffix('.service')
commands={'timer':['systemd-run','--user','--unit='+timer,'--collect','--on-calendar=2026-11-09 14:59:50 UTC','--timer-property=AccuracySec=1s','--timer-property=RandomizedDelaySec=0','/usr/bin/systemctl','--user','stop',service],
'service':['systemd-run','--user','--unit='+service.removesuffix('.service'),'--collect','--service-type=exec','--property=Restart=no','--property=KillMode=mixed','--property=RuntimeMaxSec='+str(remaining),'--property=TimeoutStopSec=8','--property=Nice=19','--property=CPUAffinity=0-15','--property=UMask=0077','--setenv=OPENBLAS_NUM_THREADS=1','--setenv=OMP_NUM_THREADS=1',PYTHON,'-B','-u',str(WORKER/'boole_supervisor.py'),'--config',str(WORKER/'production-config.json')]}
print(json.dumps({'review_only':True,'production_claim_created':False,'publisher_ready':False,'commands':commands},indent=2))
