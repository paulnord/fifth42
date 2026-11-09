import json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.sched_setaffinity(0,set(sorted(os.sched_getaffinity(0))[:4]));os.nice(10)
nvcc=os.environ.get('NVCC','/home/pnord/scratch/saved-root-pAjTHBhR/cuda-13.2/nvidia/cu13/bin/nvcc')
compiler=os.environ.get('CXX','g++-13');architecture=os.environ.get('CUDA_ARCH','sm_86')
rows=[]
for mode,name in enumerate(['baseline','low64','rows','wheel','differences','wheel_differences']):
    command=[nvcc,'-std=c++17','-O3',f'-arch={architecture}','-ccbin',compiler,f'-DEXPERIMENT={mode}',str(ROOT/'fast_gpu.cu'),'-o',str(ROOT/'bin'/name)]
    start=time.monotonic();p=subprocess.run(command,capture_output=True,text=True)
    rows.append(dict(mode=mode,name=name,command=command,seconds=time.monotonic()-start,exit_code=p.returncode,output=p.stdout+p.stderr))
    (ROOT/'build-results.json').write_text(json.dumps(rows,indent=2)+'\n')
    if p.returncode:raise RuntimeError(rows[-1])
    print(name,'built',round(rows[-1]['seconds'],2),flush=True)
