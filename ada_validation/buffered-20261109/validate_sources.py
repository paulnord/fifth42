import importlib.util,json,os
from pathlib import Path
import subprocess,time
ROOT=Path(__file__).resolve().parent

def helper():
    path=Path('/home/pnord/fifth42-low64-review-20261106/handoff/bundle/fifth42-coordinator-20261105/lattice_gpu/benchmark.py')
    spec=importlib.util.spec_from_file_location('existing_ada_resources',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def main():
    guard=helper();resources=guard.resources();assert not guard.hardware_blockers();handles,leased=guard.acquire_leases(resources,False)
    try:
        guard.idle_gpu();start=time.monotonic()
        cases=[]
        for name,command,cwd in [
          ('buffering',[str(ROOT/'test_buffering.py')],ROOT),
          ('scheduling',[str(ROOT/'test_scheduling.py')],ROOT),
          ('coordinator',['-m','unittest','discover','-s','tests','-v'],ROOT/'worker/source/lattice_gpu')]:
            with (ROOT/(name+'-tests.log')).open('x') as log:
                done=subprocess.run(['/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python','-B',*command],cwd=cwd,stdout=log,stderr=subprocess.STDOUT,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',SCALING_LATTICE_SOURCE=str(ROOT/'worker/source/lattice_prototype'),PYTHONPATH=str(ROOT/'worker')+':'+str(ROOT/'worker/source/lattice_gpu'),CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'))
            cases.append(dict(name=name,exit_code=done.returncode));print(json.dumps(cases[-1]),flush=True)
            if done.returncode:raise RuntimeError('Actual release validation failed: '+name)
        report=dict(status='passed',cases=cases,seconds=time.monotonic()-start,actual_gpu=True,independent_gmp=True,manifest_sha256=json.loads((ROOT/'worker/config.json').read_bytes())['manifest_sha256'])
        (ROOT/'unit-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return 0
    finally:
        for handle in handles:handle.close()
if __name__=='__main__':raise SystemExit(main())
