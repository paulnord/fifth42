"""Identity-pinned, read-only Cabbage collector. Never opens search journals."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,fcntl,hashlib,json,os,subprocess,time

def utc():return datetime.now(timezone.utc).isoformat()
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):
 p=Path(p);tmp=p.with_name(p.name+'.'+str(os.getpid())+'.tmp')
 with tmp.open('x') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(tmp,p);fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def show(unit):
 p=subprocess.run(['systemctl','--user','show',unit,'--property=ActiveState,SubState,MainPID,NRestarts'],text=True,capture_output=True,check=True,timeout=5)
 return dict(x.split('=',1) for x in p.stdout.splitlines() if '=' in x)
def snapshot(settings):
 raw=Path(settings['config']).read_bytes();c=json.loads(raw);config_hash=hashlib.sha256(raw).hexdigest()
 if config_hash!=settings['config_sha256']:raise RuntimeError('Frozen config changed')
 manifest=Path(settings['manifest']);manifest_hash=digest(manifest)
 if manifest_hash!=c['manifest_sha256'] or manifest_hash!=settings['manifest_sha256']:raise RuntimeError('Frozen manifest changed')
 runtime=manifest.parent
 for name,h in json.loads(manifest.read_text())['files'].items():
  if digest(runtime/name)!=h:raise RuntimeError('Frozen source/binary changed: '+name)
 expected=hashlib.sha256(json.dumps(dict(manifest_sha256=manifest_hash,config=c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 folder=Path(c['output']);service=show(settings['service_name']);timer=show(settings['deadline_timer_name'])
 active=service['ActiveState'] in ('active','activating','deactivating')
 base=dict(snapshot_utc=utc(),host='cabbage',TEST_ONLY=c.get('TEST_ONLY',False),run_id=c['run_id'],manifest_sha256=manifest_hash,config_sha256=config_hash,source_identity=expected,ledger_claim_sha256=c['ledger_claim_sha256'],reserved_interval=[c['reservation_initial_patch'],c['range_end']],parent_verified_interval=[c['reservation_initial_patch'],c['initial_patch']],parent_archive=c['parent_run'],parent_journal_sha256=c['parent_journal_sha256'],parent_audit_sha256=c['parent_audit_sha256'],reservation_manifest_sha256=c['reservation_manifest_sha256'],proposed_interval=None,workers=c['workers'],backend=c['backend'],geometry_policy=c['geometry_policy'],stop_local=c['stop_local'],stop_epoch=c['stop_epoch'],service=service,deadline_timer=timer,completed_bound=None,journal_limit_bytes=c['journal_limit_bytes'],minimum_free_disk_bytes=c['minimum_free_disk_bytes'],report_interval_seconds=900,coverage_scope='Cabbage archived parent plus fresh continuation; no full-box bound.',production_launched=False,mathematical_coverage_claim=False)
 if not (folder/'checkpoint.json').exists():
  base.update(phase='admitted_not_started' if not active else 'starting',alerts=[],committed_interval=[c['initial_patch'],c['initial_patch']],checkpoint=None,worker_metrics={},supervisor=None)
  return base
 cp=json.loads((folder/'checkpoint.json').read_text());status=json.loads((folder/'status.json').read_text());sup=json.loads((folder.parent/'supervisor.json').read_text())
 if sup['config_sha256']!=config_hash or status['run_id']!=c['run_id'] or cp['identity']!=dict(trial=c['run_id'],source_identity=expected) or status['source_identity']!=expected:raise RuntimeError('Worker/run/checkpoint identity mismatch')
 if cp['next_patch']-c['initial_patch']!=cp['patches'] or not c['initial_patch']<=cp['next_patch']<=c['range_end']:raise RuntimeError('Checkpoint interval/count mismatch')
 alerts=[]
 for name,row in [('worker',status),('supervisor',sup)]:
  if row.get('error'):alerts.append(name+': '+str(row['error']))
  if active and time.time()-datetime.fromisoformat(row['updated_utc']).timestamp()>120:alerts.append(name+' status stale')
 if active and timer['ActiveState']!='active':alerts.append('Deadline timer inactive')
 base.update(phase=('attention_required' if alerts else 'running') if active else 'stopped',alerts=alerts,committed_interval=[c['initial_patch'],cp['next_patch']],checkpoint=cp,supervisor=sup,worker_metrics={k:status[k] for k in ('updated_utc','patches_per_second','gmp_audited_chunks','search_seconds','error','reason')},production_launched=not c.get('TEST_ONLY',False),load_average=os.getloadavg())
 return base

def main():
 p=argparse.ArgumentParser();p.add_argument('--settings',required=True,type=Path);p.add_argument('--once',action='store_true');a=p.parse_args()
 settings_raw=a.settings.read_bytes();settings=json.loads(settings_raw);out=Path(settings['output']);out.mkdir(mode=0o700,parents=True,exist_ok=True)
 with (out/'collector.lock').open('a+') as lock:
  fcntl.lockf(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  while True:
   try:
    if a.settings.read_bytes()!=settings_raw:raise RuntimeError('Collector settings changed')
    row=snapshot(settings);atomic(out/'status.json',row);atomic(out/'collector-health.json',dict(status='ok',updated_utc=utc(),config_sha256=row['config_sha256']))
    if a.once or row['phase']=='stopped':return 0
   except Exception as e:
    atomic(out/'collector-health.json',dict(status='error',updated_utc=utc(),error=repr(e)))
    if a.once:return 2
   if time.time()>settings['stop_epoch']+1800:return 2
   time.sleep(15)
if __name__=='__main__':raise SystemExit(main())
