"""Rotate only clean journal-cap stops; retain claims, source and exact cursors."""
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
STATE=R/'rotation-state.json';STOP=R/'STOP_CONTROLLER'
sys.path.insert(0,str(R/'worker'))
from durable_mirror import atomic
import policy
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def command(cmd,timeout=30):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(repr(cmd)+' '+p.stderr[-1500:])
 return p.stdout
def unit(name):
 s=command(['systemctl','--user','show',name,'-p','ActiveState','-p','MainPID'])
 return dict(x.split('=',1) for x in s.splitlines() if '=' in x)
def decision(service,supervisor,status,checkpoint,config,stopping,now):
 if stopping:return 'stop'
 if service.get('ActiveState') in ('active','activating','deactivating') or service.get('MainPID')!='0':return 'wait'
 if service.get('ActiveState')=='failed' and now<config['stop_epoch']-10:raise RuntimeError('Compute service failed')
 if not supervisor or supervisor.get('worker_exit_code')!=0 or not supervisor.get('leases_released') or supervisor.get('error') is not None:raise RuntimeError('Final supervisor is missing or dirty')
 if not status or status.get('status')!='stopped' or status.get('error') is not None:raise RuntimeError('Worker did not stop cleanly')
 if status['journal_buffer']['pending_chunks'] or status['journal_buffer']['pending_bytes']:raise RuntimeError('Uncommitted journal buffer')
 if checkpoint['next_patch']==config['range_end'] or now>=config['stop_epoch']-10:return 'complete'
 if status.get('reason')!='Bulk journal byte budget reached':raise RuntimeError('Unexpected stop requires manual review: '+str(status.get('reason')))
 return 'rotate'
