"""Read-only Boole progress collector; no search locks, recovery, or Git credentials."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time,fcntl
ROOT=Path(__file__).resolve().parent
SHARE=Path('/mnt/nfs_share/boole-bulk-publishing-20261108')
CONFIG=ROOT/'worker/production-config.json'
def utc():return datetime.now(timezone.utc).isoformat()
def atomic(path,obj):
 temp=path.with_name(path.name+'.'+str(os.getpid())+'.tmp')
 with temp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(temp,path)
def show(unit):
 p=subprocess.run(['systemctl','--user','show',unit,'--property=ActiveState,SubState,MainPID,NRestarts'],capture_output=True,text=True,timeout=5,check=True)
 return dict(x.split('=',1) for x in p.stdout.splitlines() if '=' in x)
def snapshot():
 raw=CONFIG.read_bytes();c=json.loads(raw);folder=Path(c['output']);cp=json.loads((folder/'checkpoint.json').read_text());status=json.loads((folder/'status.json').read_text());supervisor=json.loads((folder.parent/'supervisor.json').read_text())
 config_hash=hashlib.sha256(raw).hexdigest()
 if config_hash!=supervisor['config_sha256']:raise RuntimeError('Frozen config changed')
 if cp['identity']['trial']!=c['run_id'] or status['run_id']!=c['run_id'] or cp['identity']['source_identity']!=status['source_identity']:raise RuntimeError('Source/run identity mismatch')
 if cp['next_patch']-c['initial_patch']!=cp['patches']:raise RuntimeError('Checkpoint patch count mismatch')
 expected=hashlib.sha256(json.dumps(dict(manifest_sha256=c['manifest_sha256'],config=c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 if cp['identity']['source_identity']!=expected:raise RuntimeError('Unexpected frozen worker identity')
 service=show(c['service_name']);timer=show(c['deadline_service_name'].removesuffix('.service')+'.timer');active=service['ActiveState'] in ('active','activating','deactivating')
 alerts=[]
 for name,row in [('worker',status),('supervisor',supervisor)]:
  if row.get('error'):alerts.append(name+': '+str(row['error']))
  if active and time.time()-datetime.fromisoformat(row['updated_utc']).timestamp()>120:alerts.append(name+' status is stale')
 if active and timer['ActiveState']!='active':alerts.append('Deadline timer inactive')
 return dict(snapshot_utc=utc(),host='boole',TEST_ONLY=False,run_id=c['run_id'],phase=('attention_required' if alerts else 'running') if active else 'stopped',alerts=alerts,service=service,deadline_timer=timer,stop_local=c['stop_local'],stop_epoch=c['stop_epoch'],workers=c['workers'],backend=c['backend'],geometry_policy=c['geometry_policy'],manifest_sha256=c['manifest_sha256'],config_sha256=config_hash,source_identity=status['source_identity'],ledger_claim_sha256=c['ledger_claim_sha256'],reserved_interval=[c['initial_patch'],c['range_end']],committed_interval=[c['initial_patch'],cp['next_patch']],checkpoint=cp,worker_metrics={k:status[k] for k in ['updated_utc','patches_per_second','gmp_audited_chunks','search_seconds','error','reason']},supervisor=supervisor,journal_limit_bytes=c['journal_limit_bytes'],minimum_free_disk_bytes=c['minimum_free_disk_bytes'],free_disk_bytes=__import__('shutil').disk_usage(folder).free,load_average=os.getloadavg(),completed_bound=None,coverage_scope='Boole continuation under original reservation; includes separately sealed parent interval; Ada coverage is separate; no full-box bound.',parent_committed_interval=[c['reservation_initial_patch'],c['initial_patch']],combined_committed_interval=[c['reservation_initial_patch'],cp['next_patch']],combined_selected_patches=c['parent_selected_patches']+cp['patches'],parent_audit_sha256=c['parent_audit_sha256'],bulk_storage_root='/mnt/fifth42-storage',parent_archive=c['parent_run'],parent_archive_receipt_sha256=c['parent_archive_receipt_sha256'],lineage_sha256=c['lineage_sha256'],claimed_interval=[c['reservation_initial_patch'],c['range_end']],report_interval_seconds=900)
def main():
 SHARE.mkdir(mode=0o700,exist_ok=True)
 with (ROOT/'collector.lock').open('a+') as lock:
  fcntl.lockf(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  while True:
   try:
    row=snapshot();atomic(SHARE/'status.json',row);atomic(SHARE/'collector-health.json',dict(status='ok',updated_utc=utc()))
    if row['phase']=='stopped':return 0
   except Exception as e:atomic(SHARE/'collector-health.json',dict(status='error',updated_utc=utc(),error=repr(e)))
   if time.time()>1794236400+1800:return 2
   time.sleep(15)
if __name__=='__main__':raise SystemExit(main())
