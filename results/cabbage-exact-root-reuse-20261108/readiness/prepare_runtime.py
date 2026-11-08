from pathlib import Path
import hashlib,json,shutil,ast,subprocess
r=Path(__file__).resolve().parent
p=r/'portable-source';m=json.loads((r/'portable-CONTENTS.json').read_text());base=p/'ada-persistent-pipeline'
for f in m['files']:
 path=(p/f['path']) if f['path'].startswith('ada-external-helpers/') else base/f['path']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256'],f['path']
print('All',len(m['files']),'portable file hashes passed.')
runtime=r/'cabbage-runtime';runtime.mkdir()
prior=Path('/home/pnord/scratch/saved-root-followup-DL829jCa')
shutil.copytree(prior/'candidate/source',runtime/'source',ignore=shutil.ignore_patterns('__pycache__','bin'))
shutil.copytree(prior/'device/src',runtime/'native-baseline/src');shutil.copytree(prior/'device/vendor',runtime/'native-baseline/vendor')
shutil.copytree(base/'independent',runtime/'independent')
(runtime/'bin').mkdir();shutil.copy2(prior/'device/bin/scaling_gpu',runtime/'bin/scaling_gpu');shutil.copy2(prior/'native/bin/gmp_reference',runtime/'bin/gmp_reference')
for name in ('packed_worker.py','gpu_validation.py'):shutil.copy2(base/name,runtime/name)
repo=Path('/home/pnord/scratch/saved-root-pAjTHBhR/repo/deployment_snapshots/weekend-20261107/boole/worker')
s=(repo/'policy.py').read_text().replace('Boole derivative','Cabbage admission derivative').replace('boole-release-manifest.json','cabbage-release-manifest.json').replace("=='boole'","=='cabbage'").replace('<=32*1024**3','<=2*1024**3').replace('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/boole-validation','/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk')
start=s.index('def validate_parent(c):');end=s.index('def validate_ledger(c):')
s=s[:start]+'''def validate_parent(c):
 p=Path(c['coverage_file']);require(digest(p)==c['coverage_sha256'],'Admission metadata changed')
 m=json.loads(p.read_text());require(m['host']=='cabbage' and m['proposed_interval']==[2250000000,3000000000],'Admission interval changed')
 require(c['parent_selected_patches']==0,'Fresh Cabbage allocation cannot inherit coverage')
 require(2250000000<=c['initial_patch']<c['range_end']<=3000000000,'Cabbage interval outside admission proposal')
 return m
'''+s[end:]
(runtime/'policy.py').write_text(s)
s=(repo/'boole_supervisor.py').read_text().replace('Boole','Cabbage').replace('/home/pnord/boole-production-validation-20261107/gpu-owner.lock',str(runtime/'gpu-owner.lock'))
(runtime/'cabbage_supervisor.py').write_text(s)
shutil.copyfile(r/'ada-admission-package/ada_export_store.py',runtime/'ada_export_store.py')
shutil.copyfile(r/'ada-admission-package/admission-plan.json',runtime/'admission-plan.json')
files={str(f.relative_to(runtime)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(runtime.rglob('*')) if f.is_file()}
manifest=dict(status='STAGED_CABBAGE_ADMISSION_CANDIDATE',production_launched=False,files=files,source_commit='be5fcb6d5818d70035a9f2a8f31812f5f1f8b53f',portable_source_manifest=m['ada_source_manifest'],candidate_adapter_sha256=files['ada_export_store.py'],actual_gpu_binary='bin/scaling_gpu',actual_kernel='native-baseline/src/kernel.hpp',actual_native_source='native-baseline/src/scaling_gpu.cu',python='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python',compiler='g++-13 13.4.0',cuda='13.2.78 sm_86',notes=['Saved-root two-file patch is unchanged from tested candidate.','Policy/supervisor are Cabbage derivatives of the published Boole runtime, with fresh allocation metadata, Cabbage test namespace and 2 GiB cap.','Store adapter is byte-identical to Ada admission package.','No production claim or production config has been created.'])
(runtime/'cabbage-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Audit source imports only; no historical launch code is invoked.
physical=[];seen=set()
for cpu in sorted(__import__('os').sched_getaffinity(0)):
 d=Path(f'/sys/devices/system/cpu/cpu{cpu}/topology');k=((d/'physical_package_id').read_text().strip(),(d/'core_id').read_text().strip())
 if k not in seen:physical.append(cpu);seen.add(k)
assert physical[:16]==list(range(16))
(r/'runtime-preparation.json').write_text(json.dumps(dict(status='prepared',files=len(files),manifest_sha256=hashlib.sha256((runtime/'cabbage-release-manifest.json').read_bytes()).hexdigest(),portable_contents_verified=len(m['files']),physical_cpus=physical[:16],adapter_matches_ada=True),indent=2)+'\n')
print('Prepared candidate runtime with',len(files),'pinned files and physical CPUs',physical[:16])
