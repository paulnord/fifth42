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
        with (ROOT/'validation.log').open('a') as log:
            done=subprocess.run(['/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python','-B',str(ROOT/'test_buffering.py')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'))
        report=dict(status='passed' if done.returncode==0 else 'failed',exit_code=done.returncode,seconds=time.monotonic()-start,actual_gpu=True,independent_gmp=True)
        (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return done.returncode
    finally:
        for handle in handles:handle.close()
if __name__=='__main__':raise SystemExit(main())
