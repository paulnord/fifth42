"""Ada root-reuse continuation: inherited claim, audited parent, frozen per-run deadline."""
from datetime import datetime,timezone
import hashlib,json,os,shutil,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BULK=Path('/mnt/localstorage/pnord/fifth42-storage')
SHARED=Path('/mnt/nfs_share/fifth42-shared-20261107')
TEST_LEDGER=Path('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/ada-group4-validation')
LOCAL=Path('/home/pnord/fifth42-local-runs')
class RequestedStop(Exception):pass
def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024**2),b''):value.update(block)
    return value.hexdigest()
def stable(value):return json.dumps(value,sort_keys=True,separators=(',',':'))
def utc():return datetime.now(timezone.utc).isoformat()

def validate_archive(config):
    path=Path(config['parent_archive_receipt'])
    require(digest(path)==config['parent_archive_receipt_sha256'],'Verified archive receipt changed')
    receipt=json.loads(path.read_bytes())
    require(receipt['status']=='verified' and receipt['raw_sha256']==config['parent_journal_raw_sha256'] and
            receipt['committed_bytes']==config['parent_journal_offset'] and
            receipt['captured_checkpoint_sha256']==config['parent_checkpoint_sha256'],
            'Archive receipt does not identify the sealed parent')
    stat=(Path(config['parent_run'])/'coverage.jsonl').stat()
    actual=[stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns]
    require(actual==config['parent_journal_identity'],'Verified archive inode/bytes/timestamps changed')
    return receipt

def verify_sources(config):
    path=Path(config['manifest'])
    require(digest(path)==config['manifest_sha256'],'Frozen release manifest changed')
    manifest=json.loads(path.read_bytes())
    for name,expected in manifest['files'].items():
        require(digest(ROOT/name)==expected,'Frozen runtime source/binary changed: '+name)
    for name,expected in manifest.get('external_files',{}).items():
        require(digest(name)==expected,'External resource helper changed: '+name)
    return manifest

def validate_parent(config):
    parent=Path(config['parent_run'])
    require(digest(parent/'checkpoint.json')==config['parent_checkpoint_sha256'],'Sealed parent checkpoint changed')
    require(digest(parent/'status.json')==config['parent_status_sha256'],'Sealed parent terminal status changed')
    state=json.loads((parent/'checkpoint.json').read_bytes());status=json.loads((parent/'status.json').read_bytes())
    require(status['status']=='stopped' and status['error'] is None,'Parent is not stopped cleanly')
    require(state['completed_bound'] is None and state['next_patch']==config['initial_patch'],
            'Continuation must start at exact selected parent cursor')
    require((state['journal_sha256'],state['journal_offset'])==
            (config['parent_journal_sha256'],config['parent_journal_offset']) and
            (parent/'coverage.jsonl').stat().st_size==state['journal_offset'],
            'Parent committed prefix identity/length changed')
    audit_path=Path(config['parent_audit_file'])
    require(digest(audit_path)==config['parent_audit_sha256'],'Sealed parent audit changed')
    audit=json.loads(audit_path.read_bytes())
    require(audit['status']=='passed' and audit['final_checkpoint'] is True and
            audit['captured_checkpoint_sha256']==config['parent_checkpoint_sha256'] and
            audit['committed_chain_sha256']==config['parent_journal_sha256'] and
            audit['committed_raw_sha256']==config['parent_journal_raw_sha256'] and
            audit['committed_bytes']==config['parent_journal_offset'] and
            audit['selected_interval'][1]==config['initial_patch'],'Final parent audit mismatch')
    validate_archive(config)
    return state

def validate_ledger(config):
    import ada_export_store
    coverage_path=Path(config['coverage_file'])
    require(digest(coverage_path)==config['coverage_sha256'],'Frozen coverage link changed')
    coverage=json.loads(coverage_path.read_bytes())
    require(coverage['status']=='verified_receipts' and coverage['final_checkpoint'] is True and
            coverage['next_patch']==config['initial_patch'] and
            coverage['parent_checkpoint_sha256']==config['parent_checkpoint_sha256'] and
            coverage['parent_journal_sha256']==config['parent_journal_sha256'],'Coverage link mismatch')
    store=ada_export_store.Store(config['ledger_root']);until=time.monotonic()+2
    require(store.device==config['ledger_device'],'Coordinator filesystem identity changed')
    while True:
        try:claim=store.claim(config['ledger_job']);break
        except ada_export_store.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.02)
    require(claim['sha256']==config['ledger_claim_sha256'],'Coordinator claim changed')
    if config.get('TEST_ONLY') is True:
        require((claim['first'],claim['last'],claim['identity'])==
                (config['initial_patch'],config['range_end'],config['manifest_sha256']),
                'Isolated validation claim mismatch')
    else:
        path=Path(config['origin_claim_file'])
        require(digest(path)==config['origin_claim_file_sha256'],'Original reservation proof changed')
        original=json.loads(path.read_bytes())
        require(claim==original and claim['identity']==config['reservation_manifest_sha256'] and
                claim['first']==config['reservation_initial_patch'] and
                claim['first']<=config['initial_patch']<config['range_end']==claim['last'],
                'Original reservation inheritance mismatch')
    import bulk_data_store
    require(bulk_data_store.verify_share(config['replica_output'])==config['data_device'],
            'Bulk-data filesystem identity changed')
    require(Path(config['output']).parent.stat().st_dev==config['local_data_device'],'Local journal filesystem identity changed')
    return store,claim

