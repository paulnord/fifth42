"""Finite GPU/GMP comparisons in remaining unclaimed ranges; no production coverage."""
import fcntl,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
os.environ['SCALING_LATTICE_SOURCE']=str(W/'source/lattice_prototype')
import adapter_runtime as adapter,coordinator_pipeline as pipeline,runtime_initialize,width_coverage as coverage
from durable_mirror import atomic
class Serial:
 def map(self,fn,args,chunksize):return list(map(fn,args))
def main():
 os.nice(19);os.sched_setaffinity(0,{1});runtime_initialize.initialize(W/'source/lattice_prototype')
 with open('/home/pnord/boole-production-validation-20261107/gpu-owner.lock','a+') as lease:
  fcntl.lockf(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
  engine=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+180)
  rows=[]
  try:
   for first in (65536,100000000,250000000,499999744):
    start=time.monotonic();window=pipeline.Window(100000000001,200000000000,first,first+256,8,222,42,'adaptive')
    try:chunk=coverage.prepare_chunk(Serial(),window,4)
    except pipeline.GuardedPatch as error:
     row=dict(first=first,last=first+256,status='unsupported',error=str(error),TEST_ONLY=True,scientific_coverage=False)
     rows.append(row);print(json.dumps(row),flush=True);continue
    prepared=time.monotonic()
    record=coverage.add_coverage(pipeline.execute_chunk(chunk,pipeline.OwnedEngine(engine),trial='TEST_ONLY_overnight-ranges',coordinator=0),chunk,4)
    gpu_done=time.monotonic();audits=[]
    for batch,receipt in zip(chunk.plan.batches,record['batches']):
     result=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,capture_output=True,text=True,check=True,timeout=30)
     reference=json.loads(result.stdout)
     assert adapter.normalized_counts(batch,reference)==list(map(tuple,receipt['native_counts']))
     assert adapter.normalized_hits(batch,reference)==list(map(tuple,receipt['native_hit_records']))
     audits.append(reference)
    row=dict(first=first,last=first+256,status='passed',TEST_ONLY=True,scientific_coverage=False,points=record['points'],physical_tasks=len(record['patches']),prepare_serial_seconds=prepared-start,gpu_seconds=gpu_done-prepared,gmp_seconds=time.monotonic()-gpu_done,record=record,references=audits)
    rows.append(row);atomic(ROOT/'evidence/boole-validation/remaining-ranges.json',dict(status='in_progress',cases=rows))
    print(json.dumps({k:row[k] for k in ('first','status','points','prepare_serial_seconds','gpu_seconds','gmp_seconds')}),flush=True)
  finally:engine.close()
  atomic(ROOT/'evidence/boole-validation/remaining-ranges.json',dict(status='passed',cases=rows,TEST_ONLY=True,scientific_coverage=False))
if __name__=='__main__':main()
