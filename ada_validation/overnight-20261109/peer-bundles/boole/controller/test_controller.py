"""Two real finite service runs demonstrate verified-copy-gated rollover."""
from datetime import datetime,timezone
import importlib.util,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import controller

def main():
 label='rollover-r1';deadline=time.time()+180;stages=[]
 for letter in ('a','b'):
  stage=Path('/home/pnord/boole-extra-20261109-'+letter);w=stage/'worker'
  sys.path[:0]=[str(w),str(w/'source/lattice_gpu')]
  import ada_export_store,policy
  c=json.loads((w/'production-config.json').read_bytes());name='boole-extra-test-'+label+'-'+letter+'-20261109'
  local=policy.LOCAL/'TEST_ONLY_boole_extra_20261109'/name;local.mkdir(mode=0o700,parents=True,exist_ok=False)
  replica=policy.BULK/'TEST_ONLY_boole_extra_20261109'/name/'run'
  store=ada_export_store.Store(policy.TEST_LEDGER/label/letter)
  c.update(TEST_ONLY=True,run_id=name,output=str(local/'run'),replica_output=str(replica),ledger_root=str(store.root),ledger_job=label+'-'+letter,ledger_device=store.device,
   range_end=c['initial_patch']+17*256,gmp_audit_period=1,test_chunk_limit=17,stop_epoch=deadline,stop_local=datetime.fromtimestamp(deadline,timezone.utc).isoformat(),service_name=name+'.service',deadline_service_name=name+'-deadline.service')
  claim=store.reserve(c['ledger_job'],c['initial_patch'],c['range_end'],c['manifest_sha256']);c['ledger_claim_sha256']=claim['sha256']
  path=ROOT/('test-'+letter+'-config.json');controller.atomic(path,c)
  stages.append(dict(root=str(stage),config=str(path),config_sha256=controller.sha(path),manifest_sha256=c['manifest_sha256'],first=c['initial_patch'],last=c['range_end']))
 plan=dict(TEST_ONLY=True,automatic_resume=False,stop_epoch=deadline,stop_local=datetime.fromtimestamp(deadline,timezone.utc).isoformat(),stages=stages,status_file=str(ROOT/'test-rollover-status.json'),controller_sha256=controller.sha(ROOT/'controller.py'))
 path=ROOT/'test-plan.json';controller.atomic(path,plan)
 result=subprocess.run([sys.executable,'-B','-u',str(ROOT/'controller.py'),'--plan',str(path),'--plan-sha256',controller.sha(path)],capture_output=True,text=True,timeout=150)
 assert result.returncode==0,result.stdout+result.stderr
 report=json.loads((ROOT/'test-rollover-status.json').read_bytes())
 assert report['status']=='all_assigned_work_complete' and len(report['completed'])==2,report
 for spec in stages:
  c=json.loads(Path(spec['config']).read_bytes())
  # Completed runs are never resumed, and a changed expected endpoint is rejected.
  try:controller.start_stage(spec,c)
  except RuntimeError as error:assert 'Existing output' in str(error)
  else:raise AssertionError('Completed output was reusable')
  changed=dict(c,range_end=c['range_end']+256)
  try:controller.verify_finished(changed,allow_test=True)
  except RuntimeError as error:assert 'partial' in str(error)
  else:raise AssertionError('Partial interval permitted a rollover')
  from audit_grouped import audit_suffix
  cp=json.loads((Path(c['output'])/'checkpoint.json').read_bytes())
  for output in (c['output'],c['replica_output']):
   audit=audit_suffix(Path(output),dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',1)
   assert audit['new_chunks']==audit['new_gmp_audited_chunks']==17
 report.update(status='passed',verified_copy_gated_rollover=True,existing_output_rejected=True,partial_interval_rejected=True,independent_grouped_and_gmp_audits='17 chunks on each of two stages, local and replica',scientific_coverage=False,controller_sha256=controller.sha(ROOT/'controller.py'))
 controller.atomic(ROOT/'controller-validation.json',report)
 print(json.dumps(dict(status='passed',stages=2,rollover='Final verified copy and both released leases required before next start.')))
if __name__=='__main__':main()
