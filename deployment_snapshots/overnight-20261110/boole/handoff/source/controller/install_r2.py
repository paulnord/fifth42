"""Install the pinned replacement controller after local actual-GPU tests pass."""
import argparse,json,math,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import controller

def main():
 p=argparse.ArgumentParser();p.add_argument('--plan-sha256',required=True);a=p.parse_args();path=ROOT/'production-plan.json'
 controller.require(controller.sha(path)==a.plan_sha256,'Prepared queue changed')
 controller.atomic(ROOT/'INSTALL_STATUS.json',dict(status='waiting_for_local_gpu_validation',plan_sha256=a.plan_sha256))
 while True:
  if (ROOT/'LOCAL_VALIDATION_FAILURE.json').exists():raise RuntimeError('Local GPU validation failed; replacement queue not installed')
  proof=ROOT/'LOCAL_VALIDATION_STATUS.json'
  if proof.exists() and json.loads(proof.read_bytes())['status']=='passed':break
  controller.require(time.time()<1794351300,'Too late to install replacement queue');time.sleep(2)
 plan=json.loads(path.read_bytes());controller.require(len(plan['stages'])==70,'Wrong expanded queue size')
 for stage in plan['stages']:
  c=controller.load_stage(stage);validation=json.loads((Path(stage['root'])/'runtime-validation.json').read_bytes())
  controller.require(validation['status']=='passed' and validation['manifest_sha256']==stage['manifest_sha256'],'Stage validation does not match its source')
 # This affects only the old once-only controller, never the compute/final-copy units.
 if controller.unit('boole-overnight-queue-20261109.service')['ActiveState']!='inactive':
  subprocess.run(['systemctl','--user','stop','boole-overnight-queue-20261109.service'],check=True,timeout=15)
 controller.require(controller.unit('boole-overnight-queue-20261109.service')['ActiveState']=='inactive','Old controller still active')
 controller.require(controller.sha(path)==a.plan_sha256,'Expanded queue changed during admission')
 cmd=['systemd-run','--user','--unit=boole-delegated-queue-20261109','--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077',
 '--property=RuntimeMaxSec='+str(math.floor(1794353400-time.time())-2),'--property=StandardOutput=append:'+str(ROOT/'production.stdout'),'--property=StandardError=append:'+str(ROOT/'production.stderr'),sys.executable,'-B','-u',str(ROOT/'controller.py'),'--plan',str(path),'--plan-sha256',a.plan_sha256,'--adopt-first']
 result=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=15)
 controller.atomic(ROOT/'INSTALL_STATUS.json',dict(status='expanded_queue_started',plan_sha256=a.plan_sha256,stages=70,additional_claims=67,additional_reserved_cells=4250000001,compute_restarted=False,command=cmd,stderr=result.stderr))
 print(result.stderr,flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as error:controller.atomic(ROOT/'INSTALL_R2_FAILURE.json',dict(status='failed',error=repr(error)));raise
