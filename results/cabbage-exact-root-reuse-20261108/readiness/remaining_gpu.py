import hashlib,json,os,statistics,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
prior=Path('/home/pnord/scratch/saved-root-followup-DL829jCa')
out=root/'remaining-gpu';out.mkdir(exist_ok=False)
rows=[]
for repeat in range(5):
 pair=[]
 for variant in (('baseline','candidate') if repeat%2==0 else ('candidate','baseline')):
  path=out/f'higher_cost-{repeat}-{variant}'
  env=dict(os.environ,ROOT_REUSE_VARIANT=variant,GPU_LOG=str(path)+'.raw.json',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
  with Path(str(path)+'.txt').open('w') as log:
   subprocess.run([sys.executable,str(prior/'gpu_probe.py'),'benchmark','--first','10625000000','--patches','1024','--output',str(path)],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=45)
  r=json.loads((path/'result.json').read_text());r.update(case='higher_cost',repeat=repeat);rows.append(r);pair.append(r)
  print(json.dumps({k:r[k] for k in ('repeat','variant','steady_seconds','points','cuda_kernel_seconds')}),flush=True)
 for k in ('signatures_sha256','native_records_sha256','points','exact_hits'):assert pair[0][k]==pair[1][k],k
 (out/'progress.json').write_text(json.dumps(dict(passed_pairs=repeat+1)))
med={v:statistics.median(r['steady_seconds'] for r in rows if r['variant']==v) for v in ('baseline','candidate')}
report=dict(status='passed',cuda_executed=True,production_coverage=False,source_session=str(prior),medians=med,throughput_ratio=med['baseline']/med['candidate'],rows=[{k:v for k,v in r.items() if k!='rows'} for r in rows],limitations=['Five fresh higher-cost pairs; previous interrupted pair excluded.','Earlier two windows were measured in a separate idle session.','Local fresh journals; NFS acceptance is separate.'])
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(med),flush=True)
