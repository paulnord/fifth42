"""Read-only checks of active ownership, grouped receipts and replicated progress."""
import fcntl,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker';sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import policy,ada_export_store
from audit_grouped import audit_suffix
from durable_mirror import atomic
from validate_boole_services import unit,excluded

def captured(replica):
 until=time.monotonic()+10
 while time.monotonic()<until:
  try:
   raw=(replica/'checkpoint.json').read_bytes();cp=json.loads(raw);receipt=json.loads((replica/'replica-state.json').read_bytes())
   if hashlib.sha256(raw).hexdigest()==receipt['checkpoint_sha256']:return cp,receipt
  except FileNotFoundError:pass
  time.sleep(.1)
 raise RuntimeError('No consistent verified replica checkpoint')

def main():
 c=policy.load_config(W/'production-config.json');local=Path(c['output']);replica=Path(c['replica_output'])
 initial,receipt=captured(replica);end=time.monotonic()+100
 while time.monotonic()<end:
  cp,receipt=captured(replica)
  if cp['next_patch']>initial['next_patch']:break
  policy.require(unit(c['service_name'])['ActiveState']=='active','Production stopped while observing progress')
  time.sleep(2)
 else:raise RuntimeError('Verified replica cursor did not advance through another mirror interval')
 local_cp=json.loads((local/'checkpoint.json').read_bytes())
 fingerprint=hashlib.sha256(policy.stable(dict(manifest_sha256=c['manifest_sha256'],config=c)).encode()).hexdigest()
 policy.require(cp['identity']==dict(trial=c['run_id'],source_identity=fingerprint),'Captured runtime identity differs')
 baseline=dict(checkpoint=dict(next_patch=c['initial_patch']),config=c)
 a=audit_suffix(local,baseline,cp,'fresh',c['gmp_audit_period'])
 b=audit_suffix(replica,baseline,cp,'fresh',c['gmp_audit_period']);policy.require(a==b,'Local/replica captured-prefix audits differ')
 def digest_prefix(path,limit):
  h=hashlib.sha256()
  with path.open('rb') as f:
   while limit:
    data=f.read(min(limit,4*1024**2));policy.require(bool(data),'Truncated captured prefix');h.update(data);limit-=len(data)
  return h.hexdigest()
 policy.require(digest_prefix(local/'coverage.jsonl',cp['journal_offset'])==digest_prefix(replica/'coverage.jsonl',cp['journal_offset'])==receipt['raw_sha256'],'Raw committed prefix digest mismatch')
 owner=Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl'
 policy.require(excluded(owner),'Original NFS owner lock not held')
 policy.require(excluded('/home/pnord/boole-production-validation-20261107/gpu-owner.lock'),'Host GPU lease not held')
 pids=[int(p) for p in subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).split()]
 native=json.loads((local/'status.json').read_bytes());sup=json.loads((local.parent/'supervisor.json').read_bytes())
 policy.require(len(pids)==1 and os.getpgid(pids[0])==native['worker_pid'],'Unexpected GPU owner/group')
 policy.require(native['status']=='running' and native['error'] is None and sup['error'] is None,'Worker/supervisor not healthy')
 affinities=json.loads((local/'worker-affinities.json').read_bytes())
 policy.require(len(affinities)==16 and set(map(tuple,affinities.values()))=={(i,) for i in range(16)},'Physical CPU allocation changed')
 names=[c['service_name'],c['deadline_service_name'].replace('.service','.timer'),c['run_id']+'-final-copy.service','boole-overnight-collector-20261109.service']
 units={name:unit(name) for name in names};policy.require(all(u['ActiveState']=='active' for u in units.values()),'Worker, timer, cleanup or collector inactive')
 policy.require(units[c['service_name']]['Restart']=='no' and units[c['service_name']]['KillMode']=='mixed','Worker restart/stop policy changed')
 policy.require(time.time()-receipt['captured_epoch']<=300,'Verified replica too old')
 report=dict(status='passed',verified_utc=policy.utc(),run_id=c['run_id'],config_sha256=policy.digest(W/'production-config.json'),manifest_sha256=c['manifest_sha256'],
  source_identity=fingerprint,initial_patch=c['initial_patch'],local_next_patch=local_cp['next_patch'],replica_next_patch=cp['next_patch'],
  observed_replica_advance=cp['next_patch']-initial['next_patch'],replica_lag_seconds=time.time()-receipt['captured_epoch'],
  grouped_prefix_audit=a,raw_prefix_sha256=receipt['raw_sha256'],original_nfs_owner_lock_exclusion=True,owner_lock_inode=owner.stat().st_ino,
  gpu_lease_exclusion=True,gpu_pid=pids[0],physical_workers=16,group_limit=c['group_limit'],local_output=str(local),replica_output=str(replica),
  dispatch_chunksize=c['dispatch_chunksize'],ready_queue=native['prefetch'],journal_buffer=native['journal_buffer'],
  stop_local=c['stop_local'],final_copy_deadline='2026-11-10T17:30:00-06:00',units=units,completed_bound=None)
 atomic(ROOT/'LIVE_VERIFICATION.json',report)
 atomic(Path('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole/LIVE_VERIFICATION.json'),report)
 print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
