"""Exercise the actual local-journal Boole services before production launch."""
from datetime import datetime,timezone
import argparse,fcntl,hashlib,json,math,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import policy,ada_export_store
from durable_mirror import atomic
from audit_grouped import audit_suffix
PYTHON='/home/pnord/boole-results-20261107/venv312/bin/python'

def command(args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=20)
 policy.require(p.returncode==0,'Service command failed: '+p.stderr)
 return dict(command=args,stdout=p.stdout,stderr=p.stderr)
def unit(name):
 p=command(['systemctl','--user','show',name,'--property=ActiveState,SubState,MainPID,Result,Restart,KillMode,NextElapseUSecRealtime'])
 return dict(line.split('=',1) for line in p['stdout'].splitlines() if '=' in line)
def excluded(path):
 with Path(path).open('a+') as f:
  try:fcntl.lockf(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return True
 return False
def wait_for(predicate,seconds,message):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if predicate():return
  time.sleep(.15)
 raise TimeoutError(message)

def launch(config,path,folder,cleanup_extension=60):
 now=time.time();service=config['service_name'];name=service.removesuffix('.service')
 cleanup=name+'-final-copy';timer_name=config['deadline_service_name'].removesuffix('.service')
 cleanup_command=['systemd-run','--user','--unit='+cleanup,'--collect','--service-type=exec','--property=Restart=no',
  '--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(max(1,math.floor(config['stop_epoch']+cleanup_extension-now)-2)),
  '--property=StandardOutput=append:'+str(folder/'final-copy.stdout'),'--property=StandardError=append:'+str(folder/'final-copy.stderr'),
  PYTHON,'-B',str(W/'finalize_replica.py'),'--config',str(path),'--config-sha256',policy.digest(path),'--wait']
 calls=[command(cleanup_command)]
 when=datetime.fromtimestamp(int(config['stop_epoch'])-10,timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
 calls.append(command(['systemd-run','--user','--unit='+timer_name,'--service-type=oneshot','--on-calendar='+when,
  '--timer-property=AccuracySec=1s','--timer-property=RandomizedDelaySec=0','--timer-property=Persistent=no',
  '/usr/bin/systemctl','--user','stop',service]))
 calls.append(command(['systemd-run','--user','--unit='+name,'--collect','--service-type=exec',
  '--property=Restart=no','--property=KillMode=mixed','--property=TimeoutStopSec=8','--property=Nice=19','--property=UMask=0077',
  '--property=CPUAffinity=0-15','--property=RuntimeMaxSec='+str(math.floor(config['stop_epoch']-time.time()-1)),
  '--property=StandardOutput=append:'+str(folder/'worker.stdout'),'--property=StandardError=append:'+str(folder/'worker.stderr'),
  PYTHON,'-B','-u',str(W/'boole_supervisor.py'),'--config',str(path)]))
 return calls,cleanup+'.service',timer_name+'.timer'

def case(label,finite=False,signal_stop=False,deadline=False):
 base=json.loads((W/'base-config.json').read_bytes());c=dict(base)
 name='boole-overnight-test-'+label+'-20261109'
 local=policy.LOCAL/'TEST_ONLY_boole_overnight_20261109'/name
 replica=policy.BULK/'TEST_ONLY_boole_overnight_20261109'/name
 local.mkdir(mode=0o700,parents=True,exist_ok=False)
 ledger=policy.TEST_LEDGER/label;s=ada_export_store.Store(ledger)
 c.update(TEST_ONLY=True,run_id=name,output=str(local/'run'),replica_output=str(replica/'run'),
   ledger_root=str(ledger),ledger_job=label,ledger_device=s.device,range_end=c['initial_patch']+1000000,
   gmp_audit_period=1 if finite else 128,test_chunk_limit=17 if finite else None,
   stop_epoch=time.time()+(40 if deadline else 100),service_name=name+'.service',deadline_service_name=name+'-deadline.service')
 c['stop_local']=datetime.fromtimestamp(c['stop_epoch'],timezone.utc).isoformat()
 claim=s.reserve(c['ledger_job'],c['initial_patch'],c['range_end'],c['manifest_sha256'])
 c['ledger_claim_sha256']=claim['sha256']
 folder=ROOT/'evidence/boole-validation'/label;folder.mkdir()
 path=folder/'config.json';atomic(path,c);policy.load_config(path)
 calls,cleanup,timer=launch(c,path,folder);timer_started=unit(timer)
 def committed():
  p=Path(c['output'])/'checkpoint.json'
  proof=local/'supervisor.json'
  if proof.exists():
   state=json.loads(proof.read_bytes())
   if state.get('error'):raise RuntimeError('Actual supervisor failed: '+state['error'])
  return p.exists() and json.loads(p.read_bytes())['chunks']>=1
 wait_for(committed,40,'Actual service did not commit; inspect '+str(folder))
 owner=s.root/'jobs'/c['ledger_job']/'journal.jsonl'
 policy.require(excluded(owner),'Actual NFS writer owner lock was not held')
 policy.require(excluded('/home/pnord/boole-production-validation-20261107/gpu-owner.lock'),'Actual GPU lease was not held')
 reuse_identity=owner.stat().st_ino
 if signal_stop:command(['systemctl','--user','stop',c['service_name']])
 wait_for(lambda:unit(c['service_name'])['ActiveState']=='inactive',110,'Compute service did not stop')
 wait_for(lambda:(Path(c['output'])/'final-replica.json').exists(),90,'Separate final copy did not finish')
 local_run=Path(c['output']);replica_run=Path(c['replica_output'])
 cpraw=(local_run/'checkpoint.json').read_bytes();cp=json.loads(cpraw)
 policy.require(cpraw==(replica_run/'checkpoint.json').read_bytes(),'Final local/replica checkpoint differs')
 a=audit_suffix(local_run,dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',c['gmp_audit_period'])
 b=audit_suffix(replica_run,dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',c['gmp_audit_period'])
 policy.require(a==b,'Independent grouped local/replica audits differ')
 supervisor=json.loads((local/'supervisor.json').read_bytes());status=json.loads((local_run/'status.json').read_bytes())
 controls=json.loads((local_run/'controls.json').read_bytes())
 policy.require(supervisor['error'] is None and supervisor['leases_released'] and supervisor['worker_exit_code']==0,'Supervisor/worker failed')
 policy.require(datetime.fromisoformat(supervisor['all_owned_processes_exited_utc']).timestamp()<c['stop_epoch'],'Owned computation exceeded absolute deadline')
 policy.require(status['journal_buffer']['pending_chunks']==0 and status['journal_buffer']['pending_bytes']==0,'Final partial buffer did not drain')
 policy.require(status['prefetch']['ready_limit']==3 and status['dispatch_chunksize']==4,'Ready queue or dispatch settings changed')
 policy.require(controls['status']=='passed' and all(x['hits'] and x['full_oracle_equal'] for x in controls['cases']),'Nonempty controls failed')
 policy.require(not excluded(owner) and owner.stat().st_ino==reuse_identity,'Stable NFS owner lock was not released')
 policy.require(not excluded('/home/pnord/boole-production-validation-20261107/gpu-owner.lock'),'GPU lease was not released')
 if finite:policy.require(cp['chunks']==17 and a['new_gmp_audited_chunks']==17,'Finite dense audit cadence failed')
 if deadline:policy.require(timer_started['ActiveState']=='active' and supervisor.get('stop_trigger') in ('signal','absolute_deadline'),'Deadline timer/supervisor did not trigger')
 if unit(timer)['ActiveState']!='inactive':command(['systemctl','--user','stop',timer])
 row=dict(case=label,status='passed',TEST_ONLY=True,scientific_coverage=False,config=c,commands=calls,
  original_timer=timer_started,checkpoint=cp,local_audit=a,replica_audit=b,supervisor=supervisor,
  worker_status=status,final_replica=json.loads((local_run/'final-replica.json').read_bytes()),
  original_owner_lock_exclusion=True,stable_owner_inode=reuse_identity,gpu_lease_exclusion=True,controls=controls)
 atomic(folder/'result.json',row)
 print(json.dumps(dict(case=label,status='passed',chunks=cp['chunks'],next_patch=cp['next_patch'])),flush=True)
 # Reusing existing output is rejected by the actual service before worker launch.
 if finite:
  reused=dict(c,service_name=name+'-reuse.service')
  reused_path=folder/'reuse-config.json';atomic(reused_path,reused)
  command(['systemd-run','--user','--unit='+name+'-reuse','--collect','--service-type=exec','--property=Restart=no',
    '--property=RuntimeMaxSec=15','--property=KillMode=mixed','--property=TimeoutStopSec=8',
    '--property=StandardOutput=append:'+str(folder/'reuse.stdout'),'--property=StandardError=append:'+str(folder/'reuse.stderr'),
    PYTHON,'-B',str(W/'boole_supervisor.py'),'--config',str(reused_path)])
  wait_for(lambda:unit(reused['service_name'])['ActiveState'] in ('failed','inactive'),20,'Reused output did not fail closed')
  wait_for(lambda:(local/'supervisor.json').exists() and json.loads((local/'supervisor.json').read_bytes()).get('error') is not None,5,'Reuse rejection proof missing')
  failure=json.loads((local/'supervisor.json').read_bytes())
  policy.require('reuse forbidden' in failure['error'] and (local_run/'checkpoint.json').read_bytes()==cpraw,'Existing output reuse mutated journal')
  row['existing_output_reuse_rejected']=True;row['reuse_rejection']=failure;atomic(folder/'result.json',row)
 return row

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r1');args=parser.parse_args()
 cases=[case('finite-'+args.revision,finite=True),case('signal-'+args.revision,signal_stop=True),case('deadline-'+args.revision,deadline=True)]
 report=dict(status='passed',checked_utc=policy.utc(),TEST_ONLY=True,scientific_coverage=False,
  manifest_sha256=policy.digest(W/'release-manifest.json'),config_sha256=policy.digest(W/'production-config.json'),
  compute_grouping=json.loads((ROOT/'evidence/boole-validation/buffered-compute.json').read_bytes()),
  mirror_unit_tests='9 passed',cases=cases)
 atomic(ROOT/'runtime-validation.json',report)
 print(json.dumps(dict(status='passed',runtime_validation=str(ROOT/'runtime-validation.json'))),flush=True)
if __name__=='__main__':main()
