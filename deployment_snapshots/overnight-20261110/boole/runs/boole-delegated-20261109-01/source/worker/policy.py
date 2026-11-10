"""Boole buffered continuation: original NFS owner, verified parent, local journal and verified bulk mirror."""
from datetime import datetime,timezone
import hashlib,json,os,shutil,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BULK=Path('/mnt/fifth42-storage')
SHARED=Path('/mnt/nfs_share/fifth42-shared-20261107')
TEST_LEDGER=Path('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/suballocation-tests/boole-local-delegated-20261109')
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

def verify_bulk(config):
    """Retain Boole's supervisor API while checking local and replica devices."""
    import bulk_data_store,subprocess
    output=Path(config['output'])
    require(output.parent.stat().st_dev==config['local_data_device'],'Local journal device changed')
    filesystem=subprocess.check_output(['findmnt','-n','-o','FSTYPE','-T',str(output.parent)],text=True,timeout=5).strip()
    require(filesystem in ('ext4','xfs','btrfs','zfs'),'Local journal filesystem changed')
    require(bulk_data_store.verify_share(config['replica_output'])==config['data_device'],'Bulk replica mount/device changed')
    return output

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

def validate_parent(config,full=False):
    parent=Path(config['parent_run'])
    reference_cursor=config['reference_parent_cursor']
    require(config['parent_selected_patches']==0 and config['allocation_kind']=='independent_reserved_interval','New allocation must keep earlier coverage separate')
    require(digest(parent/'checkpoint.json')==config['parent_checkpoint_sha256'],'Sealed parent checkpoint changed')
    require(digest(parent/'status.json')==config['parent_status_sha256'],'Sealed parent terminal status changed')
    state=json.loads((parent/'checkpoint.json').read_bytes());status=json.loads((parent/'status.json').read_bytes())
    require(status['status']=='stopped' and status['error'] is None,'Parent is not stopped cleanly')
    require(state['completed_bound'] is None and state['next_patch']==reference_cursor,
            'Historical reference cursor changed')
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
            audit['selected_interval'][1]==reference_cursor,'Final parent audit mismatch')
    validate_archive(config)
    lineage=Path(config['parent_lineage_file'])
    require(digest(lineage)==config['parent_lineage_sha256'],'Parent lineage proof changed')
    proof=json.loads(lineage.read_bytes());cursor=3000000000
    for segment in proof['segments']:
        require(segment['first']==cursor and segment['last']>cursor,'Parent lineage gap/overlap')
        require(digest(Path(segment['archive'])/'ARCHIVE_RECEIPT.json')==segment['receipt_sha256'],'Earlier archive receipt changed')
        require(digest(Path(segment['archive'])/'checkpoint.json')==segment['checkpoint_sha256'],'Earlier checkpoint changed')
        cursor=segment['last']
    require(cursor==reference_cursor and proof['covered_interval']==[3000000000,cursor],'Parent lineage cursor changed')
    return state

def validate_protected_grant(config):
    import ada_export_store,suballocation_guard
    grant=suballocation_guard.check(config)
    require(config['allocation_role']=='boole','Wrong allocation role')
    if config.get('TEST_ONLY') is not True:
        require(config['suballocation_grant_sha256']=='7c8422f5e9086519db3bc8ad2e8eeab8d7d1d60706f9b327766ba0a069c6a389' and
                grant['parent_claim_sha256']=='7d6b55c80d480208b324d6748fcc3660e12a0b70a7f2a21ad8c28bf0b0a16b33',
                'Wrong parent allocation generation')
        require(digest(ROOT/'bin/scaling_gpu')==grant['boole_native_gpu_sha256'] and
                digest(ROOT/'bin/gmp_reference')==grant['boole_native_gmp_sha256'],'Grant native identities differ')
    else:
        require(Path(config['suballocation_grant_file']).is_relative_to(TEST_LEDGER),'Test grant escaped isolated namespace')
    store=ada_export_store.Store(grant['parent_ledger']);until=time.monotonic()+2
    while True:
        try:claim=store.claim(grant['parent_job']);break
        except ada_export_store.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.02)
    require(claim['sha256']==grant['parent_claim_sha256'] and
            (claim['first'],claim['last'])==(grant['parent_first'],grant['parent_last']),'Legacy parent claim changed')
    return grant

