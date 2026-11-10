"""Authorized overnight production: fresh journals, explicit rotation, one GPU."""
from pathlib import Path
import fcntl,hashlib,json,os,signal,subprocess,sys,time,shutil,tarfile
import release,units
ROOT=Path(__file__).resolve().parent;DEADLINE=1794438000
sys.path.insert(0,str(ROOT/'worker'))
from durable_mirror import atomic
STOP=False
SHUTDOWN_TIMEOUT=900
class StopRequested(RuntimeError):pass
def load(p):return json.loads(Path(p).read_bytes())
def stop_requested():return STOP or (ROOT/'stop-request.json').exists() or time.time()>=DEADLINE-10
def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(value):return isinstance(value,str) and len(value)==64 and all(ch in '0123456789abcdef' for ch in value)
def quiescent(unit):return unit.get('ActiveState')=='inactive' and unit.get('MainPID')=='0'
def wait_for_completion(c,path,timeout=SHUTDOWN_TIMEOUT):
 """Accept only a quiescent owner, final report, and matching verified replica."""
 until=time.monotonic()+timeout;sent_stop=False;waiting='compute owner to become inactive with MainPID=0'
 def pause():
  if time.monotonic()>=until:raise TimeoutError('Shutdown incomplete: '+waiting+'; no automatic restart')
  time.sleep(min(2,max(0,until-time.monotonic())))
 while True:
  if stop_requested() and not sent_stop:units.call('stop',c['service_name']);sent_stop=True
  unit=units.state(c['service_name'])
  require(unit.get('ActiveState')!='failed','Compute service failed; no automatic restart')
  if quiescent(unit):break
  pause()
 require(unit.get('Result')=='success' and unit.get('ExecMainStatus')=='0','Compute service did not exit successfully')
 run=Path(c['output']);replica=Path(c['replica_output'])
 while True:
  try:
   sup=load(run.parent/'supervisor.json')
   require(sup.get('error') is None and sup.get('status')!='failed','Supervisor failed; no automatic restart')
   if sup.get('status')!='finished':waiting='final supervisor report';pause();continue
   require('error' in sup and sup.get('worker_exit_code')==0 and type(sup.get('worker_exit_code')) is int and sup.get('leases_released') is True,'Incomplete or failed final supervisor report; no automatic restart')
   require(sup.get('config_sha256')==release.sha(path),'Supervisor configuration identity mismatch')
   status=load(run/'status.json')
   require(status.get('error') is None and status.get('status')!='failed','Worker failed; no automatic restart')
   require('error' in status and status.get('status')=='stopped','Worker did not publish a final stopped status')
   buffer=status.get('journal_buffer',{})
   require(all(type(buffer.get(key)) is int and buffer[key]==0 for key in ('pending_chunks','pending_bytes')),'Final journal buffer is not empty')
   cp_raw=(run/'checkpoint.json').read_bytes();cp=json.loads(cp_raw)
   require(type(cp.get('next_patch')) is int and c['initial_patch']<=cp['next_patch']<=c['range_end'],'Checkpoint cursor outside configured interval')
   require(cp.get('window',{}).get('last')==c['range_end'],'Unexpected production endpoint')
   for key in ('chunks','journal_offset','next_patch','journal_sha256'):
    require(key in cp and status.get(key)==cp[key],'Final worker/checkpoint mismatch: '+key)
   require(type(cp['journal_offset']) is int and cp['journal_offset']>=0 and type(cp['chunks']) is int and cp['chunks']>=0,'Invalid checkpoint counters')
   require(digest(cp['journal_sha256']),'Invalid checkpoint journal digest')
   final=load(run/'final-replica.json');receipt=final.get('receipt',{})
   require(final.get('status')=='verified' and final.get('compute_started') is False and receipt.get('status')=='verified','Final replica is not verified')
   require(receipt.get('checkpoint_sha256')==hashlib.sha256(cp_raw).hexdigest(),'Final replica checkpoint digest mismatch')
   require((replica/'checkpoint.json').read_bytes()==cp_raw,'Replica checkpoint differs from final local checkpoint')
   for source,target in [('next_patch','next_patch'),('chunks','chunks'),('journal_offset','committed_bytes'),('journal_sha256','journal_sha256'),('identity','identity')]:
    require(source in cp and receipt.get(target)==cp[source],'Final replica/checkpoint mismatch: '+source)
   require(all(type(receipt.get(key)) is int for key in ('next_patch','chunks','committed_bytes')) and digest(receipt.get('raw_sha256')),'Invalid final replica receipt counters or digest')
   fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=c['manifest_sha256'],config=c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
   require(cp['identity']==dict(trial=c['run_id'],source_identity=fingerprint),'Checkpoint configuration identity mismatch')
   require(load(replica/'replica-state.json')==receipt,'Final replica receipt differs from published replica state')
   require((run/'coverage.jsonl').stat().st_size==cp['journal_offset'] and (replica/'coverage.jsonl').stat().st_size==cp['journal_offset'],'Final journal size differs from committed checkpoint')
   require(quiescent(units.state(c['service_name'])),'Compute owner became active while checking final evidence')
   return status,cp,sup,final
  except FileNotFoundError:
   waiting='final supervisor, worker status/checkpoint, or verified replica files';pause()
