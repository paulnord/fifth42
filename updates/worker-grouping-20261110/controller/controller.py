"""Authorized overnight production: fresh journals, explicit rotation, one GPU."""
from pathlib import Path
import fcntl,hashlib,json,os,signal,subprocess,sys,time,shutil,tarfile
import release,units
ROOT=Path(__file__).resolve().parent;DEADLINE=1794351600
sys.path.insert(0,str(ROOT/'worker'))
from durable_mirror import atomic
STOP=False
def load(p):return json.loads(Path(p).read_bytes())
def verify_controller():
 for name,h in load(ROOT/'controller-manifest.json')['files'].items():assert release.sha(ROOT/name)==h,'Frozen controller changed: '+name
def next_action(cp,status,now=None,supervisor=None):
 now=time.time() if now is None else now
 if now>=DEADLINE-10 or status.get('error') or (supervisor or {}).get('stop_trigger'):return 'stop'
 if cp['next_patch']==cp['window']['last']:return 'next_reservation'
 if status['reason']=='Local journal byte cap reached':return 'rotate'
 return 'stop'
def completion_state(status,sup,config_hash):
 """Fail closed on explicit failures; missing final fields mean wait, never success."""
 if not isinstance(status,dict) or not isinstance(sup,dict):
  raise RuntimeError('Malformed completion report')
 if status.get('error') is not None or sup.get('error') is not None:
  raise RuntimeError('Failure requires explicit recovery; no automatic restart')
 if sup.get('config_sha256') != config_hash:
  raise RuntimeError('Supervisor report does not match frozen configuration')
 if 'worker_exit_code' in sup and sup['worker_exit_code'] is not None:
  code=sup['worker_exit_code']
  if type(code) is not int or code != 0:
   raise RuntimeError('Worker did not exit successfully; explicit recovery required')
 if status.get('status') == 'failed' or sup.get('status') == 'failed':
  raise RuntimeError('Failed completion report; explicit recovery required')
 if (status.get('status') == 'stopped' and sup.get('status') == 'finished'
     and type(sup.get('worker_exit_code')) is int and sup['worker_exit_code'] == 0
     and sup.get('leases_released') is True
     and isinstance(sup.get('all_owned_processes_exited_utc'),str)
     and bool(sup['all_owned_processes_exited_utc'])
     and 'error' in status and 'error' in sup):
  return 'complete'
 return 'pending'
def await_completion(c,path,timeout=120):
 """Systemd inactivity is not proof that supervisor cleanup/reporting finished."""
 until=time.monotonic()+timeout
 while True:
  if STOP or time.time()>=DEADLINE-10:return None
  try:
   status=load(Path(c['output'])/'status.json')
   sup=load(Path(c['output']).parent/'supervisor.json')
   if completion_state(status,sup,release.sha(path)) == 'complete':
    return status,load(Path(c['output'])/'checkpoint.json'),sup
  except FileNotFoundError:
   pass
  if time.monotonic()>=until:
   raise TimeoutError('Terminal worker/lease report unavailable; explicit recovery required')
  time.sleep(2)
def available_interval(claims):
 cursor=1;gaps=[]
 for row in sorted(claims,key=lambda x:x['first']):
  if cursor<row['first']:gaps.append((cursor,row['first']))
  cursor=max(cursor,row['last'])
 if cursor<11250000001:gaps.append((cursor,11250000001))
 if not gaps:return None
 first,last=max(gaps,key=lambda x:x[1]-x[0]);return max(first,last-500000000),last
