"""Freeze disjoint, uncomputed follow-on allocations with explicit independent coverage."""
import hashlib,json,os,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TEMPLATE=Path('/home/pnord/boole-extra-20261109')
sys.path[:0]=[str(TEMPLATE/'worker'),str(TEMPLATE/'worker/source/lattice_gpu')]
import ada_export_store,bulk_data_store
from durable_mirror import atomic

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 os.umask(0o077)
 request=dict(host='boole',authorization='User: continue production until tomorrow at 5 pm',stop_epoch=1794351600,
  allocation_kind='new_uncomputed_reservations',coverage_claimed=False,
  baseline_manifest_sha256='f847feb6cd3eb0e4aeba49b950d4af1010104edcfc18525eceed38e2fb5b74ce',
  compute_files_sha256={n:sha(TEMPLATE/'worker'/n) for n in ['buffered_pipeline.py','scheduling.py','packed_worker.py','bin/scaling_gpu','bin/gmp_reference','native-baseline/src/kernel.hpp']},
  ranges=[dict(label='a',job='boole-extended-20261109-a',first=100000000,last=300000000),dict(label='b',job='boole-extended-20261109-b',first=300000000,last=500000000)],
  controls='/home/pnord/boole-overnight-20261109/evidence/boole-validation/remaining-ranges.json',
  controls_sha256=sha('/home/pnord/boole-overnight-20261109/evidence/boole-validation/remaining-ranges.json'),
  limitation='Independent reserved intervals only; earlier Boole history remains separate; no full-box bound. Near-zero fallback region is excluded.')
 atomic(ROOT/'allocation-request.json',request);request_hash=sha(ROOT/'allocation-request.json')
 store=ada_export_store.Store('/mnt/nfs_share/fifth42-shared-20261107');stages=[]
 for spec in request['ranges']:
  until=time.monotonic()+2
  while True:
   try:claim=store.reserve(spec['job'],spec['first'],spec['last'],request_hash,dict(sha256=request_hash,manifest=request));break
   except ada_export_store.Busy:
    if time.monotonic()>=until:raise
    time.sleep(.02)
  name='boole-extra-20261109-'+spec['label'];stage=Path('/home/pnord')/name
  shutil.copytree(TEMPLATE,stage,ignore=shutil.ignore_patterns('__pycache__'))
  w=stage/'worker';c=json.loads((w/'production-config.json').read_bytes())
  for n in ['parent-audit.json','parent-lineage.json']:
   c[n.replace('.json','').replace('-','_')+'_file']=str(w/n)
  # Parent archive/lineage remain a verified historical reference, not adjacent coverage.
  c.update(TEST_ONLY=False,run_id=name,allocation_kind='independent_reserved_interval',reference_parent_cursor=c['initial_patch'],parent_selected_patches=0,
   initial_patch=spec['first'],range_end=spec['last'],stop_epoch=1794351600,stop_local='2026-11-10T17:00:00-06:00',
   service_name=name+'.service',deadline_service_name=name+'-deadline.service',ledger_job=spec['job'],ledger_device=store.device,
   ledger_claim_sha256=claim['sha256'],reservation_initial_patch=claim['first'],reservation_manifest_sha256=request_hash,
   origin_claim_file=str(w/'origin-claim.json'),coverage_file=str(w/'final-coverage.json'),manifest=str(w/'release-manifest.json'),
   authorization='User authorized production until 2026-11-10 17:00 America/Chicago; fresh disjoint uncomputed allocation; earlier coverage kept separate.')
  atomic(w/'origin-claim.json',claim);c['origin_claim_file_sha256']=sha(w/'origin-claim.json')
  coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=c['initial_patch'],parent_checkpoint_sha256=c['parent_checkpoint_sha256'],
   parent_journal_sha256=c['parent_journal_sha256'],covered_intervals=[],prior_history_reference=c['parent_run'],prior_history_cursor=c['reference_parent_cursor'],
   coverage_scope='No parent coverage imported; this fresh reserved interval starts with zero completed cells.',completed_bound=None)
  atomic(w/'final-coverage.json',coverage);c['coverage_sha256']=sha(w/'final-coverage.json')
  local=Path('/home/pnord/fifth42-local-runs')/spec['job']/name;local.mkdir(mode=0o700,parents=True,exist_ok=False)
  replica=Path('/mnt/fifth42-storage/runs')/spec['job']/name/'run';assert not replica.exists()
  c.update(output=str(local/'run'),replica_output=str(replica),local_data_device=local.stat().st_dev,data_device=bulk_data_store.verify_share(replica))
  manifest=dict(host='boole',provenance='Unchanged buffered-r1 mathematics/native binary; reservation snapshot retry; explicit independent allocation guards.',
   upstream_commit='0d48c556825e1e03bc109bdef7232f4555fc0d61',allocation_request_sha256=request_hash,
   files={str(p.relative_to(w)):sha(p) for p in sorted(w.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ('production-config.json','base-config.json','release-manifest.json')},
   external_files={str(p):sha(p) for p in sorted(stage.glob('*.py'))})
  atomic(w/'release-manifest.json',manifest);c['manifest_sha256']=sha(w/'release-manifest.json')
  atomic(w/'base-config.json',c);atomic(w/'production-config.json',c)
  subprocess_code="import sys;sys.path[:0]=sys.argv[1:3];import policy;policy.load_config(sys.argv[3]);print('frozen allocation validated')"
  import subprocess
  subprocess.run([sys.executable,'-B','-c',subprocess_code,str(w),str(w/'source/lattice_gpu'),str(w/'production-config.json')],check=True)
  record=dict(root=str(stage),config=str(w/'production-config.json'),config_sha256=sha(w/'production-config.json'),manifest_sha256=c['manifest_sha256'],
   ledger_job=c['ledger_job'],claim_sha256=claim['sha256'],first=c['initial_patch'],last=c['range_end'],service=c['service_name'])
  atomic(stage/'FROZEN.json',dict(status='frozen',**record));stages.append(record)
 atomic(ROOT/'new-allocations.json',dict(status='frozen',stages=stages,allocation_request_sha256=request_hash))
 print(json.dumps(stages,indent=2))
if __name__=='__main__':main()
