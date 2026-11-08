"""Finite CPU-approved source variants through one range-corrected CUDA engine."""
import hashlib,json,os,statistics,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
out=root/'gpu-results';out.mkdir(exist_ok=False)
def call(variant,operation,path,*args):
 env=dict(os.environ,ROOT_REUSE_VARIANT=variant,GPU_LOG=str(path)+'.raw.json',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 command=[sys.executable,str(root/'gpu_probe.py'),operation,'--output',str(path),*args]
 with Path(str(path)+'.txt').open('w') as log:
  subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=140)
 return json.loads((path if operation=='validate' else path/'result.json').read_text())
validations=[call(v,'validate',out/f'validation-{v}.json') for v in ('baseline','candidate')]
assert validations[0]['cases']==validations[1]['cases'],'Baseline/candidate GPU validation mismatch'
old=json.loads(Path('/home/pnord/scratch/saved-root-pAjTHBhR/cpu/validation-baseline.json').read_text())
for now,prior in zip(validations[0]['cases'],old['cases'][:8]):
 assert {k:v for k,v in now.items() if k not in ('binary','counts','native_hits')}=={k:v for k,v in prior.items() if k not in ('binary','counts','native_hits')},'Prior CPU geometry/certificates/hit mismatch'
 if 'counts' in prior:assert now['counts']==prior['counts']
print('All 8 GPU baseline/candidate exact validation records match each other and prior CPU identities/hits; GMP counts/full records and nonempty oracles passed.',flush=True)
rows=[];start=time.monotonic()
for case,first,patches in [('boole',3000000000,4096),('ada',3917103232,4096),('higher_cost',10625000000,1024)]:
 for repeat in range(5):
  pair=[]
  for variant in (('baseline','candidate') if repeat%2==0 else ('candidate','baseline')):
   r=call(variant,'benchmark',out/f'{case}-{repeat}-{variant}','--first',str(first),'--patches',str(patches))
   r.update(case=case,repeat=repeat);rows.append(r);pair.append(r)
   print(json.dumps({k:r[k] for k in ('case','repeat','variant','steady_seconds','native_engine_seconds','cuda_kernel_seconds','points')}),flush=True)
  for key in ('signatures_sha256','native_records_sha256','points','exact_hits'):
   assert pair[0][key]==pair[1][key],f'Paired GPU mismatch: {key}'
  (out/'progress.json').write_text(json.dumps(dict(passed_pairs=len(rows)//2),indent=2)+'\n')
summary=[]
for case in ('boole','ada','higher_cost'):
 group={v:[r for r in rows if r['case']==case and r['variant']==v] for v in ('baseline','candidate')}
 med={v:statistics.median(r['steady_seconds'] for r in g) for v,g in group.items()}
 summary.append(dict(case=case,medians=med,throughput_ratio=med['baseline']/med['candidate'],samples={v:[{k:r[k] for k in ('repeat','steady_seconds','startup_seconds','shutdown_seconds','native_engine_seconds','cuda_kernel_seconds','gpu_rpc_seconds','points')} for r in g] for v,g in group.items()}))
report=dict(status='passed',cuda_executed=True,production_coverage=False,elapsed_benchmark_seconds=time.monotonic()-start,summary=summary,rows=[{k:v for k,v in r.items() if k!='rows'} for r in rows],limitations=['Bounded selected windows only; no full-shell search.','Local fresh journals; no NFS/shared production ledger.','Same range-corrected native binary for both host source variants.','Four logical CPUs, unpinned clock frequency; short samples and monitoring may perturb timings.','Startup/shutdown separate; raw timings preserved; no general GPU speedup claim.'])
(out/'benchmark-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(summary,indent=2),flush=True)
