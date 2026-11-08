"""Frozen bulk continuation; immutable parent archive and original claim/owner lock."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,time
import bulk_data_store as bulk
ROOT=Path(__file__).resolve().parent
DEADLINE=1794236400
ORIGINAL_JOB='cabbage-saved-root-20261108T222040Z'
ORIGINAL_MANIFEST='a0000b2ed70ea7566baa2c6c0a00bd8cdcbc726f53bdf1247b7b9587eb5d6932'
ORIGINAL_CLAIM='364221db0023ea69fa18b47eb512e9e83362f6d598fc19c101e74b72f4f3d1c8'
ORIGINAL_CONFIG='b5a5c0925333007544d193183b70fc4389614e23a7fb456a991dc459b56de808'
ORIGINAL_SOURCE='1447da0f79576051a0361ade79a0206b3d29cc85d1829e6436eabae628747751'
FIRST=2250000000;LAST=3000000000
TEST_ROOT=Path('/mnt/fifth42-storage/TEST_ONLY_cabbage_bulk_20261108_98XhJJdw')
_verified_raw=set()
class RequestedStop(Exception):pass
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as stream:
  for block in iter(lambda:stream.read(8*1024**2),b''):h.update(block)
 return h.hexdigest()
def stable(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def utc():return datetime.now(timezone.utc).isoformat()
def verify_sources(c):
 path=ROOT/'cabbage-release-manifest.json';require(digest(path)==c['manifest_sha256'],'Release manifest changed')
 m=json.loads(path.read_text())
 for name,h in m['files'].items():require(digest(ROOT/name)==h,'Frozen source changed: '+name)
 return m
def validate_output(c):
 path=Path(c['output']).resolve()
 if c.get('TEST_ONLY') is True:
  require(path.is_relative_to(TEST_ROOT),'TEST_ONLY output outside dedicated bulk namespace')
 else:
  require(path==Path('/mnt/fifth42-storage/runs')/ORIGINAL_JOB/c['run_id']/'run','Bulk continuation output path changed')
 device=bulk.verify_share(path)
 require(device==c['output_device'],'Bulk filesystem identity changed')
 return path

def validate_links(c,cp,status,audit,receipt,supervisor,quiescence=None,recovery=None):
 require(audit['status']=='verified_final_prefix' and audit['source_closed'] is True,'Final parent audit missing')
 require(receipt['status']=='verified' and receipt['source_closed'] is True and receipt['source_retained'] is True,'Final closed-parent archive missing')
 require(audit['run_id']==ORIGINAL_JOB and audit['manifest_sha256']==ORIGINAL_MANIFEST and audit['config_sha256']==ORIGINAL_CONFIG and audit['source_identity']==ORIGINAL_SOURCE,'Parent runtime provenance changed')
 require(cp['identity']==dict(trial=ORIGINAL_JOB,source_identity=ORIGINAL_SOURCE),'Parent checkpoint identity changed')
 require(cp['completed_bound'] is None and status['error'] is None and supervisor['error'] is None,'Parent has mathematical/runtime errors')
 clean=status['status']=='stopped' and supervisor.get('leases_released') is True and supervisor.get('worker_exit_code')==0
 if not clean:
  require(quiescence is not None and recovery is not None,'Unclean parent requires independent quiescence and recovery review')
  require(quiescence['status']=='VERIFIED_QUIESCENT_AFTER_STOP_TIMEOUT' and quiescence['original_owner_lock_acquired'] is True and quiescence['gpu_lease_acquired'] is True and quiescence['gpu_compute_processes']==[],'Parent physical ownership not released')
  require('MainPID=0' in quiescence['unit_state'] and 'Result=timeout' in quiescence['unit_state'],'Unexpected terminal service evidence')
  require(quiescence['checkpoint_sha256']==c['parent_checkpoint_sha256'] and quiescence['journal_bytes']==c['parent_journal_offset'],'Quiescence binds a different checkpoint')
  require(recovery['status']=='verified_final_checkpoint_safe_for_fresh_continuation' and recovery['original_stop']=='systemd_stop_timeout','Recovery review missing')
  require(recovery['parent_archive_receipt_sha256']==c['parent_archive_receipt_sha256'] and recovery['parent_checkpoint_sha256']==c['parent_checkpoint_sha256'] and recovery['parent_journal_raw_sha256']==c['parent_journal_raw_sha256'] and recovery['parent_journal_offset']==c['parent_journal_offset'],'Recovery review provenance changed')
  require(recovery['parent_quiescence_receipt_sha256']==c['parent_quiescence_receipt_sha256'],'Recovery quiescence identity changed')
  require(all(recovery['reviewed_checks'][k] is True for k in ('all_committed_bytes_accounted','full_chain_counts_verified','no_trailing_bytes','source_files_unchanged','owner_and_gpu_locks_released','new_KillMode_mixed_test_passed')),'Recovery checks incomplete')
 require(supervisor['config_sha256']==ORIGINAL_CONFIG,'Parent supervisor config changed')
 require(status['next_patch']<=cp['next_patch']==audit['next_patch']==receipt['captured_next_patch']==c['initial_patch'],'Continuation gap or overlap with final parent cursor')
 if clean:require(status['next_patch']==cp['next_patch'],'Clean parent status cursor changed')
 require(cp['patches']==cp['next_patch']-FIRST==c['parent_selected_patches'],'Inherited parent total changed')
 require(cp['journal_sha256']==audit['journal_sha256']==receipt['journal_chain_sha256']==c['parent_journal_sha256'],'Parent journal chain changed')
 require(cp['journal_offset']==audit['journal_offset']==receipt['committed_bytes']==c['parent_journal_offset'],'Parent journal length changed')
 require(audit['raw_sha256']==receipt['raw_sha256']==c['parent_journal_raw_sha256'],'Archived raw journal bytes changed')
 require(audit['checkpoint_sha256']==receipt['captured_checkpoint_sha256']==c['parent_checkpoint_sha256'],'Parent checkpoint hash link changed')
 require(FIRST<c['initial_patch']<c['range_end']==LAST,'Continuation outside original claim')
 require(c['reservation_manifest_sha256']==ORIGINAL_MANIFEST and c['reservation_initial_patch']==FIRST and c['ledger_claim_sha256']==ORIGINAL_CLAIM and c['ledger_job']==ORIGINAL_JOB,'Original claim lineage changed')

def validate_parent(c,full=True):
 archive=Path(c['parent_run']).resolve()
 require(archive.is_relative_to('/mnt/fifth42-storage/archives'),'Parent must be the verified bulk archive')
 require(bulk.verify_share(archive)==c['output_device'],'Parent archive filesystem changed')
 for name,key in [('checkpoint.json','parent_checkpoint_sha256'),('status.json','parent_status_sha256'),('parent-audit.json','parent_audit_sha256'),('ARCHIVE_RECEIPT.json','parent_archive_receipt_sha256'),('supervisor.json','parent_supervisor_sha256')]:require(digest(archive/name)==c[key],'Archived parent metadata changed: '+name)
 cp=json.loads((archive/'checkpoint.json').read_text());status=json.loads((archive/'status.json').read_text());audit=json.loads((archive/'parent-audit.json').read_text());receipt=json.loads((archive/'ARCHIVE_RECEIPT.json').read_text());sup=json.loads((archive/'supervisor.json').read_text())
 require(digest(archive/'configuration.json')==ORIGINAL_CONFIG and digest(archive/'source-manifest.json')==ORIGINAL_MANIFEST,'Archived parent configuration/source identity changed')
 require(digest(archive/'QUIESCENCE_RECEIPT.json')==c['parent_quiescence_receipt_sha256'],'Quiescence receipt changed')
 require(Path(c['parent_recovery_review']).resolve()==ROOT/'recovery-acceptance.json' and digest(c['parent_recovery_review'])==c['parent_recovery_review_sha256'],'Recovery acceptance changed')
 validate_links(c,cp,status,audit,receipt,sup,json.loads((archive/'QUIESCENCE_RECEIPT.json').read_text()),json.loads(Path(c['parent_recovery_review']).read_text()))
 for name,h in receipt['metadata_sha256'].items():require(digest(archive/name)==h,'Archived metadata readback changed: '+name)
 require(digest(archive/'independent-audits.tar')==receipt['audit_tar_sha256'],'Archived GMP receipts changed')
 journal=archive/'coverage.jsonl';st=journal.stat()
 require(st.st_size==c['parent_journal_offset'] and st.st_ino==c['parent_archive_journal_inode'] and st.st_mtime_ns==c['parent_archive_journal_mtime_ns'],'Archived journal file identity changed')
 key=(str(journal),st.st_ino,st.st_size,st.st_mtime_ns,c['parent_journal_raw_sha256'])
 if full and key not in _verified_raw:
  require(digest(journal)==c['parent_journal_raw_sha256'],'Archived journal SHA256 changed');_verified_raw.add(key)
 return cp

def validate_ledger(c):
 import ada_export_store as small
 require(c['ledger_root']=='/mnt/nfs_share/fifth42-shared-20261107','Original coordinator moved')
 require(c['ledger_job']==ORIGINAL_JOB and c['ledger_claim_sha256']==ORIGINAL_CLAIM,'Original claim changed')
 s=small.Store(c['ledger_root']);until=time.monotonic()+2
 while True:
  try:claim=s.claim(c['ledger_job']);break
  except small.Busy:
   if time.monotonic()>until:raise
   time.sleep(.02)
 require(s.device==c['ledger_device'],'Coordinator filesystem identity changed')
 require((claim['first'],claim['last'],claim['identity'],claim['sha256'])==(FIRST,LAST,ORIGINAL_MANIFEST,ORIGINAL_CLAIM),'Original reservation changed')
 require(claim['coverage']==dict(sha256=c['coverage_sha256'],manifest=json.loads(Path(c['coverage_file']).read_text())),'Original admission provenance changed')
 require(digest(c['coverage_file'])==c['coverage_sha256'],'Admission metadata changed')
 return s,claim

def load_config(path):
 c=json.loads(Path(path).read_text());require(os.uname().nodename.split('.')[0]=='cabbage','Wrong host')
 require(c['run_id']!=ORIGINAL_JOB and c['run_id'].startswith('cabbage-bulk-'),'Fresh continuation run ID required')
 require(c['backend']=='gpu' and c['workers']==16 and c['physical_cpus']==list(range(16)),'CPU/GPU budget changed')
 require((c['shell_lo'],c['shell_hi'],c['width'],c['bits'],c['cap'],c['geometry_policy'])==(100000000001,200000000000,8,222,42,'adaptive'),'Exact geometry changed')
 require(c['chunk_patches']==256 and 1<=c['gmp_audit_period']<=128,'Checkpoint/audit guard changed')
 require(0<c['prep_load_ceiling']<=17 and c['prep_load_ceiling']<c['running_load_limit']<=20,'Load budget changed')
 require(time.time()<c['stop_epoch']<=DEADLINE and abs(datetime.fromisoformat(c['stop_local']).timestamp()-c['stop_epoch'])<.001,'Original deadline changed/expired')
 if c.get('TEST_ONLY') is not True:require(c['stop_epoch']==DEADLINE and c.get('test_chunk_limit') is None,'Production deadline/test policy changed')
 require(0<c['journal_limit_bytes']<=128*1024**3 and c['minimum_free_disk_bytes']>=8*1024**3,'Bulk journal/storage budget changed')
 require(c['automatic_resume'] is False,'Automatic resume forbidden')
 validate_output(c);verify_sources(c);validate_parent(c);validate_ledger(c)
 return c

def remaining(c,event,output,cap=30):
 if event.is_set() or (Path(output)/'STOP').exists():raise RequestedStop('Stop requested')
 if os.getloadavg()[0]>c['running_load_limit']:raise RequestedStop('Running CPU load budget exceeded')
 left=c['stop_epoch']-time.time()-8
 if left<=0:raise RequestedStop('Absolute deadline reached; final cleanup')
 return min(cap,left)
def check_storage(c,output):
 validate_output(c)
 if shutil.disk_usage(output).free<c['minimum_free_disk_bytes']:raise RequestedStop('Bulk free disk reserve reached')
 path=Path(output)/'coverage.jsonl'
 if path.exists() and path.stat().st_size>=c['journal_limit_bytes']:raise RequestedStop('Bulk journal budget reached')
