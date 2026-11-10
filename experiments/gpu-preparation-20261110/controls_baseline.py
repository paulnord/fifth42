"""Exact nonempty finite grouped control, independent GMP and brute-force."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import adapter_runtime as adapter
import buffered_pipeline as b
import coordinator_pipeline as pipeline
import scaling_core as core
import runtime_initialize
from fractions import Fraction
GROUPS=(4,8,16)
class Serial:
 def map(self,fn,args,chunksize):return list(map(fn,args))
def check_spans(chunk):
 cursor=chunk.window.first
 for first,last in chunk.window.spans:
  assert first==cursor and first<last<=chunk.window.last
  cursor=last
 assert cursor==chunk.window.last
parser=argparse.ArgumentParser();parser.add_argument('--backend',choices=('gpu','emulated'),default='gpu');args=parser.parse_args()
runtime_initialize.initialize(W/'source/lattice_prototype')
controls=[]
engine=adapter.open_session(W/'bin/scaling_gpu',args.backend,time.monotonic()+90)
try:
 lo,hi,cap=136,153,708588;last=16
 powers=[x**5 for x in range(hi+1)]
 expected={(a,bb,c,powers[a]+powers[bb]-powers[c]) for c in range(lo,hi+1) for bb in range(1,c) for a in range(1,bb+1) if abs(powers[a]+powers[bb]-powers[c])<=cap}
 assert (117,144,153,708588) in expected
 for group in GROUPS:
     chunk=b.prepare_cached(Serial(),pipeline.Window(lo,hi,0,last,8,222,cap,'adaptive'),group)
     check_spans(chunk);b.validate_cached(chunk);hits=set()
     for batch in chunk.plan.batches:
         raw,_=engine.run(batch.packet,timeout=15);pipeline.validate_response_types(raw)
         decoded=core.decode_batch(batch,raw,args.backend);hits.update(decoded)
         done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=15)
         reference=json.loads(done.stdout);pipeline.validate_response_types(reference)
         assert adapter.normalized_counts(batch,raw)==adapter.normalized_counts(batch,reference)
         assert adapter.normalized_hits(batch,raw)==adapter.normalized_hits(batch,reference)
         assert decoded==core.decode_batch(batch,reference,'emulated')
     assert hits==expected,(group,hits,expected)
     controls.append(dict(requested_group=group,nonempty_candidates=sorted(hits),logical_spans=chunk.window.spans,points=chunk.plan.points,full_oracle_equal=True))
finally:engine.close()
print(json.dumps(controls,indent=2))
