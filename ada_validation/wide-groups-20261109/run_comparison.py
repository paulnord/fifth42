"""Finite TEST_ONLY group 4/8/16 comparison; no production restart or writes."""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction
import hashlib,json,os,signal,statistics,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent; W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import adapter_runtime as adapter
import buffered_pipeline as b
import coordinator_pipeline as pipeline
import runtime_initialize
import scaling_core as core
from resource_helper import helper
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
GROUPS=(4,8,16)
REGIONS=(('ada',4564955776),('cabbage',2572492928),('dense',9562500096))
BUDGET=180

def write(name,row):
    p=ROOT/name;t=p.with_name(p.name+'.tmp')
    t.write_text(json.dumps(row,indent=2)+'\n');os.replace(t,p)

class Serial:
    def map(self,fn,args,chunksize):return list(map(fn,args))

def check_spans(chunk):
    window=chunk.window;cursor=window.first;count=(9*window.lo+79)//80
    for span,spec in zip(window.spans,window.explicit_specs):
        first,last=span
        assert first==cursor and first<last<=window.last
        assert Fraction(*spec[3])==Fraction(9*first,10*count)
        assert Fraction(*spec[4])==Fraction(9*last,10*count)
        cursor=last
    assert cursor==window.last

def main():
    start=time.monotonic();guard=helper();handles=[];engine=None
    production=Path('/home/pnord/ada-group4-20261109/worker')
    before={n:hashlib.sha256((production/n).read_bytes()).hexdigest() for n in ['config.json','release-manifest.json','width_coverage.py','buffered_pipeline.py']}
    parent_cfg=json.loads((production/'config.json').read_bytes())
    parent_cp=(Path(parent_cfg['output'])/'checkpoint.json').read_bytes()
    assert json.loads((Path(parent_cfg['output'])/'status.json').read_bytes())['status']=='stopped'
    out=Path('/home/pnord/fifth42-local-benchmarks/TEST_ONLY_ada_wide_groups_20261109')
    out.mkdir(mode=0o700,parents=True,exist_ok=False)
    logs=ROOT/'logs';logs.mkdir(mode=0o700)
    rows=[];preflight=[];controls=[]
    manifest=json.loads((ROOT/'experiment-manifest.json').read_bytes())
    def verify_sources():
        for name,h in manifest['worker_files'].items():assert hashlib.sha256((W/name).read_bytes()).hexdigest()==h,name
    try:
        verify_sources();assert not guard.hardware_blockers()
        handles,leased=guard.acquire_leases(guard.resources(),False);guard.idle_gpu()
        os.nice(19);os.sched_setaffinity(0,set(range(16)))
        runtime_initialize.initialize(W/'source/lattice_prototype')
        write('progress.json',dict(status='preflight',budget_seconds=BUDGET,TEST_ONLY=True,production_restarted=False))
        # Exact certificates and original fine-grid edge checks before GPU work.
        for region,first in REGIONS:
            for group in GROUPS:
                chunk=b.prepare_cached(Serial(),pipeline.Window(100000000001,200000000000,first,first+256,8,222,42,'adaptive'),group)
                b.validate_cached(chunk);check_spans(chunk)
                preflight.append(dict(region=region,requested_group=group,physical_tasks=chunk.plan.tasks,points=chunk.plan.points,batches=len(chunk.plan.batches),actual_span_histogram=dict(Counter(z-a for a,z in chunk.window.spans))))
        write('preflight.json',dict(status='passed',source_manifest_sha256=hashlib.sha256((ROOT/'experiment-manifest.json').read_bytes()).hexdigest(),cases=preflight,guards_unchanged=True))
        print(json.dumps(dict(stage='preflight',status='passed',cases=preflight)),flush=True)
        engine=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+60)
        lo,hi,cap=136,153,708588;last=16
        powers=[x**5 for x in range(hi+1)]
        expected={(a,bb,c,powers[a]+powers[bb]-powers[c]) for c in range(lo,hi+1) for bb in range(1,c) for a in range(1,bb+1) if abs(powers[a]+powers[bb]-powers[c])<=cap}
        assert (117,144,153,708588) in expected
        for group in GROUPS:
            chunk=b.prepare_cached(Serial(),pipeline.Window(lo,hi,0,last,8,222,cap,'adaptive'),group)
            check_spans(chunk);b.validate_cached(chunk);hits=set()
            for batch in chunk.plan.batches:
                raw,_=engine.run(batch.packet,timeout=15);pipeline.validate_response_types(raw)
                decoded=core.decode_batch(batch,raw,'gpu');hits.update(decoded)
                done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=15)
                reference=json.loads(done.stdout);pipeline.validate_response_types(reference)
                assert adapter.normalized_counts(batch,raw)==adapter.normalized_counts(batch,reference)
                assert adapter.normalized_hits(batch,raw)==adapter.normalized_hits(batch,reference)
                assert decoded==core.decode_batch(batch,reference,'emulated')
            assert hits==expected,(group,hits,expected)
            controls.append(dict(requested_group=group,nonempty_candidates=sorted(hits),logical_spans=chunk.window.spans,points=chunk.plan.points,full_oracle_equal=True))
        engine.close();engine=None
        write('controls.json',dict(status='passed',actual_gpu=True,independent_gmp=True,exhaustive_brute=True,cases=controls))
        print(json.dumps(dict(stage='nonempty_controls',status='passed',hits=len(expected))),flush=True)
        fingerprints={};candidates={}
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',SCALING_LATTICE_SOURCE=str(W/'source/lattice_prototype'),PYTHONPATH=str(W)+':'+str(W/'source/lattice_gpu'))
        for repeat in range(3):
            for region,first in REGIONS:
                order=GROUPS[repeat:]+GROUPS[:repeat]
                if repeat%2:order=tuple(reversed(order))
                for group in order:
                    remaining=BUDGET-(time.monotonic()-start)
                    if remaining<10:raise TimeoutError('Finite comparison budget exhausted')
                    name=f'{region}-g{group}-r{repeat}';folder=out/name;dispatch=max(1,16//group)
                    command=[PYTHON,'-B',str(ROOT/'trial_wide_groups.py'),'--variant','cache_buffer8','--workers','16','--first',str(first),'--patches','32768','--group-limit',str(group),'--map-chunksize',str(dispatch),'--prep-windows','1','--output',str(folder)]
                    guard.idle_gpu()
                    with (logs/(name+'.stdout.log')).open('x') as log,(logs/(name+'.stderr.log')).open('x') as error:
                        process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=error,start_new_session=True)
                        try:code=process.wait(timeout=min(45,remaining-3))
                        except BaseException:
                            os.killpg(process.pid,signal.SIGTERM)
                            try:process.wait(timeout=2)
                            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=2)
                            raise
                    assert code==0,'Trial failed: '+name
                    row=json.loads((folder/'result.json').read_bytes())
                    assert row['status']=='passed' and row['first']==first and row['patches']==32768 and row['recovery_passed']
                    key=(region,group);fp=(row['signatures_sha256'],row['points'],row['physical_tasks'],row['hits'])
                    if key in fingerprints:assert fingerprints[key]==fp
                    else:fingerprints[key]=fp
                    if region in candidates:assert candidates[region]==row['hits'],'Candidate sets changed'
                    else:candidates[region]=row['hits']
                    row.update(region=region,repeat=repeat,command=command,output=str(folder));rows.append(row)
                    write('progress.json',dict(status='running',completed=len(rows),planned=27,elapsed_seconds=time.monotonic()-start,last={k:row[k] for k in ['region','group_limit','steady_seconds','patches_per_second']}))
                    print(json.dumps({k:row[k] for k in ['region','repeat','group_limit','steady_seconds','patches_per_second','physical_tasks','points']}),flush=True)
        summary=[]
        for region,first in REGIONS:
            times={str(g):statistics.median(row['steady_seconds'] for row in rows if row['region']==region and row['group_limit']==g) for g in GROUPS}
            summary.append(dict(region=region,first=first,cells=32768,median_seconds=times,cells_per_second={g:32768/t for g,t in times.items()},throughput_vs_group4={g:times['4']/t for g,t in times.items()}))
        verify_sources()
        assert before=={n:hashlib.sha256((production/n).read_bytes()).hexdigest() for n in before}
        assert parent_cp==(Path(parent_cfg['output'])/'checkpoint.json').read_bytes()
        report=dict(status='passed',TEST_ONLY=True,production_coverage=False,production_restarted=False,production_unchanged=True,budget_seconds=BUDGET,total_seconds=time.monotonic()-start,repeats=3,identical_candidate_sets=True,exact_original_cell_coverage=True,unmodified_native_guards=True,independent_gmp_and_recovery_every_trial=True,summary=summary,trials=rows,preflight=preflight,controls=controls,baseline_manifest_sha256=manifest['baseline_manifest_sha256'])
        write('results.json',report);write('progress.json',dict(status='passed',completed=27,planned=27,elapsed_seconds=report['total_seconds'],summary=summary))
        print(json.dumps(dict(status='passed',total_seconds=report['total_seconds'],summary=summary),indent=2),flush=True)
    except BaseException as exc:
        write('failure.json',dict(status='failed',error=f'{type(exc).__name__}: {exc}',completed=len(rows),seconds=time.monotonic()-start,production_restarted=False))
        raise
    finally:
        if engine:engine.close()
        for handle in handles:handle.close()

if __name__=='__main__':main()