def allocate_more(previous,seal):
 import ada_export_store as store_module
 c=load(previous);store=store_module.Store(c['ledger_root'])
 for attempt in range(5):
  with store.locked(store.root/'reservations.jsonl') as fd:claims=store.claims(fd)
  interval=available_interval(claims)
  if interval is None:return None
  first,last=interval;tag=time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+str(time.time_ns()%1000000)
  job='cabbage-extended-allocation-'+tag
  contract=dict(status='new_uncomputed_reservation',host='cabbage',authorized_by='User: continue production until tomorrow at 5 pm',stop_epoch=DEADLINE,grid=store_module.GRID,first=first,last=last,compute_manifest_sha256=c['manifest_sha256'],coverage_claimed=False,allocation_scope='Unreserved cells only; patch zero remains a separate unresolved boundary')
  raw=(json.dumps(contract,sort_keys=True,indent=2)+'\n').encode();digest=hashlib.sha256(raw).hexdigest()
  try:claim=store.reserve(job,first,last,digest,dict(sha256=digest,manifest=contract))
  except store_module.Conflict:continue
  with (store.root/'jobs'/job/'journal.jsonl').open('xb') as fd:fd.flush();os.fsync(fd.fileno())
  fd=os.open(store.root/'jobs'/job,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
  root=ROOT/'continuations'/('cabbage-extended-allocation-'+tag);root.mkdir(parents=True)
  return release.freeze(root,previous,seal,claim,contract)
 raise RuntimeError('Concurrent allocation did not settle; no overlapping work was started')
def bind(path):
 c=load(path);assert c['TEST_ONLY'] is False and c['stop_epoch']==DEADLINE and c['automatic_resume'] is False
 manifest=Path(c['manifest']);assert release.sha(manifest)==c['manifest_sha256']
 for name,h in load(manifest)['files'].items():assert release.sha(manifest.parent/name)==h
 row=dict(config=str(path),config_sha256=release.sha(path),manifest=str(manifest),manifest_sha256=c['manifest_sha256'],supervisor_report=str(Path(c['output']).parent/'supervisor.json'),stop_epoch=DEADLINE)
 share=Path('/mnt/nfs_share/cabbage-extended-publishing-20261109');dest=share/'runs'/c['run_id'];dest.mkdir(mode=0o700,parents=True,exist_ok=False)
 evidence={'configuration.json':Path(path),'source-manifest.json':manifest,'parent-audit.json':Path(c['parent_audit_file']),'parent-archive-receipt.json':Path(c['parent_archive_receipt']),'original-claim.json':Path(c['origin_claim_file'])}
 for name,p in evidence.items():shutil.copy2(p,dest/name);assert release.sha(dest/name)==release.sha(p)
 with tarfile.open(dest/'source.tar.gz','w:gz') as tar:
  for name in load(manifest)['files']:tar.add(manifest.parent/name,arcname='worker/'+name,recursive=False)
  tar.add(manifest,arcname='worker/release-manifest.json');tar.add(manifest.parent/'base-config.json',arcname='worker/base-config.json');tar.add(path,arcname='production-config.json')
 spec=dict(row,run_id=c['run_id'],ledger_job=c['ledger_job'],ledger_claim_sha256=c['ledger_claim_sha256'],initial_patch=c['initial_patch'],range_end=c['range_end'],fresh_reservation=c.get('fresh_reservation',False),source_archive_sha256=release.sha(dest/'source.tar.gz'),evidence_sha256={name:release.sha(dest/name) for name in evidence})
 atomic(dest/'READY.json',spec);atomic(share/'active-publication-spec.json',spec)
 atomic(ROOT/'active-configuration.json',row);return c
def state(phase,**kwargs):atomic(ROOT/'controller-state.json',dict(phase=phase,updated_epoch=time.time(),stop_epoch=DEADLINE,**kwargs))
def start(path):
 c=bind(path)
 assert not Path(c['output']).exists() and not Path(c['replica_output']).exists(),'Refuse automatic recovery or output reuse'
 units.start(path);state('running',run_id=c['run_id'],config=str(path));return c
def main():
 global STOP
 signal.signal(signal.SIGTERM,lambda *_:globals().__setitem__('STOP',True));signal.signal(signal.SIGINT,lambda *_:globals().__setitem__('STOP',True))
 lock=(ROOT/'controller.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 verify_controller()
 path=ROOT/'production-config.json';c=None;history=[];used_pending=False
 try:
  c=start(path)
  while True:
   verify_controller()
   if STOP or time.time()>=DEADLINE-10:
    units.call('stop',c['service_name']);state('stopped',reason='Requested stop or absolute deadline',history=history);return 0
   if units.state(c['service_name'])['ActiveState']=='active':time.sleep(2);continue
   completion=await_completion(c,path)
   if completion is None:state('stopped',reason='Awaiting final report; requested stop or deadline',history=history);return 0
   status,cp,sup=completion
   until=time.monotonic()+900
   while not (Path(c['output'])/'final-replica.json').exists():
    if STOP or time.time()>=DEADLINE-10:state('stopped',reason='Compute stopped; independent cleanup remains active',history=history);return 0
    if time.monotonic()>until:raise TimeoutError('Final replica did not finish')
    time.sleep(2)
   assert load(Path(c['output'])/'final-replica.json')['status']=='verified'
   history.append(dict(run_id=c['run_id'],config=str(path),first=c['initial_patch'],last=cp['next_patch'],claim_sha256=c['ledger_claim_sha256'],final_checkpoint_sha256=release.sha(Path(c['output'])/'checkpoint.json')))
   assert cp['window']['last']==c['range_end'],'Unexpected production endpoint'
   action=next_action(cp,status,supervisor=sup)
   if action=='stop':state('stopped',reason=status['reason'],history=history);return 0
   state('sealing',run_id=c['run_id'],history=history)
   ev=ROOT/'rotation-evidence'/c['run_id'];ev.mkdir(parents=True,exist_ok=False)
   with (ev/'seal.log').open('x') as log:
    subprocess.run([sys.executable,'-B',str(ROOT/'seal_previous.py'),'--config',str(path),'--evidence',str(ev)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1200)
   if STOP or time.time()>=DEADLINE-10:state('stopped',reason='Deadline after seal',history=history);return 0
   units.call('stop',c['deadline_service_name'].replace('.service','.timer'))
   if action=='next_reservation':
    if used_pending:
     path=allocate_more(path,load(ev/'parent-seal.json'))
     if path is None:state('completed_available_work',reason='No unreserved cells remain',history=history);return 0
    else:path=Path(load(ROOT/'pending-configuration.json')['config']);used_pending=True
   else:
    root=ROOT/'continuations'/('cabbage-extended-rotation-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()));root.mkdir(parents=True,exist_ok=False)
    path=release.freeze(root,path,load(ev/'parent-seal.json'))
   c=start(path)
 except BaseException as exc:
  state('failed',error=repr(exc),history=history)
  if c:units.call('stop',c['service_name'])
  raise
 finally:
  if c and (STOP or time.time()>=DEADLINE-10):units.call('stop',c['service_name'])
  lock.close()
if __name__=='__main__':raise SystemExit(main())
