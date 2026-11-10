"""Capture advancing production and replicas under the expanded frozen queue."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import controller

def capture(c):
 until=time.monotonic()+10;root=Path(c['replica_output'])
 while time.monotonic()<until:
  try:
   raw=(root/'checkpoint.json').read_bytes();cp=json.loads(raw);r=json.loads((root/'replica-state.json').read_bytes())
   if hashlib.sha256(raw).hexdigest()==r['checkpoint_sha256']:return cp,r
  except FileNotFoundError:pass
  time.sleep(.1)
 raise RuntimeError('No consistent verified replica checkpoint')
def main():
 plan=json.loads((ROOT/'production-plan.json').read_bytes());live=json.loads((ROOT/'PRODUCTION_STATUS.json').read_bytes());active=live['active'];spec=plan['stages'][active['index']];c=controller.load_stage(spec)
 controller.require(c['run_id']==active['run_id'] and controller.unit(c['service_name'])['ActiveState']=='active','Current production stage is not active')
 first,r=capture(c);until=time.monotonic()+100
 while time.monotonic()<until:
  cp,r=capture(c)
  if cp['next_patch']>first['next_patch']:break
  controller.require(controller.unit(c['service_name'])['ActiveState']=='active','Production stopped before next replica');time.sleep(2)
 else:raise TimeoutError('Verified replica did not advance')
 state=json.loads((Path(c['output'])/'status.json').read_bytes());sup=json.loads((Path(c['output']).parent/'supervisor.json').read_bytes())
 controller.require(state['status']=='running' and state['error'] is None and sup['error'] is None,'Active production is unhealthy')
 controller.require(not controller.free_lock(Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl'),'Current NFS owner is not held')
 controller.require(not controller.free_lock('/home/pnord/boole-production-validation-20261107/gpu-owner.lock'),'Current GPU lease is not held')
 names=[c['service_name'],c['deadline_service_name'].replace('.service','.timer'),c['run_id']+'-final-copy.service','boole-delegated-queue-20261109.service',c['run_id']+'-collector.service']
 units={n:controller.unit(n) for n in names};controller.require(all(v['ActiveState']=='active' for v in units.values()),'Compute, timer, copier, collector or new queue inactive')
 controller.require(len(plan['stages'])==70 and plan['stages'][:3]==json.loads(Path('/home/pnord/boole-overnight-controller-20261109/production-plan.json').read_bytes())['stages'],'Existing queue changed')
 report=dict(status='passed',queue_stages=70,additional_claims=67,additional_cells=4250000001,active_run=c['run_id'],active_interval=[c['initial_patch'],c['range_end']],local_cursor=state['next_patch'],replica_cursor=cp['next_patch'],observed_replica_advance=cp['next_patch']-first['next_patch'],replica_lag_seconds=time.time()-r['captured_epoch'],queue_plan_sha256=controller.sha(ROOT/'production-plan.json'),units=units,stop_local=c['stop_local'],source_sha256=controller.sha(__file__))
 controller.atomic(ROOT/'LIVE_VERIFICATION.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
