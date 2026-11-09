"""Run each frozen reserved interval once. Never restart a failed or partial interval."""
from datetime import datetime,timezone
import argparse,fcntl,hashlib,json,math,os,subprocess,sys,time
from pathlib import Path

def require(ok,message):
 if not ok:raise RuntimeError(message)
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for data in iter(lambda:f.read(8*1024**2),b''):h.update(data)
 return h.hexdigest()
def atomic(path,row):
 path=Path(path);path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
 temp=path.with_name(path.name+'.'+str(os.getpid())+'.tmp')
 with temp.open('w') as f:json.dump(row,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(temp,path)
 fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def unit(name):
 r=subprocess.run(['systemctl','--user','show',name,'-p','ActiveState','-p','Result','-p','MainPID'],capture_output=True,text=True,check=True,timeout=10)
 return dict(line.split('=',1) for line in r.stdout.splitlines() if '=' in line)
def free_lock(path):
 with Path(path).open('r+') as f:
  try:fcntl.lockf(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return False
 return True

def verify_finished(c,allow_test=False):
 local=Path(c['output']);replica=Path(c['replica_output'])
 require(unit(c['service_name'])['ActiveState']=='inactive','Previous computation has not exited successfully')
 sup=json.loads((local.parent/'supervisor.json').read_bytes());status=json.loads((local/'status.json').read_bytes())
 require(sup['error'] is None and sup['status']=='finished' and sup['worker_exit_code']==0 and sup['leases_released'] and sup.get('all_owned_processes_exited_utc'),'Previous supervisor did not exit cleanly')
 require(status['error'] is None and status['status'] in (('stopped','completed_test') if allow_test else ('stopped',)),'Previous worker failed')
 require(status['journal_buffer']['pending_chunks']==status['journal_buffer']['pending_bytes']==0,'Previous buffer did not drain')
 cpraw=(local/'checkpoint.json').read_bytes();cp=json.loads(cpraw)
 require(cp['next_patch']==c['range_end'] and cp['patches']==c['range_end']-c['initial_patch'],'Previous reserved interval is partial; automatic continuation forbidden')
 final_path=local/'final-replica.json'
 if not final_path.exists():return None
 final=json.loads(final_path.read_bytes());receipt=final['receipt']
 fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=c['manifest_sha256'],config=c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 require(final['status']=='verified' and final['compute_started'] is False,'Previous final copy failed')
 require(cp['identity']==receipt['identity']==dict(trial=c['run_id'],source_identity=fingerprint),'Previous final identity differs')
 require(cpraw==(replica/'checkpoint.json').read_bytes() and hashlib.sha256(cpraw).hexdigest()==receipt['checkpoint_sha256'],'Final checkpoint disagreement')
 require(cp['next_patch']==receipt['next_patch'] and cp['journal_sha256']==receipt['journal_sha256'] and cp['journal_offset']==receipt['committed_bytes'],'Final receipt mismatch')
 require((local/'coverage.jsonl').stat().st_size==(replica/'coverage.jsonl').stat().st_size==cp['journal_offset'],'Final raw length mismatch')
 require(sha(local/'coverage.jsonl')==sha(replica/'coverage.jsonl')==receipt['raw_sha256'],'Final raw bytes differ')
 require(free_lock(Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl'),'Previous NFS ownership is still held')
 require(free_lock('/home/pnord/boole-production-validation-20261107/gpu-owner.lock'),'GPU lease is still held')
 require(not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True,timeout=10).strip(),'GPU is still occupied')
 return dict(run_id=c['run_id'],interval=[c['initial_patch'],cp['next_patch']],patches=cp['patches'],chunks=cp['chunks'],points=cp['points'],hits=cp['hits'],
  raw_sha256=receipt['raw_sha256'],checkpoint_sha256=receipt['checkpoint_sha256'],final_replica=str(final_path),verified_utc=datetime.now(timezone.utc).isoformat())

def load_stage(spec):
 require(sha(spec['config'])==spec['config_sha256'],'Frozen stage configuration changed')
 c=json.loads(Path(spec['config']).read_bytes())
 require(sha(c['manifest'])==spec['manifest_sha256']==c['manifest_sha256'],'Frozen stage manifest changed')
 manifest=json.loads(Path(c['manifest']).read_bytes());w=Path(c['manifest']).parent
 for name,expected in manifest['files'].items():require(sha(w/name)==expected,'Stage source changed: '+name)
 for name,expected in manifest.get('external_files',{}).items():require(sha(name)==expected,'Stage helper changed: '+name)
 require((c['initial_patch'],c['range_end'])==(spec['first'],spec['last']),'Planned interval changed')
 return c

def start_stage(spec,c):
 require(time.time()<c['stop_epoch']-60,'Deadline too near to start another interval')
 require(not Path(c['output']).exists() and not Path(c['replica_output']).exists(),'Existing output; automatic resume forbidden')
 validation=json.loads((Path(spec['root'])/'runtime-validation.json').read_bytes())
 require(validation['status']=='passed' and validation['manifest_sha256']==c['manifest_sha256'],'Stage service validation is not current')
 folder=Path(spec['root'])/('controller-service-'+c['run_id']);folder.mkdir(mode=0o700,exist_ok=False)
 code="from pathlib import Path;import sys,json;sys.path.insert(0,sys.argv[1]);from validate_boole_services import launch;c=json.loads(Path(sys.argv[2]).read_bytes());result=launch(c,Path(sys.argv[2]),Path(sys.argv[3]),cleanup_extension=1800);print(json.dumps(result))"
 result=subprocess.run([sys.executable,'-B','-c',code,spec['root'],spec['config'],str(folder)],capture_output=True,text=True,timeout=45)
 require(result.returncode==0,'Stage launch failed: '+result.stderr[-4000:])
 atomic(folder/'launch.json',dict(stdout=result.stdout,stderr=result.stderr))
 return folder

def start_collector(spec,c):
 # The collector is read-only; every stage gets a separate immutable identity/share.
 root=Path(spec['root']);folder=root/('controller-reporter-'+c['run_id']);folder.mkdir(mode=0o700)
 share=Path('/mnt/nfs_share')/(c['run_id']+'-publishing');share.mkdir(mode=0o700,parents=True,exist_ok=False)
 import shutil
 shutil.copy2(root/'collector.py',folder/'collector.py')
 atomic(folder/'collector-settings.json',dict(host='boole',config=spec['config'],manifest=c['manifest'],config_sha256=spec['config_sha256'],manifest_sha256=c['manifest_sha256'],supervisor_report=str(Path(c['output']).parent/'supervisor.json'),output=str(share),stop_epoch=c['stop_epoch']))
 cmd=['systemd-run','--user','--unit='+c['run_id']+'-collector','--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077',
  '--property=RuntimeMaxSec='+str(max(1,math.floor(c['stop_epoch']+1800-time.time()))),'--property=StandardOutput=append:'+str(folder/'stdout.log'),'--property=StandardError=append:'+str(folder/'stderr.log'),sys.executable,'-B','-u',str(folder/'collector.py')]
 subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=15)
 return str(share)

def main():
 p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,required=True);p.add_argument('--plan-sha256',required=True);p.add_argument('--adopt-first',action='store_true');a=p.parse_args()
 require(sha(a.plan)==a.plan_sha256,'Frozen controller plan changed');plan=json.loads(a.plan.read_bytes())
 require(not plan.get('controller_sha256') or sha(__file__)==plan['controller_sha256'],'Controller source differs from plan')
 require(plan['automatic_resume'] is False,'Crash recovery is forbidden');require(plan['stages'],'No planned stages')
 allow_test=plan.get('TEST_ONLY') is True
 require(allow_test or plan['stop_epoch']==1794351600,'Wrong production cutoff')
 report=dict(status='starting',TEST_ONLY=allow_test,stop_epoch=plan['stop_epoch'],stop_local=plan['stop_local'],plan_sha256=a.plan_sha256,controller_sha256=sha(__file__),completed=[],active=None,error=None)
 def save():
  report['updated_utc']=datetime.now(timezone.utc).isoformat()
  atomic(plan['status_file'],report)
  if plan.get('shared_status_file'):atomic(plan['shared_status_file'],report)
 try:
  # Preflight every immutable stage before accepting ownership of the queue.
  configs=[load_stage(spec) for spec in plan['stages']]
  require(all(c['stop_epoch']<=plan['stop_epoch'] for c in configs),'A stage can exceed the controller cutoff')
  for index,(spec,c) in enumerate(zip(plan['stages'],configs)):
   if time.time()>=plan['stop_epoch']-60:
    report['status']='deadline_reached';save();return
   require(sha(a.plan)==a.plan_sha256,'Controller plan changed')
   if not(index==0 and a.adopt_first):
    start_stage(spec,c)
    if not allow_test:report['collector_share']=start_collector(spec,c)
   else:require(unit(c['service_name'])['ActiveState']=='active','First stage is not running for adoption')
   report.update(status='running',active=dict(index=index,run_id=c['run_id'],interval=[c['initial_patch'],c['range_end']],service=c['service_name']));save()
   waiting_since=None
   while True:
    if time.time()>=plan['stop_epoch']-20:
     report['status']='deadline_shutdown_scheduled';save();return
    state=unit(c['service_name'])
    if state['ActiveState']!='active':
     finished=verify_finished(c,allow_test)
     if finished is not None:
      report['completed'].append(finished);report['active']=None;save();break
     if waiting_since is None:waiting_since=time.monotonic()
     require(time.monotonic()-waiting_since<600,'Final verified copy did not finish')
    if time.time()>=plan['stop_epoch']-8:
     if state['ActiveState']=='active':subprocess.run(['systemctl','--user','stop',c['service_name']],check=True,timeout=15)
     report['status']='deadline_reached';save();return
    save();time.sleep(2 if allow_test else 10)
  report['status']='all_assigned_work_complete';save()
 except BaseException as error:
  report['status']='attention_required';report['error']=repr(error);save();raise
if __name__=='__main__':main()
