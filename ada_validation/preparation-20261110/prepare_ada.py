"""Freeze the Ada preparation upgrade and a separate renewed parent grant."""
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import hashlib,json,shutil,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;W=R/'worker'
OLD=Path('/home/pnord/ada-suballocation-20261109/worker')
CHILD=Path('/mnt/nfs_share/fifth42-shared-20261107/suballocations/ada-boole-20261109-r1')
HANDOFF=Path('/mnt/nfs_share/fifth42-integration-20261109/combined/parent-renewal-r2-20261110')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
 sys.path.insert(0,str(W));import ada_export_store,suballocation_guard as guard
 old=json.loads((OLD/'config.json').read_bytes());seal=json.loads((R/'sealed-parent.json').read_bytes());cp=seal['checkpoint'];parent=Path(seal['replica']);claim=ada_export_store.Store(CHILD).claim(old['ledger_job'])
 assert cp['next_patch']==5887335296 and seal['status']=='verified'
 # The historical source artifacts remain unchanged; new claim/parent proofs
 # are pinned by the run configuration instead of creating a manifest cycle.
 mf=json.loads((OLD/'release-manifest.json').read_bytes())
 names=list(mf['files'])+['gpu_preparation.py','gpu_candidate/candidate_reduction.py','gpu_candidate/gpu_lll.cu']
 mf=dict(mf,release_version='ada-preparation-r1-20261110',parent_manifest_sha256=old['manifest_sha256'],preparation_bundle_commit='37286d7c7a4f88ccec76d3d1eb17b435e1e17a77',files={n:sha(W/n) for n in names})
 write(W/'release-manifest.json',mf)
 oldgrant=json.loads(Path(old['suballocation_grant_file']).read_bytes())
 grant=dict(oldgrant,assignments=dict(ada=[cp['next_patch'],7000000000],boole=[7000000000,11250000001]),stop_epoch=1794438000,retained_manifest_sha256=sha(W/'release-manifest.json'),coordinator_source_sha256=sha(R/'parent_coordinator.py'),coordinator_state_file='coordinator-state-r2.json',ready_file='READY-r2.json',generation='renewal-r2-20261110',predecessor_grant_sha256=old['suballocation_grant_sha256'],predecessor_grant_file=old['suballocation_grant_file'],original_claim_identity=claim['identity'],verified_old_final_checkpoint_sha256=sha(parent/'checkpoint.json'),verified_old_final_audit_sha256=sha(R/'parent-audit.json'),created_utc=datetime.now(timezone.utc).isoformat(),ada_native_gpu_sha256=mf['files']['bin/scaling_gpu'])
 gp=CHILD/'GRANT-r2.json';assert not gp.exists();write(gp,grant);gsha=sha(gp)
 shutil.copy2(W/'child-claim.json',HANDOFF/'ADA_CHILD_CLAIM.json')
 coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=cp['next_patch'],parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_raw_sha256=seal['raw_sha256'],selected_interval=[old['initial_patch'],cp['next_patch']],cumulative_selected_patches=seal['cumulative_selected_patches'],full_bound_claim=False)
 write(W/'final-coverage.json',coverage)
 cfg=dict(old,run_id='ada-preparation-20261110',parent_run=str(parent),parent_checkpoint_sha256=sha(parent/'checkpoint.json'),parent_status_file=str(parent/'status.json'),parent_status_sha256=sha(parent/'status.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_offset=cp['journal_offset'],parent_journal_raw_sha256=seal['raw_sha256'],parent_journal_identity=seal['replica_journal_identity'],parent_selected_patches=seal['cumulative_selected_patches'],initial_patch=cp['next_patch'],parent_audit_file=str(W/'parent-audit.json'),parent_audit_sha256=sha(W/'parent-audit.json'),parent_archive_receipt=str(parent/'ARCHIVE_RECEIPT.json'),parent_archive_receipt_sha256=sha(parent/'ARCHIVE_RECEIPT.json'),coverage_file=str(W/'final-coverage.json'),coverage_sha256=sha(W/'final-coverage.json'),manifest=str(W/'release-manifest.json'),manifest_sha256=sha(W/'release-manifest.json'),origin_claim_file=str(W/'child-claim.json'),origin_claim_file_sha256=sha(W/'child-claim.json'),suballocation_grant_file=str(gp),suballocation_grant_sha256=gsha,handoff_parent_config_file=str(OLD/'config.json'),handoff_parent_config_sha256=sha(OLD/'config.json'),output='/home/pnord/fifth42-local-runs/'+old['ledger_job']+'/ada-preparation-20261110/run',replica_output='/mnt/localstorage/pnord/fifth42-storage/runs/'+old['ledger_job']+'/ada-preparation-20261110/run',service_name='ada-preparation-20261110.service',deadline_service_name='ada-preparation-20261110-deadline.service',stop_epoch=1794438000,stop_local='2026-11-11T17:00:00-06:00',journal_limit_bytes=64*1024**3,preparation_backend='cpu',preparation_windows=16,gpu_request_windows=1,ready_queue_limit=1,previous_attempt=old['output'])
 for key in ('output','replica_output'):Path(cfg[key]).parent.mkdir(mode=0o700,parents=True,exist_ok=True);assert not Path(cfg[key]).exists()
 for p in (W/'config.json',W/'base-config.json',R/'validation-template.json',CHILD/'retained-configuration-r2.json'):write(p,cfg)
 write(R/'configuration-state.json',dict(status='production_configured',manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(W/'config.json'),initial_patch=cfg['initial_patch'],deadline=cfg['stop_local'],production_started=False))
 for case in ('finite','signal','deadline'):
  folder=R/'runtime'/case;folder.mkdir(mode=0o700,parents=True,exist_ok=True)
  pr=guard.TEST/('preparation-'+case+'-'+str(time.time_ns()));ps=ada_export_store.Store(pr);pc=ps.reserve('test-parent',3917103232,11250000001,'a'*64,dict(TEST_ONLY=True));(pr/'jobs/test-parent/journal.jsonl').touch(mode=0o600)
  cr=pr/'suballocations/retained';store=ada_export_store.Store(cr);end=time.time()+(90 if case=='deadline' else 300);last=cfg['initial_patch']+17*256 if case=='finite' else 7000000000
  tg=dict(schema='fifth42-parent-suballocation-v1',TEST_ONLY=True,parent_ledger=str(pr),parent_job='test-parent',parent_claim_sha256=pc['sha256'],parent_first=pc['first'],parent_last=pc['last'],child_ledger=str(cr),assignments=dict(ada=[cfg['initial_patch'],last],boole=[last,11250000001]),stop_epoch=end,retained_manifest_sha256=cfg['manifest_sha256'],coverage_claimed=False)
  tgp=cr/'GRANT.json';write(tgp,tg);job='ada-preparation-test-'+case;tc=store.reserve(job,cfg['initial_patch'],last,cfg['manifest_sha256'],dict(TEST_ONLY=True));own=folder/'origin-claim.json';write(own,tc)
  output=Path('/home/pnord/fifth42-local-runs/TEST_ONLY_suballocation_20261109')/job/'run';replica=Path('/mnt/localstorage/pnord/fifth42-storage/TEST_ONLY_suballocation_20261109')/job/'run'
  for p in (output,replica):p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
  t=dict(cfg,TEST_ONLY=True,run_id=job,ledger_root=str(cr),ledger_job=job,ledger_device=store.device,ledger_claim_sha256=tc['sha256'],range_end=last,gmp_audit_period=128,test_chunk_limit=17 if case=='finite' else None,stop_epoch=end,stop_local=datetime.fromtimestamp(end,ZoneInfo('America/Chicago')).isoformat(),service_name=job+'.service',deadline_service_name=job+'-deadline.service',output=str(output),replica_output=str(replica),suballocation_grant_file=str(tgp),suballocation_grant_sha256=sha(tgp),origin_claim_file=str(own),origin_claim_file_sha256=sha(own),reservation_manifest_sha256=tc['identity'],reservation_initial_patch=tc['first'])
  write(folder/'configuration.json',t)
 for n in ('suballocation_guard.py',):shutil.copy2(W/n,HANDOFF/n)
 for n in ('parent_coordinator.py',):shutil.copy2(R/n,HANDOFF/n)
 shutil.copy2(gp,HANDOFF/'GRANT-r2.json');shutil.copy2(W/'config.json',HANDOFF/'ADA_CONFIGURATION.json');shutil.copy2(W/'release-manifest.json',HANDOFF/'ADA_SOURCE_MANIFEST.json')
 write(HANDOFF/'GRANT_PREPARED.json',dict(status='prepared_not_active',grant_file=str(gp),grant_sha256=gsha,coordinator_state_file=str(CHILD/'coordinator-state-r2.json'),ready_file=str(CHILD/'READY-r2.json'),guard_sha256=sha(W/'suballocation_guard.py'),ada_manifest_sha256=cfg['manifest_sha256'],ada_config_sha256=sha(W/'config.json'),original_child_claims_retained=True,stop_epoch=1794438000))
 print(json.dumps(dict(status='frozen',manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(W/'config.json'),grant_sha256=gsha),indent=2))
if __name__=='__main__':main()