def verify_controller():
 for name,h in load(ROOT/'controller-manifest.json')['files'].items():assert release.sha(ROOT/name)==h,'Frozen controller changed: '+name
def next_action(cp,status,now=None,stop_intent=False):
 now=time.time() if now is None else now
 if stop_intent or now>=DEADLINE-10 or status.get('error') or status.get('reason')=='Stop requested':return 'stop'
 if cp['next_patch']==cp['window']['last']:return 'next_reservation'
 if status['reason']=='Local journal byte cap reached':return 'rotate'
 return 'stop'
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
 if stop_requested():raise StopRequested('Stop requested before binding next configuration')
 c=bind(path)
 assert not Path(c['output']).exists() and not Path(c['replica_output']).exists(),'Refuse automatic recovery or output reuse'
 if stop_requested():raise StopRequested('Stop requested before starting next configuration')
 units.start(path);state('running',run_id=c['run_id'],config=str(path));return c
def main():
 global STOP
 signal.signal(signal.SIGTERM,lambda *_:globals().__setitem__('STOP',True));signal.signal(signal.SIGINT,lambda *_:globals().__setitem__('STOP',True))
 lock=(ROOT/'controller.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 path=ROOT/'production-config.json';c=None;history=[]
 try:
  verify_controller()
  settings=load(ROOT/'controller-settings.json') if (ROOT/'controller-settings.json').exists() else {}
  used_pending=settings.get('pending_consumed',False)
  require(type(used_pending) is bool,'controller-settings.pending_consumed must be boolean')
  c=start(path)
  while True:
   verify_controller()
   if stop_requested():state('stopping',reason='Requested stop or absolute deadline',history=history)
   elif units.state(c['service_name']).get('ActiveState')=='active':time.sleep(2);continue
   status,cp,sup,final=wait_for_completion(c,path)
   history.append(dict(run_id=c['run_id'],config=str(path),first=c['initial_patch'],last=cp['next_patch'],claim_sha256=c['ledger_claim_sha256'],final_checkpoint_sha256=release.sha(Path(c['output'])/'checkpoint.json')))
   assert cp['window']['last']==c['range_end'],'Unexpected production endpoint'
   action=next_action(cp,status,stop_intent=stop_requested())
   if action=='stop':state('stopped',reason=status['reason'],history=history);return 0
   state('sealing',run_id=c['run_id'],history=history)
   ev=ROOT/'rotation-evidence'/c['run_id'];ev.mkdir(parents=True,exist_ok=False)
   with (ev/'seal.log').open('x') as log:
    subprocess.run([sys.executable,'-B',str(ROOT/'seal_previous.py'),'--config',str(path),'--evidence',str(ev)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1200)
   if stop_requested():state('stopped',reason='Stop requested after seal',history=history);return 0
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
 except StopRequested as exc:
  state('stopped',reason=str(exc),history=history);return 0
 except BaseException as exc:
  state('failed',error=repr(exc),history=history)
  if c:units.call('stop',c['service_name'])
  raise
 finally:
  if c and stop_requested():units.call('stop',c['service_name'])
  lock.close()
if __name__=='__main__':raise SystemExit(main())
