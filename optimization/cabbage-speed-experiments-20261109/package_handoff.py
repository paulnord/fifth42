"""Build a reviewable source/result package. READY is deliberately separate."""
import difflib,gzip,hashlib,importlib.metadata,json,os,platform,shutil,subprocess,tarfile
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'handoff-stage';S.mkdir(exist_ok=False)
BASE=Path('/home/pnord/scratch/cabbage-bulk-20261108-98XhJJdw/worker')
RAW=Path('/mnt/fifth42-storage/experiments/integration-20261109/cabbage/rev1')
RAW.mkdir(parents=True,exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def load(p):return json.loads(p.read_text())
def run(command):return subprocess.check_output(command,text=True).strip()
# Completed raw trial directories, including partial attempts, remain available.
shutil.copytree(R/'results',RAW/'results')
for p in R.iterdir():
    if p.is_file() and (p.suffix in ('.txt','.json','.jsonl')) and p.name not in ('validation-packets.json',):shutil.copy2(p,RAW/p.name)
raw_files={str(p.relative_to(RAW)):sha(p) for p in sorted(RAW.rglob('*')) if p.is_file()}
write(RAW/'raw-manifest.json',dict(files=raw_files))

files=[]
for p in R.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(R);parts=rel.parts
    if '__pycache__' in parts:continue
    if parts[0]=='source' and 'bin' not in parts:files.append(p)
    elif parts[0] in ('bin','independent'):files.append(p)
    elif len(parts)==1 and (p.suffix in ('.py','.cpp','.hpp','.cu','.sh') or p.name in ('baseline-manifest.json','baseline-runtime-manifest.json','validation-packets.json')):files.append(p)
files=sorted(set(files));mapping={str(p.relative_to(R)):sha(p) for p in files}
with (S/'source.tar.gz').open('wb') as output:
 with gzip.GzipFile(filename='',fileobj=output,mode='wb',mtime=0) as zipped:
  with tarfile.open(fileobj=zipped,mode='w') as archive:
   for p in files:
    info=archive.gettarinfo(str(p),arcname='tested-source/'+str(p.relative_to(R)));info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
    with p.open('rb') as stream:archive.addfile(info,stream)
commands=load(R/'build-results.json')+load(R/'build-extra-results.json')
executables=[]
for p in sorted((R/'bin').iterdir()):
 if p.is_file():
  match=[x['command'] for x in commands if x['command'][-1]==str(p)]
  executables.append(dict(path=str(p.relative_to(R)),sha256=sha(p),build_command=match[-1] if match else None,
    origin='Frozen tested Cabbage worker executable' if p.name in ('scaling_gpu','gmp_reference') else 'Built in this experiment'))
manifest=dict(schema=1,bundle_root='tested-source',files=mapping,source_bundle_sha256=sha(S/'source.tar.gz'),executables=executables,
    baseline_runtime_manifest_sha256=sha(R/'baseline-runtime-manifest.json'),baseline_copy_manifest_sha256=sha(R/'baseline-manifest.json'),
    compile=dict(cxx=run(['g++-13','--version']).splitlines()[0],nvcc=run(['/home/pnord/scratch/saved-root-pAjTHBhR/cuda-13.2/nvidia/cu13/bin/nvcc','--version']),architecture='sm_86'))
write(S/'source-manifest.json',manifest)

# A patch against the actual frozen worker, with unchanged original source omitted.
code=[p for p in files if p.suffix in ('.py','.cpp','.hpp','.cu','.sh') and 'bin' not in p.relative_to(R).parts]
patch=[];changed=[]
for p in code:
 rel=str(p.relative_to(R));old=BASE/rel
 before=old.read_text().splitlines(keepends=True) if old.exists() else []
 after=p.read_text().splitlines(keepends=True)
 if before!=after:
  patch.extend(difflib.unified_diff(before,after,fromfile='a/'+rel if old.exists() else '/dev/null',tofile='b/'+rel));changed.append(rel)
(S/'changes.patch').write_text(''.join(patch))
verify=R/'patch-verification';verify.mkdir();shutil.copytree(BASE/'source',verify/'source',ignore=shutil.ignore_patterns('__pycache__','bin'))
p=subprocess.run(['patch','--batch','-p1','-i',str(S/'changes.patch')],cwd=verify,capture_output=True,text=True)
if p.returncode:raise RuntimeError(p.stdout+p.stderr)
assert all(sha(verify/name)==mapping[name] for name in changed),'Patch does not reconstruct tested code'
write(S/'patch-verification.json',dict(status='passed',changed_files=changed,stdout=p.stdout))

result_dir=S/'results';result_dir.mkdir()
for name in ['host-matrix','width-matrix','native-benchmark','candidate-matrix']:
 shutil.copy2(R/'results'/name/'summary.json',result_dir/(name+'.json'))
for p in (R/'results').glob('*.json'):shutil.copy2(p,result_dir/p.name)
for p in R.glob('*failure.json'):shutil.copy2(p,result_dir/p.name)
for p in [R/'validation-suite.json',R/'build-results.json',R/'build-extra-results.json',R/'build-attempt1.json',R/'build-before-schema2.json',R/'build-pre-format-fix.json']:
 if p.exists():shutil.copy2(p,result_dir/p.name)
for p in R.glob('*execution.json'):shutil.copy2(p,result_dir/p.name)
shutil.copy2(R/'reproduce.sh',S/'reproduce.sh');(S/'reproduce.sh').chmod(0o755)

host=load(R/'results/host-matrix/summary.json');width=load(R/'results/width-matrix/summary.json');candidate=load(R/'results/candidate-matrix/summary.json');native=load(R/'results/native-benchmark/summary.json')
report=['Cabbage speed experiments, 2026-11-09','',
 'Recommended integration: source/lattice_gpu/speed_options.py, as the initializer of a NEW process. It combines exact GMP roots, structured inverse bounds and the byte-identical direct-field serializer. It preserves existing Task/certificate/packet/coverage/journal formats.',
 '', 'Full 16-physical-core, five-repeat second holdout; actual measured throughput ratios versus the frozen width-8 worker:']
for name,values in candidate['summary'].items():
 report.append(name+': '+', '.join(f"{k} {v['throughput_ratio']:.4f}x (median {v['median_seconds']:.6f}s)" for k,v in values.items()))
report+=['','Wider-patch choices were frozen on separate training strips: low=32, middle=16, high=8. These are selected-strip choices, not a general width policy or production search coverage. Fixed exact ratio union and durable-commit cadence across widths. The initializer at width 8 preserves original geometry, certificates and packets.',
 '', 'Four-core host-only component experiments:']
for name,values in host['summary'].items():report.append(name+': '+', '.join(f"{k} {v['throughput_ratio']:.4f}x" for k,v in values.items()))
report+=['','GPU prepared-packet kernel experiments (not end-to-end pipeline gains):']
for name,values in native['summary'].items():
 best=min(values,key=lambda k:values[k]['kernel_median_seconds']);report.append(f"{name}: best {best}, {values[best]['kernel_speedup_vs_original']:.4f}x kernel throughput")
report+=['','Warm-basis reuse was slower in the tested windows. Modular row wheels and finite-difference prototypes passed correctness but were slower in these samples. Low64 filtering improved isolated kernels. Row clipping/walking helped the wider width-128 packets; these GPU variants are experiments and are not enabled by speed_options.',
 '', 'Correctness: all six host variants passed three nonempty exhaustive small domains and five high-shell windows with independent GMP full-record comparisons and tamper rejection. All six experimental GPU paths passed 51 packets, invalid input/error recovery, and separate evaluated/excluded count checks. The large nonempty Healy fixture passed all seven GPU paths. Finite differences matched Python big integers for 21,741 steps in normal and UBSan builds. Twenty-four targeted existing tests passed, including sanitizer/native nonempty checks and durable-prefix recovery.',
 '', 'GPU experiment schema 2: points_visited is explicitly evaluated points, points_exactly_excluded is mathematically excluded points, and points_accounted is their sum. Each task has expected/accounted/visited/exactly_excluded. This intentionally needs an adapter before integration into the original decoder; the recommended host initializer uses the original GPU binary and original schemas.',
 '', 'Timing includes fresh geometry, independent exact certification, bounded prefetch, original CUDA execution, exact output checks, first-chunk GMP audit and durable local commits. Startup/shutdown/recovery are separate. Every raw sample is retained. Five counterbalanced repetitions. Unrelated recurring Java work interrupted several stages; incomplete attempts are retained and excluded. Monitoring samples approximately every 0.5s and cannot exclude shorter contention bursts. Selected tests are short and machine-specific.',
 '', 'Baseline runtime manifest SHA256: '+manifest['baseline_runtime_manifest_sha256'],
 'Raw evidence: '+str(RAW),
 'No production worker, service, ledger or search coverage was changed. Ada owns release integration.']
(S/'REPORT.txt').write_text('\n'.join(report)+'\n')
handoff=dict(schema=1,host='cabbage',created_utc=datetime.now(timezone.utc).isoformat(),status='tested; pending archive reproduction and final publication',
 baseline=dict(repository='paulnord/fifth42',reporting_main_commit='dffdff748ad1bed40a8875ecb0cb6a0551aec51d',runtime_directory=str(BASE),
   runtime_manifest_sha256=manifest['baseline_runtime_manifest_sha256'],copy_manifest_sha256=manifest['baseline_copy_manifest_sha256'],frozen_executables=[x for x in executables if x['origin'].startswith('Frozen')]),
 tested_source_manifest_sha256=sha(S/'source-manifest.json'),source_bundle_sha256=sha(S/'source.tar.gz'),changed_files=changed,
 recommendation=dict(initializer='source/lattice_gpu/speed_options.py',fresh_process_required=True,baseline_width_8_identity_preserved=True,chosen_widths=candidate['selection'],width_policy_scope='Three tested ratio neighborhoods only; integrate with exact region accounting, not local benchmark patch IDs.'),
 environment=dict(hostname=platform.node(),python=platform.python_version(),packages={x:importlib.metadata.version(x) for x in ['gmpy2','fpylll','cysignals','numpy','sympy']},
  gpu=run(['nvidia-smi','--query-gpu=name,driver_version,memory.total','--format=csv,noheader']),compile=manifest['compile']),
 results=dict(host_components='results/host-matrix.json',width_training_and_first_holdout='results/width-matrix.json',kernel_only='results/native-benchmark.json',
  reusable_16core_second_holdout='results/candidate-matrix.json',correctness='results/final-validation-suite.json',large_nonempty_control='results/large-nonempty-fixture.json'),
 tested_windows=dict(shell=[100000000001,200000000000],training_left_ratios=[[6,25],[7,20],[17,20]],ratio_span=[16384,100000000001],first_holdout_offset=[1,100000],second_holdout_offset=[2,100000],
  local_patch_ids=True,production_ledger_ids=False,all_mathematical_hit_sets_preserved=True),
 schema_changes=dict(recommended_host_initializer='None',experimental_gpu_output='Schema 2: visited/evaluated and exactly-excluded separated, accounted sum; per-task accounted/visited/exactly_excluded. Original decoder adaptation required.',
  packet='Unchanged LATTICE_GPU_V1',certificate='Unchanged for host arithmetic and serializer; warm basis and widths legitimately change geometry/certificates.',journal='Original schema for timed host pipelines; GPU experiments were not journal-integrated.'),
 raw_evidence=dict(path=str(RAW),ada_physical_path=str(RAW).replace('/mnt/fifth42-storage','/mnt/localstorage/pnord/fifth42-storage'),manifest_sha256=sha(RAW/'raw-manifest.json')),
 limitations=report[-9:],production_used_code=False,production_coverage=False,
 reproduction=dict(command='./reproduce.sh /absolute/new/output /absolute/pinned/python /absolute/nvcc',optional_full_benchmarks='Add --benchmarks as fourth argument',
  commands=[x['command'] for x in commands],pinned_dependencies='Python 3.12; gmpy2 2.2.2, fpylll 0.6.4, cysignals 1.12.5, numpy 2.3.5, sympy 1.14.0; GMP C++ development libraries; g++-13; CUDA 13.2 sm_86 tested.'),
 publication=None)
write(S/'HANDOFF.json',handoff)
write(R/'package-state.json',dict(stage=str(S),raw=str(RAW),source_files=len(files),archive_sha256=sha(S/'source.tar.gz')))
print(json.dumps(dict(stage=str(S),raw=str(RAW),files=len(files),archive_bytes=(S/'source.tar.gz').stat().st_size)),flush=True)
