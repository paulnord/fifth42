"""Frozen weekend allocation, storage budget, parent identity and deadline."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import time

ROOT=Path(__file__).resolve().parent


class RequestedStop(Exception):
    pass


def require(condition,message):
    if not condition:raise RuntimeError(message)


def digest(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):result.update(block)
    return result.hexdigest()


def stable(value):return json.dumps(value,sort_keys=True,separators=(',',':'))


def verify_sources(config):
    path=Path(config['manifest'])
    require(digest(path)==config['manifest_sha256'],'Release manifest changed')
    manifest=json.loads(path.read_text())
    for name,expected in manifest['files'].items():
        require(digest(ROOT/name)==expected,'Frozen executable/source changed: '+name)
    for name,expected in manifest.get('external_files',{}).items():
        require(digest(name)==expected,'Existing resource helper changed: '+name)
    return manifest


def validate_parent(config):
    parent=Path(config['parent_run'])
    require(digest(parent/'checkpoint.json')==config['parent_checkpoint_sha256'],'Parent checkpoint changed')
    state=json.loads((parent/'checkpoint.json').read_text())
    if config.get('parent_layout')=='continuation':
        status_path=Path(config['parent_status_file'])
        require(digest(status_path)==config['parent_status_sha256'],'Parent terminal status changed')
        status=json.loads(status_path.read_text())
        require(status['status']=='stopped' and status['error'] is None,'Previous continuation is not stopped cleanly')
    else:
        require(state['status']=='stopped','Parent is not stopped')
    require(state['completed_bound'] is None,'Parent is not a selected-only checkpoint')
    require(state['next_patch']==config['initial_patch'],'Continuation does not start at parent cursor')
    require(state['journal_sha256']==config['parent_journal_sha256'] and
            state['journal_offset']==config['parent_journal_offset'],'Parent journal identity changed')
    require((parent/'coverage.jsonl').stat().st_size==state['journal_offset'],'Parent has an uncommitted suffix')
    return state


def validate_ledger(config):
    import ada_export_store
    coverage_path=Path(config['coverage_file'])
    require(digest(coverage_path)==config['coverage_sha256'],'Verified handoff metadata changed')
    coverage=json.loads(coverage_path.read_bytes())
    require(coverage['status']=='verified_receipts' and coverage['final_checkpoint'] is True and
            coverage['next_patch']==config['initial_patch'] and
            coverage['parent_checkpoint_sha256']==config['parent_checkpoint_sha256'] and
            coverage['parent_journal_sha256']==config['parent_journal_sha256'],
            'Handoff metadata does not identify the verified final parent')
    store=ada_export_store.Store(config['ledger_root'])
    require(store.device==config['ledger_device'],'Shared ledger filesystem identity changed')
    until=time.monotonic()+1
    while True:
        try:
            claim=store.claim(config['ledger_job'])
            break
        except ada_export_store.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.02)
    require(claim['sha256']==config['ledger_claim_sha256'] and
            (claim['first'],claim['last'],claim['identity'])==
            (config['initial_patch'],config['range_end'],config['manifest_sha256']) and
            claim['coverage']==dict(sha256=config['coverage_sha256'],manifest=coverage),
            'Shared reservation or runtime/coverage identity changed')
    return store,claim


def load_config(path):
    config=json.loads(Path(path).read_text())
    base=json.loads((ROOT/'base-config.json').read_text())
    for name in ('parent_run','parent_checkpoint_sha256','parent_journal_sha256','parent_journal_offset',
                 'initial_patch','shell_lo','shell_hi','width','bits','cap','workers','physical_cpus','chunk_patches',
                 'parent_layout','parent_status_file','parent_status_sha256','prep_load_ceiling',
                 'running_load_limit','journal_limit_bytes','minimum_free_disk_bytes',
                 'geometry_policy','ledger_root','ledger_job','ledger_device','ledger_claim_sha256',
                 'coverage_file','coverage_sha256','output','range_end'):
        require(config[name]==base[name],'Validated run setting changed: '+name)
    require(config['backend']=='gpu' and config['workers']==16,'Unsupported engine/allocation')
    require(config['geometry_policy']=='adaptive','Production requires the validated adaptive precision policy')
    require(config['ledger_runtime_identity']==config['manifest_sha256'],'Ledger runtime identity changed')
    require(config['physical_cpus']==list(range(16)),'Unsupported physical CPU allocation')
    require(0<config['prep_load_ceiling']<=17,'Preparation pacing exceeds the resource budget')
    require(config['prep_load_ceiling']<config['running_load_limit']<=20,'Invalid running CPU budget')
    require(0<config['journal_limit_bytes']<=128*1024**3,'Invalid weekend journal budget')
    require(config['minimum_free_disk_bytes']>=4*1024**3,'Insufficient free disk reserve')
    require(time.time()<config['stop_epoch']<=base['stop_epoch'],'Invalid or expired absolute deadline')
    require(abs(datetime.fromisoformat(config['stop_local']).timestamp()-config['stop_epoch'])<.001,
            'Local and absolute stop times disagree')
    expected_output=Path(config['ledger_root'])/'jobs'/config['ledger_job']/'run'
    require(Path(config['output']).resolve()==expected_output.resolve(),'Output must match the shared reserved job')
    require(config['range_end']==11250000001,'Selected shell endpoint changed')
    require(config.get('test_chunk_limit') is None or 1<=config['test_chunk_limit']<=32,'Invalid bounded validation limit')
    require(1<=config['gmp_audit_period']<=128,'Independent audit interval enlarged')
    require(3*config['shell_hi']**5<2**191,'Exact I192 range proof failed')
    verify_sources(config);validate_parent(config);validate_ledger(config)
    return config


def remaining(config,stop_event,output,cap=30):
    if stop_event.is_set() or (Path(output)/'STOP').exists():raise RequestedStop('Stop requested')
    left=config['stop_epoch']-time.time()-8
    if left<=0:raise RequestedStop('Absolute deadline reached; final checkpoint cleanup')
    return min(cap,left)


def check_storage(config,output):
    output=Path(output)
    if shutil.disk_usage(output).free<config['minimum_free_disk_bytes']:
        raise RequestedStop('Free space below weekend disk reserve')
    journal=output/'coverage.jsonl'
    if journal.exists() and journal.stat().st_size>=config['journal_limit_bytes']:
        raise RequestedStop('Coverage journal reached weekend byte budget')


def utc():return datetime.now(timezone.utc).isoformat()
