"""Actual finite/signal/deadline services, original owner lock and final replicas."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import fcntl,hashlib,json,os,subprocess,sys,time
import units
R=Path(__file__).resolve().parent;W=R/'worker';sys.path.insert(0,str(W))
import audit_grouped,policy
base=json.loads((R/'production-config.json').read_bytes());configs=R/'test-configs';configs.mkdir(exist_ok=True)
def load(p):return json.loads(Path(p).read_bytes())
def wait(predicate,seconds,message):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if predicate():return
  time.sleep(.2)
 raise TimeoutError(message)
def cp_exists(c,n=1):
 try:return load(Path(c['output'])/'checkpoint.json')['chunks']>=n
 except FileNotFoundError:return False
def main():
 rows=[]
 for case in ['finite','signal','deadline']:
  c=dict(base);run=f'cabbage-extended-test-{case}-{time.time_ns()}';stop=int(time.time())+(50 if case=='deadline' else 110)
  c.update(TEST_ONLY=True,run_id=run,output=f'/home/pnord/fifth42-local-runs/TEST_ONLY_cabbage_extended_20261109/{run}/run',replica_output=f'/mnt/fifth42-storage/TEST_ONLY_cabbage_extended_20261109/{run}/run',
   stop_epoch=stop,stop_local=datetime.fromtimestamp(stop,ZoneInfo('America/Chicago')).isoformat(),gmp_audit_period=128 if case=='deadline' else 1,
   test_chunk_limit=5 if case=='finite' else None,range_end=base['initial_patch']+1280 if case=='finite' else base['range_end'],
   service_name=f'fifth-{run}.service',deadline_service_name=f'fifth-{run}-deadline.service',cleanup_service_name=f'fifth-{run}-final-copy.service')
  for p in [Path(c['output']).parent,Path(c['replica_output']).parent]:p.mkdir(mode=0o700,parents=True,exist_ok=False)
  path=configs/(run+'.json');path.write_text(json.dumps(c,indent=2)+'\n');path.chmod(0o400)
  started=time.time()
  try:
   _,unit_files=units.start(path)
   wait(lambda:cp_exists(c,2),30,'Worker did not commit two chunks')
   # While running, another process must not acquire the original NFS owner.
   if case!='finite':
    p=Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl'
    with p.open('r+') as owner:
     try:fcntl.lockf(owner,fcntl.LOCK_EX|fcntl.LOCK_NB)
     except BlockingIOError:owner_excluded=True
     else:raise AssertionError('Original owner lock was not held')
   else:owner_excluded=None
   if case=='signal':units.call('stop',c['service_name'])
   wait(lambda:units.state(c['service_name'])['ActiveState'] in ('inactive','failed'),65,'Compute did not stop')
   service=units.state(c['service_name']);assert service['Result']=='success' and service['ExecMainStatus']=='0',service
   assert time.time()<stop,'Owned compute did not stop before the hard deadline'
   wait(lambda:(Path(c['output'])/'final-replica.json').exists(),45,'Independent final replica was not completed')
   wait(lambda:units.state(c['cleanup_service_name'])['ActiveState'] in ('inactive','failed'),10,'Cleanup did not finish')
   assert units.state(c['cleanup_service_name'])['Result']=='success'
   local=Path(c['output']);replica=Path(c['replica_output']);cp=load(local/'checkpoint.json');assert (local/'checkpoint.json').read_bytes()==(replica/'checkpoint.json').read_bytes()
   terminal=load(local/'status.json')
   assert terminal['error'] is None and terminal['journal_buffer']['pending_chunks']==0 and terminal['journal_buffer']['pending_bytes']==0
   assert (local/'coverage.jsonl').stat().st_size==cp['journal_offset']
   if case=='finite':assert cp['chunks']==5 and cp['patches']==1280
   receipt=load(replica/'replica-state.json');assert receipt['next_patch']==cp['next_patch'] and receipt['checkpoint_sha256']==hashlib.sha256((local/'checkpoint.json').read_bytes()).hexdigest()
   audit=lambda folder:audit_grouped.audit_suffix(folder,dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',c['gmp_audit_period'])
   a,b=audit(local),audit(replica);assert a==b
   sup=load(local.parent/'supervisor.json');assert sup['leases_released'] and sup['worker_exit_code']==0 and sup['error'] is None
   for p in [Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl',Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock')]:
    with p.open('r+') as lock:fcntl.lockf(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
   assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
   try:policy.load_config(path)
   except RuntimeError as e:assert 'Existing output' in str(e)
   else:raise AssertionError('Existing output reuse was accepted')
   rows.append(dict(case=case,status='passed',config=str(path),chunks=cp['chunks'],logical_cells=cp['patches'],physical_tasks=cp['physical_tasks'],points=cp['points'],
    local_cursor=cp['next_patch'],replica_cursor=receipt['next_patch'],owner_excluded_while_running=owner_excluded,leases_released=True,actual_systemd_timer=True,
    compute_stopped_before_deadline=True,final_copy_service_passed=True,both_copies_independently_audited=True,final_buffer_drained=True,output_reuse_rejected=True,supervisor=sup,
    seconds=time.time()-started,unit_files=unit_files))
   (R/'evidence/runtime-validation-progress.json').write_text(json.dumps(rows,indent=2)+'\n');print(case,'PASS',cp['chunks'],'chunks',cp['next_patch'],flush=True)
  finally:
   units.call('stop',c['deadline_service_name'].replace('.service','.timer'))
   units.call('stop',c['service_name'])
   if units.state(c['cleanup_service_name'])['ActiveState']=='active':units.call('stop',c['cleanup_service_name'])
 result=dict(status='passed',host='cabbage',manifest_sha256=base['manifest_sha256'],config_sha256=hashlib.sha256((R/'production-config.json').read_bytes()).hexdigest(),
  actual_services=True,actual_local_and_nfs=True,original_owner_lock=True,group_limit=base['group_limit'],cases=rows,
  buffering_tests=json.loads((R/'evidence/buffering-validation.json').read_bytes()),dispatch_chunksize=4,ready_queue_limit=3,journal_buffer_records=8)
 (R/'evidence/runtime-validation.json').write_text(json.dumps(result,indent=2)+'\n');print('ALL RUNTIME ACCEPTANCE PASSED',flush=True)
if __name__=='__main__':main()
