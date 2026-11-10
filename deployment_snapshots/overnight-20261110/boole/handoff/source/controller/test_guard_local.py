"""Actual Boole NFS admission and loss-of-lease tests for the supplied guard."""
from datetime import datetime,timezone
import copy,json,subprocess,sys,time,uuid
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent;stage=Path('/home/pnord/boole-delegated-20261109-00');W=stage/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import policy,suballocation_guard as guard,ada_export_store
from durable_mirror import atomic

def main():
 base=json.loads((W/'production-config.json').read_bytes());assert guard.check(base)['assignments']['ada'][1]==7000000000
 label='guard-'+uuid.uuid4().hex;parent=ada_export_store.Store(policy.TEST_LEDGER/label);child=ada_export_store.Store(parent.root/'suballocations/boole')
 c=dict(base);last=c['initial_patch']+1000000;deadline=time.time()+100
 original=parent.reserve('test-parent',3917103232,last,c['manifest_sha256'])
 g=dict(schema='fifth42-parent-suballocation-v1',TEST_ONLY=True,parent_ledger=str(parent.root),parent_job='test-parent',parent_claim_sha256=original['sha256'],parent_first=original['first'],parent_last=last,child_ledger=str(child.root),assignments=dict(ada=[4631300224,c['initial_patch']],boole=[c['initial_patch'],last]),stop_epoch=deadline,coverage_claimed=False)
 path=child.root/'GRANT.json';atomic(path,g)
 local=policy.LOCAL/'TEST_ONLY_boole_delegated_20261109'/label;local.mkdir(mode=0o700,parents=True)
 c.update(TEST_ONLY=True,run_id=label,output=str(local/'run'),replica_output=str(policy.BULK/'TEST_ONLY_boole_delegated_20261109'/label/'run'),ledger_root=str(child.root),ledger_job=label,ledger_device=child.device,range_end=last,stop_epoch=deadline,stop_local=datetime.fromtimestamp(deadline,timezone.utc).isoformat(),suballocation_grant_file=str(path),suballocation_grant_sha256=policy.digest(path),service_name=label+'.service',deadline_service_name=label+'-deadline.service')
 claim=child.reserve(label,c['initial_patch'],c['range_end'],c['manifest_sha256']);c['ledger_claim_sha256']=claim['sha256'];cfg=ROOT/'guard-test-config.json';atomic(cfg,c)
 p=subprocess.Popen([sys.executable,'-B','-u',str(stage/'test_coordinator.py'),'--grant',str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 results=[]
 def reject(name,change,message):
  changed=dict(c,**change)
  try:guard.check(changed)
  except RuntimeError as error:assert message in str(error),(name,str(error));results.append(dict(test=name,status='passed',error=str(error)))
  else:raise AssertionError(name+' did not fail closed')
 try:
  assert p.stdout.readline().strip()=='ready'
  assert policy.load_config(cfg)==c;results.append(dict(test='full_local_test_admission',status='passed'))
  reject('grant_digest',dict(suballocation_grant_sha256='0'*64),'grant changed')
  reject('interval_overflow',dict(range_end=c['range_end']+1),'escaped')
  reject('wrong_child',dict(ledger_root=str(parent.root)),'Wrong child ledger')
  reject('wrong_deadline',dict(stop_epoch=deadline-1),'changed delegated cutoff')
  with patch.object(guard.time,'time',return_value=time.time()+11):
   reject('stale_heartbeat',{},'heartbeat is stale')
  p.terminate();p.wait(timeout=5)
  reject('lost_parent_lease',{},'parent lease is absent')
 finally:
  if p.poll() is None:p.terminate();p.wait(timeout=5)
  p.stdout.close();p.stderr.close()
 report=dict(status='passed',TEST_ONLY=True,scientific_coverage=False,production_guard='Passed from Boole against live Ada coordinator, original parent lock, activation audit, READY and every claim boundary',tests=results,guard_sha256=policy.digest(W/'suballocation_guard.py'),manifest_sha256=base['manifest_sha256'])
 atomic(ROOT/'guard-validation.json',report);print(json.dumps(dict(status='passed',tests=len(results),cross_host_production_guard='passed')))
if __name__=='__main__':main()
