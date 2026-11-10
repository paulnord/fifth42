"""Write the exact tested code, all 67 immutable configurations, and queue evidence."""
from datetime import datetime,timezone
import difflib,hashlib,json,os,shutil,subprocess,sys,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import controller
DEST=Path('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole/delegated-r1')

def main():
 controller.require(json.loads((ROOT/'LOCAL_VALIDATION_STATUS.json').read_bytes())['status']=='passed','Actual local validation is not complete')
 controller.require(json.loads((ROOT/'LIVE_VERIFICATION.json').read_bytes())['status']=='passed','Expanded production live verification did not pass')
 controller.require(json.loads((ROOT/'INSTALL_STATUS.json').read_bytes())['status']=='expanded_queue_started','Replacement queue is not installed')
 controller.require(controller.unit('boole-delegated-queue-20261109.service')['ActiveState']=='active','Expanded queue is not running')
 live=json.loads((ROOT/'PRODUCTION_STATUS.json').read_bytes());controller.require(live['status']=='running' and live.get('active'),'No active production stage')
 DEST.mkdir(mode=0o700,parents=True,exist_ok=False);(DEST/'results').mkdir()
 states=json.loads((ROOT/'stages.json').read_bytes())['stages'];first=Path(states[0]['root']);w=first/'worker'
 common=json.loads((w/'release-manifest.json').read_bytes());files={}
 for name in common['files']:files['common/worker/'+name]=w/name
 for p in first.glob('*.py'):files['common/'+p.name]=p
 reconstruction=[]
 for stage in states:
  c=controller.load_stage(stage);root=Path(stage['root']);worker=root/'worker';manifest=json.loads(Path(c['manifest']).read_bytes());prefix='stages/'+c['run_id']
  delta=[]
  for name,h in manifest['files'].items():
   if common['files'].get(name)!=h:files[prefix+'/worker/'+name]=worker/name;delta.append(name)
  for name in ('release-manifest.json','base-config.json','production-config.json'):files[prefix+'/worker/'+name]=worker/name
  files[prefix+'/runtime-validation.json']=root/'runtime-validation.json'
  reconstruction.append(dict(run_id=c['run_id'],manifest_sha256=stage['manifest_sha256'],config_sha256=stage['config_sha256'],delta_files=delta))
 for path in ROOT.glob('*.py'):files['controller/'+path.name]=path
 for name in ('production-plan.json','stages.json','guard-validation.json','actual-gpu-validation.json','GITHUB_VERIFICATION.json'):
  files['controller/'+name]=ROOT/name
 hashes={name:controller.sha(p) for name,p in sorted(files.items())}
 with tarfile.open(DEST/'source.tar.gz','w:gz') as tar:
  for name,p in sorted(files.items()):tar.add(p,arcname=name,recursive=False)
 with tarfile.open(DEST/'source.tar.gz','r:gz') as tar:
  contents={m.name:tar.extractfile(m).read() for m in tar.getmembers() if m.isfile()}
  controller.require({n:hashlib.sha256(b).hexdigest() for n,b in contents.items()}==hashes,'Source archive readback differs')
  for spec in reconstruction:
   prefix='stages/'+spec['run_id']+'/worker/';manifest=json.loads(contents[prefix+'release-manifest.json'])
   controller.require(hashlib.sha256(contents[prefix+'release-manifest.json']).hexdigest()==spec['manifest_sha256'],'Reconstructed manifest changed')
   controller.require(hashlib.sha256(contents[prefix+'production-config.json']).hexdigest()==spec['config_sha256'],'Reconstructed config changed')
   for external,h in manifest.get('external_files',{}).items():
    controller.require(hashlib.sha256(contents['common/'+Path(external).name]).hexdigest()==h,'Reconstructed helper differs')
   for name,h in manifest['files'].items():
    member=prefix+name if prefix+name in contents else 'common/worker/'+name
    controller.require(hashlib.sha256(contents[member]).hexdigest()==h,'Reconstructed frozen source differs: '+name)
 controller.atomic(DEST/'source-manifest.json',dict(files=hashes,reconstruction=reconstruction,archive_readback='All archived bytes and all 67 reconstructed frozen runtimes match the tested files',source_archive_sha256=controller.sha(DEST/'source.tar.gz')))
 for name in ('guard-validation.json','actual-gpu-validation.json','LOCAL_VALIDATION_STATUS.json','INSTALL_STATUS.json','PRODUCTION_STATUS.json','GITHUB_VERIFICATION.json','LIVE_VERIFICATION.json','validation-service-launch.json','installer-launch.json'):
  shutil.copy2(ROOT/name,DEST/'results'/name)
 shutil.copy2(ROOT/'INSTALL_FAILURE.json',DEST/'results/installer-first-attempt-failure.json')
 shutil.copy2(ROOT/'install.stderr',DEST/'results/installer-first-attempt.stderr')
 for name in ('actual-gpu.stdout','actual-gpu.stderr','controller-tests.log'):shutil.copy2(ROOT/name,DEST/'results'/name)
 for p in (first/'evidence/boole-validation').rglob('*'):
  if p.is_file():
   dest=DEST/'results/service-tests'/p.relative_to(first/'evidence/boole-validation');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 baseline=Path('/home/pnord/boole-extra-20261109-b')
 ident=dict(baseline_manifest_sha256=controller.sha(baseline/'worker/release-manifest.json'),baseline_config_sha256=controller.sha(baseline/'worker/production-config.json'),
  protected_allocation_commit='3a17f457780c87987feec1586688b24854666ecf',grant_sha256='7c8422f5e9086519db3bc8ad2e8eeab8d7d1d60706f9b327766ba0a069c6a389',
  native_gpu_sha256=common['files']['bin/scaling_gpu'],native_gmp_sha256=common['files']['bin/gmp_reference'],native_rebuild=False,
  math_modules={n:common['files'][n] for n in ('packed_worker.py','buffered_pipeline.py','scheduling.py','width_coverage.py','native-baseline/src/kernel.hpp')},
  note='Baseline source and journals preserved. Separate child-claim proof is pinned per fresh configuration. No mathematical/packet/grouped-journal schema changes.')
 controller.atomic(DEST/'baseline-identity.json',ident)
 patches=[]
 for name in ('worker/policy.py','worker/suballocation_guard.py','validate_boole_services.py','test_coordinator.py'):
  new=first/name;old=baseline/name
  patches.extend(difflib.unified_diff(old.read_text().splitlines(True) if old.exists() else [],new.read_text().splitlines(True),fromfile='baseline/'+name,tofile='delegated/'+name))
 patches.extend(difflib.unified_diff(Path('/home/pnord/boole-overnight-controller-20261109/controller.py').read_text().splitlines(True),(ROOT/'controller.py').read_text().splitlines(True),fromfile='baseline/controller.py',tofile='controller/controller.py'))
 for name in ('delegated_publication.py','validate_at_boundary.py','install_after_validation.py','install_r2.py'):
  patches.extend(difflib.unified_diff([],(ROOT/name).read_text().splitlines(True),fromfile='/dev/null',tofile='controller/'+name))
 (DEST/'changes.patch').write_text(''.join(patches))
 plan=json.loads((ROOT/'production-plan.json').read_bytes());actual=json.loads((ROOT/'actual-gpu-validation.json').read_bytes())
 handoff=dict(host='boole',status='queued_and_running_existing_work',completed_utc=datetime.now(timezone.utc).isoformat(),authorization='User: validate Ada handoff locally and append all claims after the existing queue',
  stop_local='2026-11-10T17:00:00-06:00',compute_shutdown_begins_local='2026-11-10T16:59:50-06:00',final_copy_until_local='2026-11-10T17:30:00-06:00',
  additional_cells=4250000001,additional_claims=67,new_queue_stages=70,additional_interval=[7000000000,11250000001],claim_span_cells=64000000,
  queue_plan_sha256=controller.sha(ROOT/'production-plan.json'),controller_sha256=plan['controller_sha256'],existing_stages_preserved=plan['stages'][:3],new_stages=states,
  allocation_guard='Exact Ada module pinned by source manifest and called by load_config/validate_ledger at admission and every five seconds in the supervisor. Failure stops gracefully.',
  source_reconstruction='Copy common/ to a fresh scratch root, then overlay stages/<run_id>/worker/. Every reconstructed manifest/config/source/native byte was checked in a fresh archive readback.',
  binary_build='Reused exactly the validated Boole CUDA 12.8.93 / g++13.4 / sm86 binaries; no rebuild or arithmetic change. bin/scaling_gmp is a byte-identical reporting alias of gmp_reference.',
  build_commands=['/usr/local/cuda-12.8/bin/nvcc -std=c++17 -O3 -arch=sm_86 -ccbin /usr/bin/g++-13 -I"$WORKER/native-baseline/compat" "$WORKER/native-baseline/src/scaling_gpu.cu" -o "$SCRATCH_BIN/scaling_gpu"','/usr/bin/g++-13 -std=c++17 -O2 "$WORKER/independent/gmp_reference.cpp" -lgmpxx -lgmp -o "$SCRATCH_BIN/gmp_reference"'],
  test_commands=['/home/pnord/boole-results-20261107/venv312/bin/python -B -u '+str(ROOT/'test_guard_local.py'),'/home/pnord/boole-results-20261107/venv312/bin/python -B '+str(ROOT/'test_controller_local.py'),'/home/pnord/boole-results-20261107/venv312/bin/python -B -u '+str(first/'validate_boole_services.py')+' --revision delegated-r1'],
  tests=dict(local_guard='7 passed including real NFS lease loss, stale heartbeat and scope rejection; production grant checked from Boole',controller='6 passed: exact archive, immutable identities, partial/reuse rejection, completed-stage adoption without restart',
   actual_gpu_cases=[dict(case=r['case'],chunks=r['checkpoint']['chunks'],gmp_audited_chunks=r['local_audit']['new_gmp_audited_chunks'],status=r['status']) for r in actual['cases']],
   checks='Nonempty controls, exact native/GMP counts and full records, original grid, child owner exclusion, local/replica audits and readback, source hashes, buffer drain and actual deadline timer.',
   per_stage_scope='All 67 immutable child configurations validated locally. Executable code is byte-identical across them and tested on actual GPU in representative stage00. Each production stage runs its own controls and first-chunk independent GMP before commit.'),
  installer_recovery='First installer stopped safely before launch because systemd had already unloaded the stopped old queue unit. R2 checks inactivity before issuing stop, then starts the exact unchanged expanded queue. Both original failure and successful install are preserved in results.',
  timing='Current compute completed naturally; no compute restart to change controller. Local finite/GMP/signal/deadline checks ran at that boundary. See exact service commands, timestamps and timings in results.',
  reporting=dict(stable_share='/mnt/nfs_share/boole-delegated-publishing-20261109',switch='At first verified delegated replica, identity-bound evidence is copied and active-publication-spec.json written last for Ada relay admission.',publication_now='Existing first three collectors and publisher paths retained; delegated publishing becomes active when its first stage starts.'),
  live_state=live,coverage='Reservations are not completed coverage; disjoint parent_selected_patches remains zero; no full-box bound.',automatic_resume=False)
 controller.atomic(DEST/'HANDOFF.json',handoff)
 (DEST/'HANDOFF.txt').write_text('Boole appended all 67 protected claims after the unchanged three-stage queue (70 stages total).\nThe active compute was allowed to complete naturally. Actual Boole finite GPU, graceful signal and deadline tests passed before replacement controller admission. No compute was restarted to change controllers.\nThe exact Ada guard is checked at admission and at least every five seconds; live heartbeat and original-parent lease are required.\nDeadline remains November 10 at 17:00 Central; cleanup begins 16:59:50.\nMonitor ../PRODUCTION_STATUS.json for the current stage. Stop boole-delegated-queue-20261109.service before stopping active compute; leave final-copy service running.\nDelegated stages use the stable collector share specified in HANDOFF.json; active-publication-spec is only written after a verified replica. Ada relay admission is checked there when the delegated work actually starts.\nsource.tar.gz contains common exact source and per-claim metadata overlays; source-manifest.json records every file and all 67 reconstruction checks.\n')
 (DEST/'reproduce.sh').write_text('#!/usr/bin/env bash\nset -euo pipefail\ncd -- "$(dirname -- "$0")"\nsha256sum --check SHA256SUMS\n# Exact test/build commands are in HANDOFF.json. Use scratch outputs and unique TEST_ONLY revision IDs on an idle GPU.\n# Never reuse archived production output directories or replace a running frozen file.\n')
 (DEST/'reproduce.sh').chmod(0o700)
 allfiles=[p for p in sorted(DEST.rglob('*')) if p.is_file()]
 (DEST/'SHA256SUMS').write_text(''.join(controller.sha(p)+'  '+str(p.relative_to(DEST))+'\n' for p in allfiles))
 for p in allfiles+[DEST/'SHA256SUMS']:
  with p.open('rb') as f:os.fsync(f.fileno())
 ready=dict(status='ready',host='boole',completed_utc=datetime.now(timezone.utc).isoformat(),source_bundle_sha256=controller.sha(DEST/'source.tar.gz'),source_manifest_sha256=controller.sha(DEST/'source-manifest.json'),handoff_sha256=controller.sha(DEST/'HANDOFF.json'),plan_sha256=handoff['queue_plan_sha256'],additional_claims=67,additional_reserved_cells=4250000001,queue_stages=70,local_gpu_validation='passed',source_archive_readback='passed',active_stage=live['active'])
 controller.atomic(DEST/'READY.json',ready)
 print(json.dumps(ready,indent=2),flush=True)
if __name__=='__main__':main()