def load_config(path):
    config=json.loads(Path(path).read_bytes());base=json.loads((ROOT/'base-config.json').read_bytes())
    require(os.uname().nodename.split('.')[0]=='ada','Wrong actual host')
    if config.get('TEST_ONLY') is True:
        allowed={'TEST_ONLY','run_id','output','replica_output','ledger_root','ledger_job','ledger_device',
                 'ledger_claim_sha256','range_end','gmp_audit_period','test_chunk_limit',
                 'stop_epoch','stop_local','service_name','deadline_service_name'}
        require(all(config.get(k)==v for k,v in base.items() if k not in allowed),
                'Validation changed frozen geometry/resource/parent settings')
        require(Path(config['ledger_root']).is_relative_to(TEST_LEDGER),'Test ledger escaped isolated namespace')
        expected=LOCAL/'TEST_ONLY_group4_20261109'/config['run_id']/'run'
        replica_expected=BULK/'TEST_ONLY_group4_20261109'/config['run_id']/'run'
        require(config['initial_patch']<config['range_end']<=base['range_end'],'Invalid test interval')
    else:
        require(config==base,'Production configuration differs from sealed base')
        require(Path(config['ledger_root'])==SHARED,'Wrong production coordinator')
        expected=LOCAL/config['ledger_job']/config['run_id']/'run'
        replica_expected=BULK/'runs'/config['ledger_job']/config['run_id']/'run'
        require(config.get('test_chunk_limit') is None,'Production test limit is forbidden')
    require(Path(config['output']).resolve()==expected.resolve(),'Output escaped reserved local directory')
    require(Path(config['replica_output']).resolve()==replica_expected.resolve(),'Replica escaped reserved bulk directory')
    require(config['dispatch_chunksize']==4 and config['ready_queue_limit']==3 and config['journal_buffer_records']==8 and config['journal_buffer_bytes']==8*1024**2 and config['journal_buffer_max_age_seconds']==.25,'Buffered runtime policy changed')
    require(config['group_limit']==4 and config['replica_interval_seconds']==60 and
            config['maximum_replica_lag_seconds']==300,'Invalid grouping or replication policy')
    import subprocess
    filesystem=subprocess.run(['findmnt','-n','-o','FSTYPE','-T',str(Path(config['output']).parent)],capture_output=True,text=True,check=True,timeout=5).stdout.strip()
    require(filesystem in ('ext4','xfs','btrfs','zfs'),'Journal is not on an admitted local filesystem')
    require(config['backend']=='gpu' and config['workers']==16 and
            config['physical_cpus']==list(range(16)),'Validated CPU/GPU allocation changed')
    require((config['shell_lo'],config['shell_hi'],config['width'],config['bits'],config['cap'],config['chunk_patches'])==
            (100000000001,200000000000,8,222,42,256) and config['geometry_policy']=='adaptive',
            'Validated arithmetic/geometry policy changed')
    require(0<config['prep_load_ceiling']<=17 and config['prep_load_ceiling']<config['running_load_limit']<=20,
            'CPU budget changed')
    require(0<config['journal_limit_bytes']<=128*1024**3 and config['minimum_free_disk_bytes']>=8*1024**3,
            'Bulk journal/storage budget invalid')
    require(time.time()<config['stop_epoch']<=base['stop_epoch'] and
            abs(datetime.fromisoformat(config['stop_local']).timestamp()-config['stop_epoch'])<.001,
            'Frozen per-run absolute deadline exceeded/expired')
    require(config['automatic_resume'] is False and 1<=config['gmp_audit_period']<=128,
            'Automatic resume/audit policy changed')
    require(config.get('test_chunk_limit') is None or 1<=config['test_chunk_limit']<=32,
            'Invalid finite validation limit')
    verify_sources(config);validate_parent(config);validate_ledger(config)
    return config

def remaining(config,event,output,cap=30):
    if event.is_set() or (Path(output)/'STOP').exists():raise RequestedStop('Stop requested')
    left=config['stop_epoch']-time.time()-8
    if left<=0:raise RequestedStop('Absolute deadline reached; final cleanup')
    return min(cap,left)

def check_storage(config,output):
    if shutil.disk_usage(output).free<config['minimum_free_disk_bytes']:
        raise RequestedStop('Bulk storage reserve reached')
    path=Path(output)/'coverage.jsonl'
    if path.exists() and path.stat().st_size>=config['journal_limit_bytes']:
        raise RequestedStop('Bulk journal byte budget reached')
