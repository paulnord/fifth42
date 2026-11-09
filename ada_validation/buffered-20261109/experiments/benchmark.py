"""Balanced, same-input, end-to-end comparison of memory and durable buffering."""
from datetime import datetime,timezone
import hashlib,json,os
from pathlib import Path
import statistics,subprocess,time
from run_validation import helper
ROOT=Path(__file__).resolve().parent
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'

def execute(phase,cases,repeats,patches,results,guard):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1')
    output=Path('/home/pnord/fifth42-local-benchmarks/TEST_ONLY_buffering_20261109')/phase;output.mkdir(mode=0o700,parents=True,exist_ok=False)
    signatures={};expected={};rows=[]
    for repeat in range(repeats):
        order=cases[repeat%len(cases):]+cases[:repeat%len(cases)]
        if repeat%2:order=list(reversed(order))
        for region,first,factor,variant,workers in order:
            guard.idle_gpu();name=f'{region}-{variant}-w{workers}-{repeat}';folder=output/name
            command=[PYTHON,'-B',str(ROOT/'trial.py'),'--variant',variant,'--workers',str(workers),'--first',str(first),'--patches',str(patches),'--group-limit',str(factor),'--output',str(folder)]
            began=time.monotonic()
            with (results/(name+'.stdout.log')).open('x') as out,(results/(name+'.stderr.log')).open('x') as err:
                done=subprocess.run(command,cwd=ROOT,stdout=out,stderr=err,env=env,timeout=180)
            if done.returncode:raise RuntimeError('Trial failed: '+name)
            guard.idle_gpu();row=json.loads((folder/'result.json').read_bytes());key=(region,first,factor)
            science=(row['points'],row['physical_tasks'],row['hits'])
            if key not in signatures:signatures[key]=row['signatures_sha256'];expected[key]=science
            assert row['signatures_sha256']==signatures[key] and science==expected[key],'Scientific inputs, certificates, packets, counts or candidates changed'
            row.update(region=region,repeat=repeat,output=str(folder),elapsed_with_setup_and_audit_seconds=time.monotonic()-began);rows.append(row)
            (results/'progress.json').write_text(json.dumps(dict(completed=len(rows),planned=repeats*len(cases),last=row),indent=2)+'\n')
            print(json.dumps({k:row[k] for k in ('region','variant','workers','repeat','steady_seconds','patches_per_second')}),flush=True)
    summaries=[]
    for region in sorted({r['region'] for r in rows}):
        subset=[r for r in rows if r['region']==region];labels=sorted({(r['variant'],r['workers']) for r in subset})
        medians={f'{variant}-w{workers}':statistics.median(r['steady_seconds'] for r in subset if r['variant']==variant and r['workers']==workers) for variant,workers in labels}
        baseline=medians.get('baseline-w16')
        summaries.append(dict(region=region,median_seconds=medians,throughput_vs_baseline={name:baseline/value for name,value in medians.items()} if baseline else None))
    report=dict(status='passed',phase=phase,checked_utc=datetime.now(timezone.utc).isoformat(),same_scientific_inputs=True,
          same_candidate_sets=True,all_durable_modes_independently_audited_and_reopened=True,includes_final_buffer_drain=True,
          volatile_ram_mode_is_upper_bound_only=True,production_started=False,summary=summaries,trials=rows)
    (results/'results.json').write_text(json.dumps(report,indent=2)+'\n');return report

def main():
    assert json.loads((ROOT/'validation.json').read_bytes())['status']=='passed'
    baseline=json.loads((ROOT/'baseline-identity.json').read_bytes())
    files={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('buffered_pipeline.py','trial.py','benchmark.py','test_buffering.py','run_validation.py')}
    manifest=dict(status='isolated_experiment',baseline_manifest_sha256=baseline['manifest_sha256'],experiment_files=files,compute_sources=baseline['files'])
    (ROOT/'experiment-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    guard=helper();resources=guard.resources();assert not guard.hardware_blockers();handles,leased=guard.acquire_leases(resources,False)
    results=ROOT/'screening';results.mkdir(mode=0o700,exist_ok=False)
    variants=['baseline','encode_once','cache','buffer8','cache_buffer8','cache_buffer32','cache_async8','cache_ram']
    try:
        report=execute('screening',[('ada',4398843264,2,v,16) for v in variants],5,32768,results,guard)
        print(json.dumps(dict(status='passed',summary=report['summary']),indent=2),flush=True)
    finally:
        for handle in handles:handle.close()
if __name__=='__main__':main()
