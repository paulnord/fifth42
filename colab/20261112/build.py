"""Build on the destination host; records actual compilers and GPU architecture."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent
def main(gpu):
    (ROOT/'bin').mkdir(exist_ok=True);(ROOT/'results').mkdir(exist_ok=True)
    cxx=shutil.which('g++')
    if not cxx:raise RuntimeError('A C++ compiler is required')
    commands=[[cxx,'-std=c++17','-O3',str(ROOT/'native/src/scaling_cpu.cpp'),'-pthread','-o',str(ROOT/'bin/scaling_cpu')],
              [cxx,'-std=c++17','-O3',str(ROOT/'native/independent/gmp_reference.cpp'),'-lgmpxx','-lgmp','-o',str(ROOT/'bin/gmp_reference')]]
    if gpu:
        nvcc=shutil.which('nvcc')
        if not nvcc:raise RuntimeError('CUDA toolkit is required; choose a Colab GPU runtime')
        commands.append([nvcc,'-std=c++17','-O3','-arch=native',str(ROOT/'native/src/scaling_gpu.cu'),'-o',str(ROOT/'bin/scaling_gpu')])
    for command in commands:subprocess.run(command,check=True,timeout=60)
    report=dict(status='passed',commands=commands,compiler=subprocess.check_output([cxx,'--version'],text=True),
        binaries={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'bin').iterdir() if p.is_file()})
    (ROOT/'results/build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--gpu',action='store_true');main(p.parse_args().gpu)
