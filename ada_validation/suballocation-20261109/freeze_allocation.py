"""Freeze a disjoint child ledger from the exact sealed Ada cursor."""
from datetime import datetime,timezone
import hashlib,json,os,shutil,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
OLD=Path('/home/pnord/ada-overnight-20261109/worker')
CHILD=Path('/mnt/nfs_share/fifth42-shared-20261107/suballocations/ada-boole-20261109-r1')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,row):
    p=Path(p);t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(row,indent=2)+'\n');os.replace(t,p)
def main():
    import sys
    sys.path.insert(0,str(W));import ada_export_store
    old=json.loads((OLD/'config.json').read_bytes());seal=json.loads((ROOT/'sealed-parent.json').read_bytes())
    assert seal['status']=='verified' and seal['final_cursor']<7000000000
    parent=Path(seal['replica']);cp=json.loads((parent/'checkpoint.json').read_bytes())
    assert cp==seal['checkpoint'] and sha(parent/'checkpoint.json')==json.loads((ROOT/'final-parent-audit.json').read_bytes())['captured_checkpoint_sha256']
    source=ada_export_store.Store(old['ledger_root']);origin=source.claim(old['ledger_job'])
    assert origin['sha256']==old['ledger_claim_sha256']
    store=ada_export_store.Store(CHILD)
    grant=dict(schema='fifth42-parent-suballocation-v1',TEST_ONLY=False,parent_ledger=old['ledger_root'],parent_job=old['ledger_job'],parent_claim_sha256=origin['sha256'],parent_first=origin['first'],parent_last=origin['last'],child_ledger=str(CHILD),assignments=dict(ada=[cp['next_patch'],7000000000],boole=[7000000000,origin['last']]),stop_epoch=1794351600,retained_manifest_sha256=sha(W/'release-manifest.json'),coordinator_source_sha256=sha(ROOT/'parent_coordinator.py'),coverage_claimed=False,verified_old_final_checkpoint_sha256=sha(parent/'checkpoint.json'),verified_old_final_audit_sha256=sha(ROOT/'final-parent-audit.json'),created_utc=datetime.now(timezone.utc).isoformat(),boole_native_gpu_sha256='690581e2d68d89d5d02fea261fae3a2552f679b73d5ddcc97d17d4965b65680b',boole_native_gmp_sha256='8d514a59a5488de9a16a2f7ab0ecd351fdc13816298ddb777a18d9aa94158eb6')
    assert not (CHILD/'GRANT.json').exists();write(CHILD/'GRANT.json',grant);gsha=sha(CHILD/'GRANT.json')
    a=store.reserve('ada-suballocated-20261109',cp['next_patch'],7000000000,gsha,dict(allocation_kind='retained_parent_subset',grant_sha256=gsha,coverage_claimed=False))
    for claim in [a]:(CHILD/'jobs'/claim['job']/'journal.jsonl').touch(mode=0o600)
    allocations=[]
    for i,first in enumerate(range(7000000000,origin['last'],64000000)):
        last=min(first+64000000,origin['last']);job=f'boole-delegated-20261109-{i:02d}'
        c=store.reserve(job,first,last,gsha,dict(allocation_kind='new_uncomputed_parent_subclaim',role='boole',grant_sha256=gsha,coverage_claimed=False))
        (CHILD/'jobs'/job/'journal.jsonl').touch(mode=0o600)
        allocations.append(dict(job=job,first=first,last=last,identity=c['identity'],claim_sha256=c['sha256']))
    write(CHILD/'BOOLE_ALLOCATIONS.json',dict(status='reserved_not_coverage',grant_sha256=gsha,allocations=allocations,stop_epoch=1794351600,host_validation_required=True))
    write(CHILD/'PARENT_CLAIM.json',origin);shutil.copy2(W/'suballocation_guard.py',CHILD/'suballocation_guard.py');shutil.copy2(ROOT/'parent_coordinator.py',CHILD/'parent_coordinator.py')
    receipt=parent/'ARCHIVE_RECEIPT.json'
    value=dict(status='verified',raw_sha256=seal['raw_sha256'],committed_bytes=cp['journal_offset'],captured_checkpoint_sha256=sha(parent/'checkpoint.json'),source=seal['local'],archive=str(parent),captured_status_sha256=sha(parent/'status.json'),method='Complete rolling receipt/GMP audit plus final full local and bulk raw SHA256 equality',audit_sha256=sha(ROOT/'final-parent-audit.json'))
    if receipt.exists():assert json.loads(receipt.read_bytes())==value
    else:write(receipt,value)
    for p in [W/'parent-audit.json',ROOT/'parent-audit.json']:shutil.copy2(ROOT/'final-parent-audit.json',p)
    write(W/'child-claim.json',a)
    coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=cp['next_patch'],parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_raw_sha256=seal['raw_sha256'],selected_interval=[old['initial_patch'],cp['next_patch']],cumulative_selected_patches=seal['cumulative_selected_patches'],full_bound_claim=False)
    write(W/'final-coverage.json',coverage)
    cfg=dict(old,run_id='ada-suballocation-20261109',parent_run=str(parent),parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_status_file=str(parent/'status.json'),parent_status_sha256=sha(parent/'status.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_offset=cp['journal_offset'],parent_journal_raw_sha256=seal['raw_sha256'],parent_journal_identity=seal['replica_journal_identity'],parent_selected_patches=seal['cumulative_selected_patches'],initial_patch=cp['next_patch'],range_end=7000000000,parent_audit_file=str(W/'parent-audit.json'),parent_audit_sha256=sha(W/'parent-audit.json'),parent_archive_receipt=str(receipt),parent_archive_receipt_sha256=sha(receipt),coverage_file=str(W/'final-coverage.json'),coverage_sha256=sha(W/'final-coverage.json'),manifest=str(W/'release-manifest.json'),manifest_sha256=sha(W/'release-manifest.json'),origin_claim_file=str(W/'child-claim.json'),origin_claim_file_sha256=sha(W/'child-claim.json'),ledger_root=str(CHILD),ledger_job=a['job'],ledger_device=store.device,ledger_claim_sha256=a['sha256'],reservation_manifest_sha256=gsha,reservation_initial_patch=a['first'],allocation_role='ada',suballocation_grant_file=str(CHILD/'GRANT.json'),suballocation_grant_sha256=gsha,handoff_parent_config_file=str(OLD/'config.json'),handoff_parent_config_sha256=sha(OLD/'config.json'),output='/home/pnord/fifth42-local-runs/ada-suballocated-20261109/ada-suballocation-20261109/run',replica_output='/mnt/localstorage/pnord/fifth42-storage/runs/ada-suballocated-20261109/ada-suballocation-20261109/run',service_name='ada-suballocation-20261109.service',deadline_service_name='ada-suballocation-20261109-deadline.service',previous_attempt=old['output'],journal_limit_bytes=116*1024**3,authorization='User relayed Boole request for additional coordinated nonoverlapping work through Nov 10 at 5 p.m. Central. Ada retains an explicit hard-capped child range; Boole receives protected child claims only after the original parent lease is exclusively held by the coordinator and the bounded successor is verified.')
    for key in ['output','replica_output']:
        p=Path(cfg[key]);p.parent.mkdir(mode=0o700,parents=True,exist_ok=True);assert not p.exists()
    cfg['local_data_device']=Path(cfg['output']).parent.stat().st_dev
    for p in [W/'config.json',W/'base-config.json',ROOT/'validation-template.json']:write(p,cfg)
    write(CHILD/'retained-configuration.json',cfg);shutil.copy2(W/'release-manifest.json',CHILD/'retained-source-manifest.json')
    write(ROOT/'configuration-state.json',dict(status='production_configured',manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(W/'config.json'),initial_patch=cfg['initial_patch'],deadline=cfg['stop_local'],production_started=False))
    write(ROOT/'allocation-state.json',dict(status='prepared',grant_sha256=gsha,ada=[cfg['initial_patch'],7000000000],boole=[7000000000,origin['last']],boole_claims=len(allocations),config_sha256=sha(W/'config.json'),manifest_sha256=cfg['manifest_sha256']))
    print(json.dumps(json.loads((ROOT/'allocation-state.json').read_bytes()),indent=2))
if __name__=='__main__':main()