def validate_ledger(config):
    validate_protected_grant(config)
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
        try:
            with store.locked(store.root/'reservations.jsonl') as fd:
                reservations=store.claims(fd)
            break
        except ada_export_store.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.02)
    found=[r for r in reservations if r['job']==config['ledger_job']]
    require(len(found)==1,'Unknown/ambiguous reserved job')
    claim=found[0]
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
    for other in reservations:
        if other['job']!=claim['job']:
            require(not(claim['first']<other['last'] and other['first']<claim['last']),'Original allocation overlaps another owner')
    import bulk_data_store
    require(bulk_data_store.verify_share(config['replica_output'])==config['data_device'],
            'Bulk-data filesystem identity changed')
    require(Path(config['output']).parent.stat().st_dev==config['local_data_device'],'Local journal filesystem identity changed')
    return store,claim

def load_config(path):
    config=json.loads(Path(path).read_bytes());base=json.loads((ROOT/'base-config.json').read_bytes())
    require(os.uname().nodename.split('.')[0]=='boole','Wrong actual host')
    if config.get('TEST_ONLY') is True:
        allowed={'TEST_ONLY','run_id','output','replica_output','ledger_root','ledger_job','ledger_device',
                 'ledger_claim_sha256','range_end','gmp_audit_period','test_chunk_limit',
                 'stop_epoch','stop_local','service_name','deadline_service_name','suballocation_grant_file','suballocation_grant_sha256'}
        require(all(config.get(k)==v for k,v in base.items() if k not in allowed),
                'Validation changed frozen geometry/resource/parent settings')
        require(Path(config['ledger_root']).is_relative_to(TEST_LEDGER),'Test ledger escaped isolated namespace')
        expected=LOCAL/'TEST_ONLY_boole_delegated_20261109'/config['run_id']/'run'
        replica_expected=BULK/'TEST_ONLY_boole_delegated_20261109'/config['run_id']/'run'
        require(config['initial_patch']<config['range_end']<=base['range_end'],'Invalid test interval')
    else:
        require(config==base,'Production configuration differs from sealed base')
        require(config['run_id'].startswith('boole-delegated-20261109-') and config['ledger_job']==config['run_id'] and config['stop_epoch']==1794351600,'Frozen new allocation identity/deadline changed')
        require(7000000000<=config['reservation_initial_patch']==config['initial_patch']<config['range_end']<=11250000001 and config['range_end']-config['initial_patch']<=64000000,'New allocation escaped tested planning interval')
        require(Path(config['ledger_root'])==SHARED/'suballocations/ada-boole-20261109-r1','Wrong protected child coordinator')
        expected=LOCAL/config['ledger_job']/config['run_id']/'run'
        replica_expected=BULK/'runs'/config['ledger_job']/config['run_id']/'run'
        require(config.get('test_chunk_limit') is None,'Production test limit is forbidden')
    require(Path(config['output']).resolve()==expected.resolve(),'Output escaped reserved local directory')
    require(Path(config['replica_output']).resolve()==replica_expected.resolve(),'Replica escaped reserved bulk directory')
    require(config['group_limit']==4 and config['dispatch_chunksize']==4 and config['ready_queue_limit']==3 and config['preparation_windows']==1,'Buffered dispatch/queue settings changed')
    require(config['journal_buffer_records']==8 and config['journal_buffer_bytes']==8388608 and config['journal_buffer_max_age_seconds']==0.25,'Durable buffer bounds changed')
    require(config['group_limit'] in (1,2,4) and config['replica_interval_seconds']==60 and
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
    require(0<config['journal_limit_bytes']<=32*1024**3 and config['minimum_free_disk_bytes']>=16*1024**3,
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
    if os.getloadavg()[0]>config['running_load_limit']:raise RequestedStop('Running CPU load budget exceeded')
    left=config['stop_epoch']-time.time()-8
    if left<=0:raise RequestedStop('Absolute deadline reached; final cleanup')
    return min(cap,left)

def check_storage(config,output):
    require(Path(output).stat().st_dev==config['local_data_device'],'Local output device changed')
    import bulk_data_store
    require(bulk_data_store.verify_share(config['replica_output'])==config['data_device'],'Bulk replica mount/device changed')
    if shutil.disk_usage(BULK).free<config['minimum_free_disk_bytes']:
        raise RequestedStop('Bulk replica storage reserve reached')
    if shutil.disk_usage(output).free<config['minimum_free_disk_bytes']:
        raise RequestedStop('Bulk storage reserve reached')
    path=Path(output)/'coverage.jsonl'
    if path.exists() and path.stat().st_size>=config['journal_limit_bytes']:
        raise RequestedStop('Bulk journal byte budget reached')
