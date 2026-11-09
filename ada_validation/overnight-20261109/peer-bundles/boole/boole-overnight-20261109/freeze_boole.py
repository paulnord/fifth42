"""Freeze Boole's own combined runtime after parent and grouping verification."""
import hashlib,json,os,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import policy,ada_export_store,bulk_data_store
from durable_mirror import atomic

def main():
 parent=json.loads((ROOT/'sealed-parent.json').read_bytes())
 grouping=json.loads((ROOT/'evidence/boole-validation/buffered-compute.json').read_bytes())
 assert parent['status']=='verified' and grouping['status']=='passed' and grouping['selected_group_limit']==4
 archive=Path(parent['archive']);job='boole-precision-20261107T222232Z';name='boole-overnight-20261109'
 for path in (archive/'independent-audits',archive,archive.parent):
  fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
  try:os.fsync(fd)
  finally:os.close(fd)
 local=policy.LOCAL/job/name;local.mkdir(mode=0o700,parents=True,exist_ok=True)
 assert not (local/'run').exists()
 replica=policy.BULK/'runs'/job/name/'run';assert not replica.exists()
 shutil.copy2('/home/pnord/boole-bulk-20261108/original-claim.json',W/'origin-claim.json')
 shutil.copy2(ROOT/'parent-audit.json',W/'parent-audit.json')
 shutil.copy2(ROOT/'parent-lineage.json',W/'parent-lineage.json')
 store=ada_export_store.Store('/mnt/nfs_share/fifth42-shared-20261107');claim=store.claim(job)
 assert json.loads((W/'origin-claim.json').read_bytes())==claim
 cp=json.loads((archive/'checkpoint.json').read_bytes())
 coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=cp['next_patch'],
  covered_intervals=[[3000000000,cp['next_patch']]],parent_checkpoint_sha256=policy.digest(archive/'checkpoint.json'),
  parent_journal_sha256=cp['journal_sha256'],parent_archive=str(archive),completed_bound=None,
  earlier_separate_coverage=json.loads(Path('/home/pnord/boole-bulk-20261108/worker/boole-final-coverage.json').read_bytes()))
 atomic(W/'final-coverage.json',coverage)
 existing=W/'release-manifest.json'
 if not (ROOT/'evidence/ada-reference-runtime-manifest.json').exists():shutil.copy2(existing,ROOT/'evidence/ada-reference-runtime-manifest.json')
 files={str(p.relative_to(W)):policy.digest(p) for p in sorted(W.rglob('*')) if p.is_file() and '__pycache__' not in p.parts
        and p.name not in ('release-manifest.json','production-config.json','base-config.json')}
 external={str(p):policy.digest(p) for p in sorted(ROOT.glob('*.py')) if p.is_file()}
 manifest=dict(host='boole',provenance='GitHub 0d48c556825e1e03bc109bdef7232f4555fc0d61 buffered-r1; unchanged Boole native binary/search; bounded reservation-snapshot retry; exact-parent continuation and user-authorized extended deadline.',
  source_bundle_sha256='a5149bdfdaa050c998576f8f07b22b39fb88a0b1fd3befb75fceefaffeb5b4f4',files=files,external_files=external,
  compiler='g++-13 13.4.0; CUDA 12.8.93; sm_86',python='/home/pnord/boole-results-20261107/venv312/bin/python')
 atomic(existing,manifest)
 c=dict(TEST_ONLY=False,run_id=name,parent_run=str(archive),parent_checkpoint_sha256=policy.digest(archive/'checkpoint.json'),
  parent_status_sha256=policy.digest(archive/'status.json'),parent_journal_sha256=cp['journal_sha256'],
  parent_journal_offset=cp['journal_offset'],parent_journal_raw_sha256=parent['audit']['committed_raw_sha256'],
  parent_journal_identity=parent['parent_journal_identity'],parent_selected_patches=cp['next_patch']-3000000000,
  parent_audit_file=str(W/'parent-audit.json'),parent_audit_sha256=policy.digest(W/'parent-audit.json'),
  parent_archive_receipt=str(archive/'ARCHIVE_RECEIPT.json'),parent_archive_receipt_sha256=policy.digest(archive/'ARCHIVE_RECEIPT.json'),
  parent_lineage_file=str(W/'parent-lineage.json'),parent_lineage_sha256=policy.digest(W/'parent-lineage.json'),
  initial_patch=cp['next_patch'],range_end=3750000000,shell_lo=100000000001,shell_hi=200000000000,width=8,bits=222,cap=42,
  workers=16,physical_cpus=list(range(16)),chunk_patches=256,stop_local='2026-11-10T17:00:00-06:00',stop_epoch=1794351600,
  backend='gpu',gmp_audit_period=128,automatic_resume=False,publication=False,
  manifest=str(existing),manifest_sha256=policy.digest(existing),output=str(local/'run'),replica_output=str(replica),
  service_name=name+'.service',deadline_service_name=name+'-deadline.service',test_chunk_limit=None,
  prep_load_ceiling=17.,running_load_limit=20.,journal_limit_bytes=32*1024**3,minimum_free_disk_bytes=16*1024**3,
  geometry_policy='adaptive',ledger_root=str(store.root),ledger_job=job,ledger_device=store.device,
  ledger_claim_sha256=claim['sha256'],origin_claim_file=str(W/'origin-claim.json'),origin_claim_file_sha256=policy.digest(W/'origin-claim.json'),
  coverage_file=str(W/'final-coverage.json'),coverage_sha256=policy.digest(W/'final-coverage.json'),
  reservation_manifest_sha256=claim['identity'],reservation_initial_patch=3000000000,
  data_device=bulk_data_store.verify_share(replica),local_data_device=local.stat().st_dev,
  optimization='saved-root+exact-host+low64+group4+checked-task-cache+ready-queue+durable-eight-record-buffer',
  dispatch_chunksize=4,ready_queue_limit=3,journal_buffer_records=8,journal_buffer_bytes=8388608,journal_buffer_max_age_seconds=0.25,preparation_windows=1,
  group_limit=grouping['selected_group_limit'],replica_interval_seconds=60,maximum_replica_lag_seconds=300,
  authorization='User authorized continuation until tomorrow at 5 pm; exact verified checkpoint restart; NFS ownership unchanged; continue until 2026-11-10 17:00 America/Chicago; final copy until 17:30.')
 atomic(W/'base-config.json',c);atomic(W/'production-config.json',c)
 policy.load_config(W/'production-config.json')
 atomic(ROOT/'FROZEN.json',dict(status='frozen',manifest_sha256=c['manifest_sha256'],config_sha256=policy.digest(W/'production-config.json'),
  first=c['initial_patch'],group_limit=c['group_limit'],local_output=c['output'],replica_output=c['replica_output'],stop_local=c['stop_local']))
 print(json.dumps(json.loads((ROOT/'FROZEN.json').read_bytes()),indent=2),flush=True)
if __name__=='__main__':main()
