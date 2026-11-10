"""Cabbage continuation: original NFS claim, local journal, verified NFS replica."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,os,shutil,subprocess,time
ROOT=Path(__file__).resolve().parent
LOCAL=Path('/home/pnord/fifth42-local-runs');BULK=Path('/mnt/fifth42-storage')
SHARED=Path('/mnt/nfs_share/fifth42-shared-20261107')
JOB='cabbage-extended-allocation-20261109'
CLAIM='8f413e93a894f1f7442e63afdbbfc283759f9f6569bedf1de8a4f4c9b59bbbdd'
RESERVATION='69c042a8cbe018e0cd8a7cb81477739e1db9fbaa603f77f97ad1afd75309cdbe'
FIRST=500000000;LAST=2250000000;DEADLINE=1794351600
class RequestedStop(Exception):pass
def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for data in iter(lambda:f.read(4*1024**2),b''):h.update(data)
    return h.hexdigest()
def stable(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def utc():return datetime.now(timezone.utc).isoformat()
def verify_sources(c):
    require(Path(c['manifest']).resolve()==ROOT/'release-manifest.json','Wrong runtime manifest')
    require(digest(c['manifest'])==c['manifest_sha256'],'Frozen release manifest changed')
    m=json.loads(Path(c['manifest']).read_bytes())
    for name,h in m['files'].items():require(digest(ROOT/name)==h,'Frozen source changed: '+name)
    return m
def validate_archive(c):
    p=Path(c['parent_archive_receipt']);require(digest(p)==c['parent_archive_receipt_sha256'],'Parent archive receipt changed')
    r=json.loads(p.read_bytes());require(r['status']=='verified' and r['source_closed'] and r['source_retained'],'Unverified parent archive')
    require((r['raw_sha256'],r['committed_bytes'],r['captured_checkpoint_sha256'])==(c['parent_journal_raw_sha256'],c['parent_journal_offset'],c['parent_checkpoint_sha256']),'Parent archive provenance changed')
    st=(Path(c['parent_run'])/'coverage.jsonl').stat()
    require([st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns]==c['parent_journal_identity'],'Sealed archive inode/bytes/timestamps changed')
    return r
def validate_parent(c,full=True):
    parent=Path(c['parent_run']).resolve();require(parent.is_relative_to(BULK/'archives'),'Parent outside retained bulk archives')
    require(digest(parent/'checkpoint.json')==c['parent_checkpoint_sha256'] and digest(parent/'status.json')==c['parent_status_sha256'],'Sealed parent checkpoint/status changed')
    cp=json.loads((parent/'checkpoint.json').read_bytes());status=json.loads((parent/'status.json').read_bytes())
    require(status['status']=='stopped' and status['error'] is None,'Parent worker did not stop successfully')
    require(cp['identity']==c['parent_identity'] and cp['completed_bound'] is None and cp['next_patch']==c.get('parent_final_cursor',c['initial_patch']),'Parent cursor or identity changed')
    require((cp['journal_sha256'],cp['journal_offset'])==(c['parent_journal_sha256'],c['parent_journal_offset']),'Parent committed prefix changed')
    require(c['parent_selected_patches']==(0 if c.get('fresh_reservation') else c['initial_patch']-FIRST),'Parent logical lineage changed')
    require(digest(c['parent_audit_file'])==c['parent_audit_sha256'],'Final parent audit changed')
    audit=json.loads(Path(c['parent_audit_file']).read_bytes())
    require(audit['status']=='passed' and audit['final_checkpoint'] and audit['uncommitted_trailing_bytes']==0,'Final audit incomplete')
    require((audit['captured_checkpoint_sha256'],audit['committed_chain_sha256'],audit['committed_raw_sha256'],audit['committed_bytes'],audit['selected_interval'][1])==(c['parent_checkpoint_sha256'],c['parent_journal_sha256'],c['parent_journal_raw_sha256'],c['parent_journal_offset'],c.get('parent_final_cursor',c['initial_patch'])),'Final audit provenance changed')
    q=audit['quiescence'];require(q['original_owner_lock_acquired'] and q['gpu_lease_acquired'] and not q['gpu_compute_processes'] and q['worker_exit_code']==0 and q['worker_leases_released'],'Parent quiescence missing')
    validate_archive(c);return cp
def validate_output(c):
    if c.get('TEST_ONLY') is True:
        expected=LOCAL/'TEST_ONLY_cabbage_extended_20261109'/c['run_id']/'run'
        replica=BULK/'TEST_ONLY_cabbage_extended_20261109'/c['run_id']/'run'
    else:
        expected=LOCAL/JOB/c['run_id']/'run';replica=BULK/'runs'/JOB/c['run_id']/'run'
    require(Path(c['output']).resolve()==expected and Path(c['replica_output']).resolve()==replica,'Output escaped its reserved directory')
    require(expected.parent.stat().st_dev==c['local_data_device'],'Local device changed')
    fs=subprocess.check_output(['findmnt','-n','-o','FSTYPE','-T',str(expected.parent)],text=True,timeout=5).strip()
    require(fs in ('ext4','xfs','btrfs','zfs'),'Journal is not on an actual local filesystem')
    import bulk_data_store as bulk
    require(bulk.verify_share(replica)==c['data_device'],'Bulk replica mount/device changed')
    return expected
def validate_ledger(c):
    import ada_export_store as store_module
    require(c['ledger_root']==str(SHARED) and c['ledger_job']==JOB and c['ledger_claim_sha256']==CLAIM,'Original shared owner/claim changed')
    require(digest(c['origin_claim_file'])==c['origin_claim_file_sha256'],'Original claim proof changed')
    original=json.loads(Path(c['origin_claim_file']).read_bytes());store=store_module.Store(c['ledger_root'])
    require(store.device==c['ledger_device'],'Coordinator mount identity changed')
    until=time.monotonic()+2
    while True:
        try:claim=store.claim(JOB);break
        except store_module.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.02)
    require(claim==original and (claim['first'],claim['last'],claim['identity'],claim['sha256'])==(FIRST,LAST,RESERVATION,CLAIM),'Original reservation inheritance changed')
    require(digest(c['coverage_file'])==c['coverage_sha256'],'Original admission coverage proof changed')
    require(claim['coverage']==dict(sha256=c['coverage_sha256'],manifest=json.loads(Path(c['coverage_file']).read_bytes())),'Original admission coverage link changed')
    require(FIRST<=c['initial_patch']<c['range_end']<=LAST,'Continuation outside original reservation')
    return store,claim
def load_config(path):
    c=json.loads(Path(path).read_bytes());base=json.loads((ROOT/'base-config.json').read_bytes())
    require(os.uname().nodename.split('.')[0]=='cabbage','Wrong actual host')
    if c.get('TEST_ONLY') is True:
        allowed={'TEST_ONLY','run_id','output','replica_output','range_end','gmp_audit_period','test_chunk_limit','stop_epoch','stop_local','service_name','deadline_service_name','cleanup_service_name','group_limit'}
        require(all(c.get(k)==v for k,v in base.items() if k not in allowed),'Test changed frozen parent/geometry/resources')
        require(c['run_id'].startswith('cabbage-extended-test-'),'Wrong test namespace')
    else:
        require(c==base and c['run_id'].startswith('cabbage-extended-') and c.get('test_chunk_limit') is None,'Production differs from frozen base')
        require(c['stop_epoch']==DEADLINE and c['range_end']==LAST,'Production deadline or endpoint changed')
    require(c['backend']=='gpu' and c['workers']==16 and c['physical_cpus']==list(range(16)),'CPU/GPU budget changed')
    require((c['shell_lo'],c['shell_hi'],c['width'],c['bits'],c['cap'],c['chunk_patches'],c['geometry_policy'])==(100000000001,200000000000,8,222,42,256,'adaptive'),'Arithmetic/logical grid changed')
    require(c['dispatch_chunksize']==4 and c['ready_queue_limit']==3 and c['journal_buffer_records']==8 and c['journal_buffer_bytes']==8388608 and c['journal_buffer_max_age_seconds']==.25 and c['preparation_windows']==1 and c['gpu_request_windows']==1,'Buffered pipeline policy changed')
    require(c['group_limit'] in (1,2,4) and c['replica_interval_seconds']==60 and c['maximum_replica_lag_seconds']==300,'Unsupported grouping/replication policy')
    require(0<c['prep_load_ceiling']<=17 and c['prep_load_ceiling']<c['running_load_limit']<=20,'CPU load budget changed')
    require(0<c['journal_limit_bytes']<=32*1024**3 and c['minimum_free_disk_bytes']>=16*1024**3,'Local journal budget/reserve changed')
    require(time.time()<c['stop_epoch']<=DEADLINE and abs(datetime.fromisoformat(c['stop_local']).timestamp()-c['stop_epoch'])<.001,'Deadline changed or expired')
    require(c['automatic_resume'] is False and 1<=c['gmp_audit_period']<=128,'Resume/audit policy changed')
    require(c.get('test_chunk_limit') is None or 1<=c['test_chunk_limit']<=32,'Invalid finite test limit')
    require(not Path(c['output']).exists(),'Existing output cannot be reused')
    require(not Path(c['replica_output']).exists(),'Existing replica cannot be reused for a fresh run')
    validate_output(c);verify_sources(c);validate_parent(c);validate_ledger(c)
    return c
def remaining(c,event,output,cap=30):
    if event.is_set() or (Path(output)/'STOP').exists():raise RequestedStop('Stop requested')
    if os.getloadavg()[0]>c['running_load_limit']:raise RequestedStop('Running CPU load budget exceeded')
    left=c['stop_epoch']-time.time()-10
    if left<=0:raise RequestedStop('Absolute deadline reached; final cleanup')
    return min(cap,left)
def check_storage(c,output):
    require(Path(output).stat().st_dev==c['local_data_device'] and BULK.stat().st_dev==c['data_device'],'Local/replica device changed')
    for p in (output,c['replica_output']):
        ancestor=Path(p)
        while not ancestor.exists():ancestor=ancestor.parent
        if shutil.disk_usage(ancestor).free<c['minimum_free_disk_bytes']:raise RequestedStop('Storage free reserve reached')
    p=Path(output)/'coverage.jsonl'
    if p.exists() and p.stat().st_size>=c['journal_limit_bytes']:raise RequestedStop('Local journal byte cap reached')
