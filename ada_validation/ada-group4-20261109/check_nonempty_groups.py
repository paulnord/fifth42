"""Full four-cell grouped shell: identical nonempty GPU/GMP/brute candidate sets."""
import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import adapter_runtime as adapter
import buffered_pipeline as b
import coordinator_pipeline as pipeline
import runtime_initialize
import scaling_core as core
from validate_sources import helper
class Serial:
    def map(self,fn,args,chunksize): return list(map(fn,args))
def main():
    guard=helper();resources=guard.resources();assert not guard.hardware_blockers()
    handles,leased=guard.acquire_leases(resources,False);engine=None
    try:
        guard.idle_gpu();os.sched_setaffinity(0,set(range(16)))
        runtime_initialize.initialize(W/'source/lattice_prototype')
        engine=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+90)
        lo,hi,cap=32,63,2951
        expected={(a,bb,c,a**5+bb**5-c**5) for c in range(lo,hi+1) for bb in range(1,c) for a in range(1,bb+1) if abs(a**5+bb**5-c**5)<=cap}
        assert (39,48,51,2916) in expected
        results=[]
        for group in (2,4):
            window=pipeline.Window(lo,hi,0,4,8,222,cap,'adaptive')
            chunk=b.prepare_cached(Serial(),window,group);b.validate_cached(chunk)
            hits=set()
            for batch in chunk.plan.batches:
                raw,_=engine.run(batch.packet,timeout=20)
                gpu=core.decode_batch(batch,raw,'gpu')
                done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=20)
                ref=json.loads(done.stdout)
                assert adapter.normalized_counts(batch,raw)==adapter.normalized_counts(batch,ref)
                assert gpu==core.decode_batch(batch,ref,'emulated')
                hits.update(gpu)
            assert hits==expected, (group,hits,expected)
            assert chunk.window.spans[0][0]==0 and chunk.window.spans[-1][1]==4
            results.append(dict(group_limit=group,hits=sorted(hits),logical_spans=chunk.window.spans,points=chunk.plan.points))
        report=dict(status='passed',actual_gpu=True,independent_gmp=True,exhaustive_brute_equal=True,nonempty=True,full_four_cell_span=True,results=results)
        (ROOT/'gpu-validation.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
    finally:
        if engine: engine.close()
        for handle in handles: handle.close()
if __name__=='__main__':main()
