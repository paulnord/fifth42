"""Balanced end-to-end group 2/4 comparison on identical original-grid cells."""
import hashlib, json, os, statistics, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from validate_sources import helper
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'

def main():
    guard=helper(); resources=guard.resources()
    assert not guard.hardware_blockers()
    handles,leased=guard.acquire_leases(resources,False)
    out=Path('/home/pnord/fifth42-local-benchmarks/TEST_ONLY_ada_group4_20261109')
    out.mkdir(mode=0o700,parents=True,exist_ok=False)
    logdir=ROOT/'benchmarks';logdir.mkdir(mode=0o700)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',SCALING_LATTICE_SOURCE=str(ROOT/'worker/source/lattice_prototype'),PYTHONPATH=str(ROOT/'worker')+':'+str(ROOT/'worker/source/lattice_gpu'))
    rows=[]; fingerprints={}; candidates=None
    first=4434273664; patches=32768
    try:
        for repeat in range(5):
            order=[(2,8),(4,4)] if repeat%2==0 else [(4,4),(2,8)]
            for group,dispatch in order:
                name=f'ada-g{group}-d{dispatch}-r{repeat}'; folder=out/name
                guard.idle_gpu()
                cmd=[PYTHON,'-B',str(ROOT/'trial_groups.py'),'--variant','cache_buffer8','--workers','16','--first',str(first),'--patches',str(patches),'--group-limit',str(group),'--map-chunksize',str(dispatch),'--prep-windows','1','--output',str(folder)]
                with (logdir/(name+'.stdout.log')).open('x') as log, (logdir/(name+'.stderr.log')).open('x') as err:
                    done=subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=err,timeout=150)
                assert done.returncode==0, name+' failed; see stderr'
                row=json.loads((folder/'result.json').read_bytes())
                assert row['status']=='passed' and row['first']==first and row['patches']==patches and row['recovery_passed']
                fp=(row['signatures_sha256'],row['points'],row['physical_tasks'],row['hits'])
                if group in fingerprints: assert fingerprints[group]==fp
                else: fingerprints[group]=fp
                if candidates is None: candidates=row['hits']
                assert row['hits']==candidates, 'Candidate sets differ across groupings'
                row.update(repeat=repeat,output=str(folder),command=cmd);rows.append(row)
                print(json.dumps({k:row[k] for k in ('group_limit','repeat','steady_seconds','patches_per_second','hits')}),flush=True)
        medians={str(group):statistics.median(r['steady_seconds'] for r in rows if r['group_limit']==group) for group in (2,4)}
        report=dict(status='passed',first=first,patches=patches,repeats=5,original_width8_interval=[first,first+patches],identical_candidate_sets=True,complete_logical_coverage=True,independent_gmp_per_trial=True,median_seconds=medians,throughput_ratio_group4_over_group2=medians['2']/medians['4'],trials=rows)
        (ROOT/'selection-results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='trials'},indent=2),flush=True)
    finally:
        for handle in handles: handle.close()

if __name__=='__main__': main()
