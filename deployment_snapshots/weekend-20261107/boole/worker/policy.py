"""Boole derivative: immutable source, explicit interval, actual shared ledger."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,time
ROOT=Path(__file__).resolve().parent
class RequestedStop(Exception):pass
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def stable(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def utc():return datetime.now(timezone.utc).isoformat()
def verify_sources(c):
 p=ROOT/'boole-release-manifest.json';require(digest(p)==c['manifest_sha256'],'Release manifest changed')
 m=json.loads(p.read_text())
 for n,h in m['files'].items():require(digest(ROOT/n)==h,'Frozen source changed: '+n)
 return m
def validate_parent(c):
 p=Path(c['coverage_file']);require(digest(p)==c['coverage_sha256'],'Final Ada coverage changed')
 m=json.loads(p.read_text());require(m['status']=='verified_receipts' and m['final_checkpoint'] is True,'Final coverage missing')
 require(m['covered_intervals']==[[3750000000,3917103232]],'Historical coverage changed')
 require(3000000000<=c['initial_patch']<c['range_end']<=3750000000,'Boole interval outside disjoint range')
 return m
def validate_ledger(c):
 import ada_export_store as w
 s=w.Store(c['ledger_root']);until=time.monotonic()+2
 while True:
  try:r=s.claim(c['ledger_job']);break
  except w.Busy:
   if time.monotonic()>until:raise
   time.sleep(.02)
 require(s.device==c['ledger_device'],'Shared filesystem changed')
 require(r['sha256']==c['ledger_claim_sha256'] and (r['first'],r['last'],r['identity'])==(c['initial_patch'],c['range_end'],c['manifest_sha256']),'Reservation changed')
 require(r['coverage']==dict(sha256=c['coverage_sha256'],manifest=json.loads(Path(c['coverage_file']).read_text())),'Coverage link changed')
 return s,r
def load_config(path):
 c=json.loads(Path(path).read_text());require(os.uname().nodename.split('.')[0]=='boole','Wrong host')
 require(c['backend']=='gpu' and c['workers']==16 and c['physical_cpus']==list(range(16)),'CPU/GPU allocation changed')
 require(c['geometry_policy'] in ('baseline','adaptive'),'Unknown geometry policy')
 require((c['shell_lo'],c['shell_hi'],c['width'],c['bits'],c['cap'])==(100000000001,200000000000,8,222,42),'Exact geometry changed')
 require(c['chunk_patches']==256 and 1<=c['gmp_audit_period']<=128,'Checkpoint/audit interval changed')
 require(0<c['prep_load_ceiling']<=17 and c['prep_load_ceiling']<c['running_load_limit']<=20,'Load budget changed')
 require(time.time()<c['stop_epoch']<=1794236400 and abs(datetime.fromisoformat(c['stop_local']).timestamp()-c['stop_epoch'])<.001,'Deadline invalid')
 require(c['minimum_free_disk_bytes']>=8*1024**3 and 0<c['journal_limit_bytes']<=32*1024**3,'Storage budget invalid')
 expected=Path(c['ledger_root'])/'jobs'/c['ledger_job']/'run'
 require(Path(c['output']).resolve()==expected.resolve(),'Output must match reserved job')
 test=c.get('TEST_ONLY') is True
 if test:require(Path(c['ledger_root']).is_relative_to('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/boole-validation'),'Test ledger outside isolated namespace')
 else:
  require(c['ledger_root']=='/mnt/nfs_share/fifth42-shared-20261107','Wrong production ledger')
  require(c['geometry_policy']=='adaptive' and c.get('test_chunk_limit') is None,'Production policy changed')
 require(c['automatic_resume'] is False,'Automatic resume forbidden')
 verify_sources(c);validate_parent(c);validate_ledger(c);return c
def remaining(c,event,output,cap=30):
 if event.is_set() or (Path(output)/'STOP').exists():raise RequestedStop('Stop requested')
 if os.getloadavg()[0]>c['running_load_limit']:raise RequestedStop('Running CPU load budget exceeded')
 left=c['stop_epoch']-time.time()-8
 if left<=0:raise RequestedStop('Absolute deadline reached; final cleanup')
 return min(cap,left)
def check_storage(c,output):
 if shutil.disk_usage(output).free<c['minimum_free_disk_bytes']:raise RequestedStop('Free disk reserve reached')
 p=Path(output)/'coverage.jsonl'
 if p.exists() and p.stat().st_size>=c['journal_limit_bytes']:raise RequestedStop('Journal budget reached')
