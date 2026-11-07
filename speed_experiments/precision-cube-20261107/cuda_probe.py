#!/usr/bin/env python3
"""Optional bounded Cabbage/Boole GPU check. Not executed in the cloud package."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'cube'))
import validate_cube as v

def main():
    if sys.flags.optimize:raise RuntimeError('Use ordinary Python, not -O')
    p=argparse.ArgumentParser();p.add_argument('--binary',required=True);p.add_argument('--output',default='cuda_probe_results.json');args=p.parse_args()
    binary=str(Path(args.binary).resolve())
    if not Path(binary).is_file():raise RuntimeError('CUDA binary does not exist')
    if os.environ.get('CUDA_VISIBLE_DEVICES') not in ('0',None):raise RuntimeError('Select GPU0 only for this bounded probe')
    busy=subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],capture_output=True,text=True,check=True,timeout=10)
    if busy.stdout.strip():raise RuntimeError('GPU has an active compute process; do not disturb it')
    os.environ['CUDA_VISIBLE_DEVICES']='0';started=time.monotonic();rows=[]
    for bound,mode,cap in [(34,'constant',384),(100,'constant',2951),(1000,'constant',42),(1000,'healy',0)]:
        patches,small=v.prepare(bound,mode,cap);expected=v.direct(bound,mode,cap)
        fallback={h for h in expected if any(lo<=h[2]<=hi for lo,hi in small)}
        for kind in ('sphere','cube'):
            cpu,cr=v.execute(patches,mode,cap,kind)
            gpu,gr=v.execute(patches,mode,cap,kind,binary)
            assert gr.get('backend')=='gpu' and cr.get('backend')=='emulated'
            assert gpu==cpu and gpu|fallback==expected
            rows.append(dict(bound=bound,mode=mode,kind=kind,points=gr['points_visited'],hits=sorted(gpu|fallback),gpu_engine_seconds=gr['engine_seconds'],cpu_engine_seconds=cr['engine_seconds']))
        if time.monotonic()-started>300:raise RuntimeError('Bounded GPU probe wall-time guard exceeded')
    report=dict(status='passed',scope='complete small positive domains only; this is correctness, not production throughput',elapsed_seconds=time.monotonic()-started,binary=binary,cases=rows)
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print('PASS',args.output)

if __name__=='__main__':main()
