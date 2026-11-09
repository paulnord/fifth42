"""Archive exactly the frozen tested runtimes and the tested once-only queue."""
from datetime import datetime,timezone
import difflib,hashlib,json,os,shutil,sys,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import controller
RETURN=Path('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole')
DEST=RETURN/'handoff-r1'

def copy(source,destination):
 destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
def main():
 DEST.mkdir(mode=0o700,exist_ok=False)
 plan=json.loads((ROOT/'production-plan.json').read_bytes());stages=plan['stages']
 configs=[controller.load_stage(s) for s in stages]
 primary=Path(stages[0]['root']);live=json.loads((primary/'LIVE_VERIFICATION.json').read_bytes())
 assert live['status']=='passed' and json.loads((ROOT/'controller-validation.json').read_bytes())['controller_sha256']==controller.sha(ROOT/'controller.py')
 assert controller.unit('boole-overnight-queue-20261109.service')['ActiveState']=='active'
 bundle_files={}
 for spec,c in zip(stages,configs):
  root=Path(spec['root']);w=root/'worker';prefix=root.name
  manifest=json.loads(Path(c['manifest']).read_bytes())
  for name in manifest['files']:bundle_files[prefix+'/worker/'+name]=w/name
  for path in manifest.get('external_files',{}):bundle_files[prefix+'/'+Path(path).name]=Path(path)
  for name in ('base-config.json','production-config.json','release-manifest.json'):bundle_files[prefix+'/worker/'+name]=w/name
  validation=json.loads((root/'runtime-validation.json').read_bytes())
  assert validation['status']=='passed' and validation['manifest_sha256']==spec['manifest_sha256'] and validation['config_sha256']==spec['config_sha256']
  for name in ('runtime-validation.json','FROZEN.json'):copy(root/name,DEST/'results'/prefix/name)
  # Preserve the actual finite/signal/deadline inputs and outcomes.
  for path in (root/'evidence/boole-validation').rglob('*'):
   if path.is_file() and path.suffix in ('.json','.stderr','.stdout'):copy(path,DEST/'results'/prefix/'service-tests'/path.relative_to(root/'evidence/boole-validation'))
 for path in sorted(ROOT.glob('*.py')):bundle_files['controller/'+path.name]=path
 for name in ('production-plan.json','allocation-request.json','new-allocations.json','controller-validation.json','systemd-launch.json','test-plan.json','test-a-config.json','test-b-config.json','reservation-retry-tests.txt'):
  bundle_files['controller/'+name]=ROOT/name
 for name in ('sealed-parent.json','parent-audit.json','parent-archive-receipt.json','parent-lineage.json','LIVE_VERIFICATION.json','RUN_STATUS.json'):
  copy(primary/name,DEST/'results'/name)
 copy(primary/'evidence/boole-validation/remaining-ranges.json',DEST/'results/remaining-ranges.json')
 old=Path('/home/pnord/boole-buffered-20261109')
 oldcfg=json.loads((old/'worker/production-config.json').read_bytes())
 copy(Path(oldcfg['output']).parent/'supervisor.json',DEST/'results/previous-supervisor-failure.json')
 copy(Path(oldcfg['output'])/'final-replica.json',DEST/'results/previous-final-replica.json')
 baseline=dict(host='boole',upstream_commit='0d48c556825e1e03bc109bdef7232f4555fc0d61',upstream_release_source_tar_sha256='a5149bdfdaa050c998576f8f07b22b39fb88a0b1fd3befb75fceefaffeb5b4f4',
  previous_runtime=str(old),previous_manifest_sha256=controller.sha(old/'worker/release-manifest.json'),previous_config_sha256=controller.sha(old/'worker/production-config.json'),
  previous_final_cursor=3470403072,previous_checkpoint_sha256=controller.sha(Path(oldcfg['output'])/'checkpoint.json'),
  previous_claim_sha256=oldcfg['ledger_claim_sha256'],native_binary_unchanged=True,native_gpu_sha256=controller.sha(primary/'worker/bin/scaling_gpu'),gmp_binary_sha256=controller.sha(primary/'worker/bin/gmp_reference'),
  math_modules_unchanged={n:controller.sha(primary/'worker'/n) for n in ('packed_worker.py','buffered_pipeline.py','scheduling.py','native-baseline/src/kernel.hpp')})
 controller.atomic(DEST/'baseline-identity.json',baseline)
 hashes={name:controller.sha(path) for name,path in sorted(bundle_files.items())}
 with tarfile.open(DEST/'source.tar.gz','w:gz') as tar:
  for name,path in sorted(bundle_files.items()):tar.add(path,arcname=name,recursive=False)
 # Read the completed archive back and compare every archived byte identity.
 with tarfile.open(DEST/'source.tar.gz','r:gz') as tar:
  actual={member.name:hashlib.sha256(tar.extractfile(member).read()).hexdigest() for member in tar.getmembers()}
 assert actual==hashes,'Archive differs from the files tested'
 controller.atomic(DEST/'source-manifest.json',dict(files=hashes,archive_sha256=controller.sha(DEST/'source.tar.gz'),archive_readback='Every archived file SHA256 equals its tested on-disk file',stages=stages,controller_sha256=plan['controller_sha256']))
 patches=[]
 for spec in stages:
  root=Path(spec['root'])
  for name in ('worker/policy.py','worker/boole_supervisor.py','worker/production-config.json','freeze_boole.py','launch_boole.py','validate_boole_services.py','verify_boole_live.py','prepare_node_reporting.py'):
   new=root/name;prior=old/name
   if new.exists():patches.extend(difflib.unified_diff(prior.read_text().splitlines(True) if prior.exists() else [],new.read_text().splitlines(True),fromfile='baseline/'+name,tofile=root.name+'/'+name))
 for path in sorted(ROOT.glob('*.py')):patches.extend(difflib.unified_diff([],path.read_text().splitlines(True),fromfile='/dev/null',tofile='controller/'+path.name))
 (DEST/'changes.patch').write_text(''.join(patches))
 build_commands=[
  '/usr/local/cuda-12.8/bin/nvcc -std=c++17 -O3 -arch=sm_86 -ccbin /usr/bin/g++-13 -I"$WORKER/native-baseline/compat" "$WORKER/native-baseline/src/scaling_gpu.cu" -o "$SCRATCH_BIN/scaling_gpu"',
  '/usr/bin/g++-13 -std=c++17 -O2 "$WORKER/independent/gmp_reference.cpp" -lgmpxx -lgmp -o "$SCRATCH_BIN/gmp_reference"']
 tests=[
  '/home/pnord/boole-results-20261107/venv312/bin/python -B /home/pnord/boole-overnight-20261109/test_reservation_retry.py',
  'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/pnord/boole-results-20261107/venv312/bin/python -B /home/pnord/boole-overnight-20261109/test_allocation_windows.py',
  *['/home/pnord/boole-results-20261107/venv312/bin/python -B -u '+s['root']+'/validate_boole_services.py --revision '+r for s,r in zip(stages,('overnight-r1','extra-a','extra-b'))],
  '/home/pnord/boole-results-20261107/venv312/bin/python -B -u /home/pnord/boole-overnight-controller-20261109/test_controller.py',
  '/home/pnord/boole-results-20261107/venv312/bin/python -B -u /home/pnord/boole-overnight-20261109/verify_boole_live.py']
 handoff=dict(host='boole',status='running_verified',created_utc=datetime.now(timezone.utc).isoformat(),authorization='User: continue production until tomorrow at 5 pm; Continue in unclaimed ranges',
  stop_local='2026-11-10T17:00:00-06:00',compute_shutdown_begins_local='2026-11-10T16:59:50-06:00',final_copy_until_local='2026-11-10T17:30:00-06:00',
  baseline=baseline,stages=stages,controller_plan_sha256=controller.sha(ROOT/'production-plan.json'),controller_sha256=plan['controller_sha256'],
  changes=['Single bounded-retry reservation snapshot replaces separately locked claim and overlap reads. Original digest/grid/ownership/overlap checks remain.',
   'Fresh exact-checkpoint continuation with extended immutable deadline; original frozen runtime/journals retained.',
   'Two fresh uncomputed disjoint reservations, with historical reference kept separate from their coverage.',
   'Tested once-only controller waits for complete endpoint, clean process exit, released leases, final verified copy, and equal raw local/replica hashes before next launch. Failed/partial stages never resume automatically.'],
  compiler='g++-13 13.4.0; CUDA 12.8.93; sm_86',python='/home/pnord/boole-results-20261107/venv312/bin/python',build_commands=build_commands,
  build_this_revision='Native sources and binaries are unchanged; the existing validated Boole binaries were reused in every actual service/GMP comparison.',test_commands=tests,
  results=dict(parent='418366 chunks / 107101696 cells: complete local and replica receipt/GMP audits; full byte hashes equal final receipt; 3269 recorded independent GMP audits',
   reservation_retry='4 passed: transient lock, bounded timeout, bad digest, signed overlap',service_cases='3 cases per frozen runtime: finite 17-chunk dense GMP, signal stop, actual deadline timer; local/replica audits and controls pass; output reuse rejected',
   rollover='Two real finite services completed in order; 17 GMP-audited chunks each, local and replica. Reuse and partial endpoint rejected.',
   remaining_windows='Full GPU/GMP count and candidate-record equality at 100000000, 250000000, 499999744. At 65536, required fallback was rejected; that area was not reserved.',
   live=live),resource_policy=dict(workers=16,physical_cpus=list(range(16)),group_limit=4,dispatch_chunksize=4,ready_queue_limit=3,journal_buffer_records=8,journal_cap_bytes=32*1024**3,local_journals=True,replica_interval_seconds=60,NFS_ownership=True,automatic_resume=False),
  coverage='Only explicitly committed selected intervals. Follow-on reservations are not completed coverage. Earlier coefficients were not all recomputed; no full-box bound.',
  work_limit='679596928 cells were queued at startup. The queue may finish before the deadline; another owner range will not be used without a coordinated assignment. See ../ALLOCATION_REQUEST.json.',
  reporting=dict(queue_status=str(RETURN/'PRODUCTION_STATUS.json'),current_collector='/mnt/nfs_share/boole-overnight-publishing-20261109',new_publisher_admission='Requested in ../READY_FOR_PUBLISHER.json; no new GitHub publication claimed.'),
  service='boole-overnight-20261109.service',queue_service='boole-overnight-queue-20261109.service',logout_safe='systemd user services; Linger=yes',source_archive_readback='passed')
 controller.atomic(DEST/'HANDOFF.json',handoff)
 (DEST/'HANDOFF.txt').write_text('Boole is running with a November 10, 2026 17:00 Central cutoff.\nRead HANDOFF.json, baseline-identity.json and source-manifest.json.\nThe previous run stopped safely after a transient reservation-lock error; its verified final cursor is 3470403072. The new single-snapshot bounded retry is tested.\nCurrent original reservation continues to 3750000000, then separate fresh claims [100000000,300000000) and [300000000,500000000). A once-only systemd controller gates transitions on clean completion and verified final copies. No partial/failed run is resumed.\nThe assigned work may finish early. More coordinated work is requested in ../ALLOCATION_REQUEST.json.\nMonitor ../PRODUCTION_STATUS.json for the active run and its per-run collector share; the old buffered collector identifies the stopped old run.\nTo stop gracefully: stop boole-overnight-queue-20261109.service FIRST, then stop the active compute service named in ../PRODUCTION_STATUS.json. Leave its independent final-copy service running.\nOriginal source and journals are preserved. No search arithmetic, kernel, packet or grouped journal schema changed.\nFresh standalone archive readback verified every source/binary against files used in tests. Native build commands are provided for a scratch directory; do not replace a running frozen binary.\n')
 (DEST/'reproduce.sh').write_text('#!/usr/bin/env bash\nset -euo pipefail\ncd -- "$(dirname -- "$0")"\nsha256sum --check SHA256SUMS\n# Exact test invocations and scratch build commands are recorded in HANDOFF.json.\n# Finite GPU/service tests require an idle host and NEW isolated test revision IDs.\n# Do not rerun production launch scripts or reuse the archived production outputs.\n')
 (DEST/'reproduce.sh').chmod(0o700)
 # Only immutable handoff files are checksummed; live status resides outside this directory.
 files=[p for p in sorted(DEST.rglob('*')) if p.is_file()]
 (DEST/'SHA256SUMS').write_text(''.join(controller.sha(p)+'  '+str(p.relative_to(DEST))+'\n' for p in files))
 for p in files+[DEST/'SHA256SUMS']:
  with p.open('rb') as f:os.fsync(f.fileno())
 ready=dict(status='ready',host='boole',completed_utc=datetime.now(timezone.utc).isoformat(),handoff=str(DEST),source_bundle_sha256=controller.sha(DEST/'source.tar.gz'),source_manifest_sha256=controller.sha(DEST/'source-manifest.json'),handoff_sha256=controller.sha(DEST/'HANDOFF.json'),checksums_sha256=controller.sha(DEST/'SHA256SUMS'),source_archive_readback='passed',production='running_verified')
 controller.atomic(DEST/'READY.json',ready)
 controller.atomic(RETURN/'READY.json',ready)
 controller.atomic('/mnt/nfs_share/boole-buffered-publishing-20261109/NEXT_RUN.json',dict(status='superseded_after_verified_final_copy',next_run_id='boole-overnight-20261109',next_collector='/mnt/nfs_share/boole-overnight-publishing-20261109',handoff=str(DEST),queue_status=str(RETURN/'PRODUCTION_STATUS.json')))
 print(json.dumps(ready,indent=2))
if __name__=='__main__':main()
