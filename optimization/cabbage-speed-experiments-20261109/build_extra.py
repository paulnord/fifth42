import hashlib,json,os,shutil,subprocess
from pathlib import Path
r=Path(__file__).resolve().parent;out=r/'source/lattice_gpu/bin';out.mkdir(exist_ok=True)
os.sched_setaffinity(0,set(sorted(os.sched_getaffinity(0))[:4]));os.nice(10)
commands=[
 ['g++-13','-std=c++17','-O3','-Wall','-Wextra','-Werror',str(r/'native_audit.cpp'),'-o',str(r/'bin/audit')],
 ['g++-13','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(r/'native_audit.cpp'),'-o',str(r/'bin/audit_ubsan')],
 ['g++-13','-std=c++17','-O3','-Wall','-Wextra','-Werror','-pthread',str(r/'source/lattice_gpu/src/scaling_cpu.cpp'),'-o',str(out/'scaling_cpu')],
 ['g++-13','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-pthread',str(r/'source/lattice_gpu/src/scaling_cpu.cpp'),'-o',str(out/'scaling_cpu_sanitize')],
 ['g++-13','-std=c++17','-O3','-Wall','-Wextra','-Werror',str(r/'independent/gmp_reference.cpp'),'-lgmpxx','-lgmp','-o',str(r/'bin/gmp_reference-rebuilt')],
 ['/home/pnord/scratch/saved-root-pAjTHBhR/cuda-13.2/nvidia/cu13/bin/nvcc','-std=c++17','-O3','-arch=sm_86','-ccbin','g++-13',str(r/'source/lattice_gpu/src/scaling_gpu.cu'),'-o',str(r/'bin/scaling_gpu-rebuilt')]]
commands=[[os.environ.get('CXX','g++-13') if x=='g++-13' else os.environ.get('NVCC',x) if x.endswith('/nvcc') else '-arch='+os.environ.get('CUDA_ARCH','sm_86') if x=='-arch=sm_86' else x for x in command] for command in commands]
rows=[]
for command in commands:
 p=subprocess.run(command,capture_output=True,text=True);rows.append(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
 (r/'build-extra-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 if p.returncode:raise RuntimeError(rows[-1])
 print(Path(command[-1]).name,'built',flush=True)
