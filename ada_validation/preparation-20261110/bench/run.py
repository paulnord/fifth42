"""Matched finite CPU batching comparison under Ada's actual resource leases."""
import hashlib,importlib.util,json,os,statistics,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parent;W=R/'worker'
sys.path.insert(0,str(W));import policy,transition_resources
def read(p):return json.loads(Path(p).read_bytes())
def main():
 c=read(W/'config.json');policy.verify_sources(c)
 path='/home/pnord/fifth42-low64-review-20261106/handoff/bundle/fifth42-coordinator-20261105/lattice_gpu/benchmark.py'
 spec=importlib.util.spec_from_file_location('owned_benchmark',path);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 assert not helper.hardware_blockers();handles,leased=transition_resources.acquire(helper,helper.resources(),c)
 rows=[]
 try:
  for rep in range(3):
   for size in ((1,16) if rep%2==0 else (16,1)):
    folder=B/('cpu-w%d-r%d'%(size,rep));cmd=[sys.executable,'-B',str(B/'trial_preparation.py'),'--variant','cache_buffer8','--workers','16','--first',str(c['initial_patch']),'--patches','32768','--group-limit','4','--map-chunksize','4','--preparation-backend','cpu','--window-batch',str(size),'--output',str(folder)]
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=45,env=env);(B/(folder.name+'.log')).write_text(p.stdout+p.stderr);p.check_returncode();row=read(folder/'result.json');row.update(repeat=rep);rows.append(row);print(folder.name,round(row['patches_per_second']),flush=True)
  assert len({(x['signatures_sha256'],x['points'],x['physical_tasks'],str(x['hits'])) for x in rows})==1
  rates={s:statistics.median(x['patches_per_second'] for x in rows if x['preparation_window_batch']==s) for s in (1,16)}
  summary=dict(status='passed',TEST_ONLY=True,production_coverage=False,source_manifest_sha256=c['manifest_sha256'],identical_candidate_signatures_counts_hits=True,baseline_cells_per_second=rates[1],batched_cells_per_second=rates[16],batched_improvement_percent=100*(rates[16]/rates[1]-1),selected_windows=16 if rates[16]>rates[1] else 1,samples=rows)
  (R/'benchmark-results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='samples'}),flush=True)
 finally:
  for h in handles:h.close()
if __name__=='__main__':main()