def service(name,cwd,script,args,deadline):
 return ['systemd-run','--user','--unit='+name,'--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(max(1,int(deadline+1800-time.time()))),'--working-directory='+str(cwd),'--property=StandardOutput=append:'+str(Path(cwd)/(name+'.stdout.log')),'--property=StandardError=append:'+str(Path(cwd)/(name+'.stderr.log')),PYTHON,'-B','-u',str(script),*args]
def require_running_context(active):
 c=read(active['config']);assert sha(active['config'])==active['config_sha256']
 assert c['manifest_sha256']==read(R/'worker/config.json')['manifest_sha256']
 for n,h in read(c['manifest'])['files'].items():assert sha(Path(c['manifest']).parent/n)==h,n
 assert c['range_end']==7000000000 and c['stop_epoch']==1794438000
 return c
def finish_and_seal(active,c):
 out=Path(c['output']);rep=Path(c['replica_output']);until=time.monotonic()+1800
 while not (out/'final-replica.json').exists():
  if STOP.exists():return None
  if time.monotonic()>until:raise TimeoutError('Final replica did not finish')
  time.sleep(2)
 final=read(out/'final-replica.json');raw=(out/'checkpoint.json').read_bytes();cp=json.loads(raw)
 assert final['status']=='verified' and (rep/'checkpoint.json').read_bytes()==raw
 receipt=final['receipt'];assert receipt['checkpoint_sha256']==hashlib.sha256(raw).hexdigest() and receipt['committed_bytes']==cp['journal_offset'] and receipt['journal_sha256']==cp['journal_sha256']
 assert (out/'coverage.jsonl').stat().st_size==(rep/'coverage.jsonl').stat().st_size==cp['journal_offset']
 import suballocation_guard
 assert not suballocation_guard.locked_by_other(Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl')
 # All receipt parsing stays on the stopped NVMe source, keeping bulk I/O free
 # for the other nodes. The final mirror already compared the complete bytes.
 from parallel_audit_ref import audit
 checked=audit(out,c,workers=16)
 checked.update(captured_checkpoint_sha256=receipt['checkpoint_sha256'],committed_chain_sha256=cp['journal_sha256'],committed_raw_sha256=receipt['raw_sha256'],selected_interval=[c['initial_patch'],cp['next_patch']],uncommitted_trailing_bytes=0,owner_lock_released=True,local_and_replica_equal=True)
 folder=R/'rotation-evidence'/c['run_id'];folder.mkdir(mode=0o700,parents=True,exist_ok=True)
 atomic(folder/'parent-audit.json',checked)
 ar=dict(status='verified',raw_sha256=receipt['raw_sha256'],committed_bytes=cp['journal_offset'],captured_checkpoint_sha256=receipt['checkpoint_sha256'],source=str(out),archive=str(rep),captured_status_sha256=sha(rep/'status.json'),method='Full unchanged receipt/GMP audit and independent final mirror byte comparison/readback',audit_sha256=sha(folder/'parent-audit.json'))
 assert not (rep/'ARCHIVE_RECEIPT.json').exists();atomic(rep/'ARCHIVE_RECEIPT.json',ar)
 # Reuse the verified archive copy and preserve the original journal path.
 local=out/'coverage.jsonl';pending=out/'coverage.OFFLOAD_PENDING.jsonl';assert not local.is_symlink() and not pending.exists()
 os.rename(local,pending)
 try:local.symlink_to(rep/'coverage.jsonl');assert local.stat().st_size==cp['journal_offset'];pending.unlink()
 except BaseException:
  if local.is_symlink():local.unlink()
  if pending.exists():os.rename(pending,local)
  raise
 atomic(out/'LOCAL_JOURNAL_ARCHIVED.json',dict(status='archived_verified_copy_with_original_path_preserved',source=str(local),archive=str(rep/'coverage.jsonl'),bytes=cp['journal_offset'],raw_sha256=receipt['raw_sha256']))
 return folder,cp,checked,rep
def prepare_successor(active,c,sealed,index):
 folder,cp,audit,parent=sealed;name='ada-preparation-rotation-%02d-20261110'%index;root=R/'stages'/name;w=root/'worker'
 root.mkdir(mode=0o700,parents=True,exist_ok=False)
 shutil.copytree(Path(c['manifest']).parent,w,ignore=shutil.ignore_patterns('__pycache__','*.log','supervisor-report.json','supervisor-preflight.json','launch.json','preparation-report.json','launcher.lock','coordinator.lock','STOP'))
 shutil.copy2(folder/'parent-audit.json',root/'parent-audit.json');shutil.copy2(folder/'parent-audit.json',w/'parent-audit.json')
 stat=(parent/'coverage.jsonl').stat();n=dict(c,run_id=name,initial_patch=cp['next_patch'],parent_run=str(parent),parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_status_file=str(parent/'status.json'),parent_status_sha256=sha(parent/'status.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_offset=cp['journal_offset'],parent_journal_raw_sha256=audit['committed_raw_sha256'],parent_journal_identity=[stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns],parent_selected_patches=c['parent_selected_patches']+cp['patches'],parent_audit_file=str(w/'parent-audit.json'),parent_audit_sha256=sha(w/'parent-audit.json'),parent_archive_receipt=str(parent/'ARCHIVE_RECEIPT.json'),parent_archive_receipt_sha256=sha(parent/'ARCHIVE_RECEIPT.json'),manifest=str(w/'release-manifest.json'),origin_claim_file=str(w/'child-claim.json'),handoff_parent_config_file=active['config'],handoff_parent_config_sha256=active['config_sha256'],service_name=name+'.service',deadline_service_name=name+'-deadline.service',journal_limit_bytes=32*1024**3,output=str(Path(c['output']).parents[1]/name/'run'),replica_output=str(Path(c['replica_output']).parents[1]/name/'run'),coverage_file=str(w/'final-coverage.json'))
 coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=cp['next_patch'],parent_checkpoint_sha256=n['parent_checkpoint_sha256'],parent_journal_sha256=cp['journal_sha256'],parent_journal_raw_sha256=n['parent_journal_raw_sha256'],cumulative_selected_patches=n['parent_selected_patches'],full_bound_claim=False)
 atomic(w/'final-coverage.json',coverage);n['coverage_sha256']=sha(w/'final-coverage.json')
 for key in ('output','replica_output'):Path(n[key]).parent.mkdir(mode=0o700,parents=True,exist_ok=True);assert not Path(n[key]).exists()
 for p in (w/'config.json',w/'base-config.json'):atomic(p,n)
 for file in ('runtime-validation.json','gpu-validation.json','unit-validation.json','selection-results.json','prepare_launch.py','collector.py','publish_buffered.py'):shutil.copy2(R/file,root/file)
 atomic(root/'configuration-state.json',dict(status='production_configured',manifest_sha256=n['manifest_sha256'],config_sha256=sha(w/'config.json'),production_started=False))
 reporting=(R/'prepare_reporting.py').read_text().replace("REPORTER = Path('/home/pnord/ada-preparation-reporting-20261110')","REPORTER = ROOT/'reporting'").replace("cfg['run_id'] == 'ada-preparation-20261110'","cfg['run_id'] == "+repr(name)).replace("service_name='ada-preparation-publisher-20261110.service'","service_name=cfg['run_id']+'-publisher.service'")
 (root/'prepare_reporting.py').write_text(reporting)
 return dict(root=str(root),worker=str(w),config=str(w/'config.json'),config_sha256=sha(w/'config.json'),service=n['service_name'],collector=name+'-collector.service',publisher=name+'-publisher.service',reporter=str(root/'reporting'))
def start_successor(previous,active):
 c=read(active['config']);root=Path(active['root']);w=Path(active['worker']);reporter=Path(active['reporter'])
 until=time.monotonic()+60
 while unit(previous['publisher'])['ActiveState'] in ('active','activating','deactivating'):
  if STOP.exists():return False
  if time.monotonic()>until:raise TimeoutError('Previous terminal publisher did not finish')
  time.sleep(1)
 prior=read(previous['config']);closed=read(Path(prior['output'])/'checkpoint.json');published=read(Path(previous['reporter'])/'readiness.json')
 assert published['latest_push']['phase']=='stopped' and published['latest_push']['next_patch']==closed['next_patch']
 assert published['latest_readback']['status']=='passed' and published['latest_readback']['commit']==published['latest_push']['commit']
 if STOP.exists():return False
 command(['systemctl','--user','stop',previous['collector']])
 for script in ('prepare_launch.py','prepare_reporting.py'):command([PYTHON,'-B',str(root/script)])
 for kind,script,args,cwd in [('final-copy',w/'finalize_replica.py',['--config',active['config'],'--config-sha256',active['config_sha256'],'--wait'],root),('collector',reporter/'collector.py',[],reporter)]:
  if STOP.exists():return False
  command(service(c['run_id']+'-'+kind,cwd,script,args,c['stop_epoch']))
 if STOP.exists():return False
 command([PYTHON,'-B',str(w/'launch_weekend.py'),'--launch'],timeout=70)
 until=time.monotonic()+30
 while not (Path(c['replica_output'])/'checkpoint.json').exists():
  if STOP.exists():return False
  if time.monotonic()>until:raise TimeoutError('New stage has no verified first replica')
  time.sleep(.2)
 command(service(c['run_id']+'-publisher',reporter,reporter/'publish_bulk_worker.py',[],c['stop_epoch']))
 return True
def main():
 p=argparse.ArgumentParser();p.add_argument('--self-sha256',required=True);a=p.parse_args();assert sha(__file__)==a.self_sha256
 if STATE.exists():raise RuntimeError('Controller state exists; manual review required')
 cfg=R/'worker/config.json';active=dict(root=str(R),worker=str(R/'worker'),config=str(cfg),config_sha256=sha(cfg),service='ada-preparation-20261110.service',collector='ada-preparation-collector-20261110.service',publisher='ada-preparation-publisher-20261110.service',reporter='/home/pnord/ada-preparation-reporting-20261110')
 state=dict(status='adopting',active=active,completed=[],source_sha256=a.self_sha256,automatic_failed_resume=False)
 try:
  while True:
   assert sha(__file__)==a.self_sha256
   if STOP.exists():state.update(status='stop',active=active,updated_epoch=time.time());atomic(STATE,state);return
   c=require_running_context(active);s=unit(active['service'])
   if s['ActiveState'] in ('active','activating','deactivating') or s['MainPID']!='0':action='stop' if STOP.exists() else 'wait'
   else:action=decision(s,read(Path(active['worker'])/'supervisor-report.json'),read(Path(c['output'])/'status.json'),read(Path(c['output'])/'checkpoint.json'),c,STOP.exists(),time.time())
   state.update(status='running' if action=='wait' else action,active=active,updated_epoch=time.time());atomic(STATE,state)
   if action in ('stop','complete'):return
   if action=='wait':time.sleep(5);continue
   sealed=finish_and_seal(active,c)
   if sealed is None:return
   previous=active;active=prepare_successor(previous,c,sealed,len(state['completed'])+1)
   state['completed'].append(dict(run_id=c['run_id'],cursor=sealed[1]['next_patch'],evidence=str(sealed[0])))
   state.update(status='starting',active=active,updated_epoch=time.time());atomic(STATE,state)
   if not start_successor(previous,active):return
 except BaseException as e:
  state.update(status='failed_closed',error=repr(e),active=active,updated_epoch=time.time());atomic(STATE,state);raise
if __name__=='__main__':main()
