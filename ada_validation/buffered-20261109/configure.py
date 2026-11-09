"""Seal a fresh buffered continuation of the stopped and fully audited run."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import shutil,time
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
OLD=Path('/home/pnord/ada-full-integration-20261109/worker')
TESTS=Path('/home/pnord/ada-buffering-tests-20261109')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,row):path.write_text(json.dumps(row,indent=2)+'\n')
def main():
    old=json.loads((OLD/'config.json').read_bytes());seal=json.loads((TESTS/'sealed-parent.json').read_bytes())
    assert seal['status']=='verified' and seal['final_cursor']==4398843264
    parent=Path(seal['replica']);cp=json.loads((parent/'checkpoint.json').read_bytes());audit=json.loads((TESTS/'final-parent-audit.json').read_bytes())
    assert audit['status']=='passed' and audit['final_checkpoint'] and cp['next_patch']==audit['selected_interval'][1]
    receipt=parent/'ARCHIVE_RECEIPT.json'
    row=dict(status='verified',raw_sha256=seal['raw_sha256'],committed_bytes=cp['journal_offset'],captured_checkpoint_sha256=sha(parent/'checkpoint.json'),
             source=str(seal['local']),archive=str(parent),captured_status_sha256=sha(parent/'status.json'),
             method='Sealed stopped replica; full independent hash-chain/native-count/GMP audit and full SHA256 equality with the local journal.',audit_sha256=sha(TESTS/'final-parent-audit.json'))
    if receipt.exists():assert json.loads(receipt.read_bytes())==row
    else:write(receipt,row)
    shutil.copy2(TESTS/'final-parent-audit.json',W/'parent-audit.json');shutil.copy2(TESTS/'final-parent-audit.json',ROOT/'parent-audit.json')
    coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=cp['next_patch'],parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_raw_sha256=seal['raw_sha256'],selected_interval=[old['initial_patch'],cp['next_patch']],cumulative_selected_patches=seal['cumulative_selected_patches'],older_parent_archive=old['parent_run'],full_bound_claim=False)
    write(W/'final-coverage.json',coverage)
    original=json.loads((OLD/'release-manifest.json').read_bytes());names=list(original['files'])+['buffered_pipeline.py','scheduling.py']
    mf=dict(original,files={name:sha(W/name) for name in names},created_utc=datetime.now(timezone.utc).isoformat(),parent_manifest_sha256=old['manifest_sha256'],
            release_version='ada-buffered-r1-20261109',continuation='Fresh sealed-parent continuation with immutable canonical task cache, bounded ready queue, explicit dispatch and durable grouped journal commits.')
    mf['selected_components']=original['selected_components']+['Checked immutable canonical task data retained across preparation and consumption','Eight-record durable journal buffer; checkpoint advances only after fsync','Actual ready queue depth and empty/full wait telemetry']
    write(W/'release-manifest.json',mf)
    cfg=dict(old,run_id='ada-buffered-20261109',parent_run=str(parent),parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_status_file=str(parent/'status.json'),parent_status_sha256=sha(parent/'status.json'),
             parent_journal_sha256=cp['journal_sha256'],parent_journal_offset=cp['journal_offset'],parent_journal_raw_sha256=seal['raw_sha256'],parent_journal_identity=seal['replica_journal_identity'],
             parent_selected_patches=seal['cumulative_selected_patches'],initial_patch=cp['next_patch'],parent_audit_file=str(W/'parent-audit.json'),parent_audit_sha256=sha(W/'parent-audit.json'),
             parent_archive_receipt=str(receipt),parent_archive_receipt_sha256=sha(receipt),coverage_file=str(W/'final-coverage.json'),coverage_sha256=sha(W/'final-coverage.json'),
             manifest=str(W/'release-manifest.json'),manifest_sha256=sha(W/'release-manifest.json'),origin_claim_file=str(W/'origin-claim.json'),
             output='/home/pnord/fifth42-local-runs/20261107T213849Z-precision/ada-buffered-20261109/run',
             replica_output='/mnt/localstorage/pnord/fifth42-storage/runs/20261107T213849Z-precision/ada-buffered-20261109/run',
             service_name='ada-buffered-20261109.service',deadline_service_name='ada-buffered-20261109-deadline.service',previous_attempt=old['output'],
             optimization=old['optimization']+'+immutable-canonical-cache+buffered-durable-journal',dispatch_chunksize=8,ready_queue_limit=3,journal_buffer_records=8,journal_buffer_bytes=8*1024**2,journal_buffer_max_age_seconds=.25,
             authorization='User requested stopping today\'s run, testing memory/buffering strategies, deploying the strongest validated strategy and restarting production, then clean handoffs and GitHub publication.')
    assert cfg['stop_epoch']==1794265200 and time.time()<cfg['stop_epoch']-120
    for key in ('output','replica_output'):Path(cfg[key]).parent.mkdir(mode=0o700,parents=True,exist_ok=True);assert not Path(cfg[key]).exists()
    cfg['local_data_device']=Path(cfg['output']).parent.stat().st_dev
    for path in (W/'config.json',W/'base-config.json',ROOT/'validation-template.json'):
        assert not path.exists();write(path,cfg)
    write(ROOT/'configuration-state.json',dict(status='production_configured',deadline=cfg['stop_local'],initial_patch=cfg['initial_patch'],manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(W/'config.json'),production_started=False))
    print(json.dumps(dict(status='configured_not_started',manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(W/'config.json'),initial_patch=cfg['initial_patch'],stop_local=cfg['stop_local']),indent=2))
if __name__=='__main__':main()
