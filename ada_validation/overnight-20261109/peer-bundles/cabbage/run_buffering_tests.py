"""Run the supplied suites unchanged against this worker under Cabbage's leases."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,time
import cabbage_test_guard
R=Path(__file__).resolve().parent;W=R/'worker'
sys.path.insert(0,str(W));sys.path.insert(0,str(W/'source/lattice_gpu'))
os.environ['SCALING_LATTICE_SOURCE']=str(W/'source/lattice_prototype')
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
os.environ['PYTHONPATH']=os.pathsep.join([str(W),str(W/'source/lattice_gpu')])
guard=cabbage_test_guard.helper();assert not guard.hardware_blockers()
handles,errors=guard.acquire_leases(guard.resources(),False);assert not errors
try:
 started=time.monotonic();cases=[]
 for name in ['test_buffering.py','test_scheduling.py']:
  done=subprocess.run([sys.executable,'-B',str(R/name)],cwd=R,capture_output=True,text=True,timeout=240)
  log=done.stdout+done.stderr;(R/'evidence'/(name+'.log')).write_text(log);print(log,flush=True)
  match=re.search(r'Ran (\d+) tests?',log)
  cases.append(dict(suite=name,status='passed' if done.returncode==0 else 'failed',tests=int(match[1]) if match else 0))
 passed=all(c['status']=='passed' and c['tests']>0 for c in cases)
 evidence=dict(status='passed' if passed else 'failed',tests=sum(c['tests'] for c in cases),cases=cases,seconds=time.monotonic()-started,
  supplied_tests_unchanged=True,actual_worker=str(W),original_owner_and_gpu_leases=True,
  files_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'test_buffering.py',R/'test_scheduling.py',W/'buffered_pipeline.py',W/'scheduling.py',W/'packed_worker.py']})
 (R/'evidence/buffering-validation.json').write_text(json.dumps(evidence,indent=2)+'\n')
 raise SystemExit(0 if passed else 1)
finally:
 for handle in handles:handle.close()
