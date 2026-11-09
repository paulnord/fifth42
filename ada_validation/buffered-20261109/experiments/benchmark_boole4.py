from datetime import datetime,timezone
import hashlib,json,os,statistics,subprocess,time
from pathlib import Path
from run_validation import helper
ROOT=Path(__file__).resolve().parent;PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
def main():
    assert json.loads((ROOT/'scheduling-validation.json').read_bytes())['status']=='passed'
    names=['buffered_pipeline.py','scheduling.py','trial_boole4.py','test_scheduling.py','benchmark_boole4.py']
    manifest=dict(status='scheduling_experiment',baseline_manifest_sha256=json.loads((ROOT/'baseline-identity.json').read_bytes())['manifest_sha256'],experiment_files={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names})
    (ROOT/'experiment-manifest-boole4.json').write_text(json.dumps(manifest,indent=2)+'\n')
    guard=helper();resources=guard.resources();assert not guard.hardware_blockers();handles,leased=guard.acquire_leases(resources,False)
    results=ROOT/'boole4-holdout';results.mkdir(mode=0o700,exist_ok=False)
    out=Path('/home/pnord/fifth42-local-benchmarks/TEST_ONLY_buffering_20261109/boole4-holdout');out.mkdir(mode=0o700,exist_ok=False)
    settings=[('baseline',16,8,1),('cache_buffer8',16,8,1),('cache_buffer8',16,4,1)]
    rows=[];science={}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1')
    try:
        for region,first,factor in [('boole',3336181248,4)]:
            for repeat in range(5):
                order=settings[repeat:]+settings[:repeat]
                if repeat%2:order=list(reversed(order))
                for variant,workers,map_chunk,prep_windows in order:
                    label=f'{variant}-w{workers}-m{map_chunk}-p{prep_windows}';name=f'{region}-{label}-{repeat}';folder=out/name
                    guard.idle_gpu();cmd=[PYTHON,'-B',str(ROOT/'trial_boole4.py'),'--variant',variant,'--workers',str(workers),'--first',str(first),'--patches','32768','--group-limit',str(factor),'--map-chunksize',str(map_chunk),'--prep-windows',str(prep_windows),'--output',str(folder)]
                    with (results/(name+'.stdout.log')).open('x') as log,(results/(name+'.stderr.log')).open('x') as err:
                        done=subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=err,timeout=180)
                    if done.returncode:raise RuntimeError('Scheduling test failed: '+name)
                    row=json.loads((folder/'result.json').read_bytes());fingerprint=(row['signatures_sha256'],row['points'],row['physical_tasks'],row['hits'])
                    if region not in science:science[region]=fingerprint
                    assert science[region]==fingerprint,'Scheduling changed scientific inputs, counts or candidates'
                    row.update(region=region,repeat=repeat,label=label,output=str(folder));rows.append(row)
                    (results/'progress.json').write_text(json.dumps(dict(completed=len(rows),planned=15,last=row),indent=2)+'\n')
                    print(json.dumps({k:row[k] for k in ('region','label','repeat','steady_seconds','patches_per_second')}),flush=True)
        summary=[]
        for region in ('boole',):
            part=[r for r in rows if r['region']==region];medians={label:statistics.median(r['steady_seconds'] for r in part if r['label']==label) for label in sorted({r['label'] for r in part})}
            baseline=medians['baseline-w16-m8-p1'];summary.append(dict(region=region,median_seconds=medians,throughput_vs_baseline={label:baseline/value for label,value in medians.items()}))
        (results/'results.json').write_text(json.dumps(dict(status='passed',summary=summary,trials=rows,same_scientific_inputs=True,ready_depth_instrumented=True),indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
    finally:
        for h in handles:h.close()
if __name__=='__main__':main()
