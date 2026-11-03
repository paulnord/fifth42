#!/usr/bin/env python3
"""Compare exact kernel variants on bounded samples after baseline completion.

Default: B=1,000,000, 65,536 z rows in each of three regions, at most 30 s
total. This is a benchmark, not a claim of full-box coverage. It requires
passing optimized GPU validation. No long job or automatic continuation.
"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import signal
import subprocess
import sys
import time

from check_idle import ensure_idle
from reference import verify
from run import atomic_json,fingerprint,sha

ROOT=Path(__file__).resolve().parent

def run_command(args,timeout):
    p=subprocess.Popen(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:out,err=p.communicate(timeout=timeout)
    except BaseException:
        import os
        os.killpg(p.pid,signal.SIGKILL);p.communicate();raise
    if p.returncode:raise RuntimeError(err.strip())
    return json.loads(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-seconds',type=float,default=30)
    ap.add_argument('--output',type=Path,default=ROOT/'runs/gpu-comparison.json')
    args=ap.parse_args()
    if not 0<args.max_seconds<=30:raise ValueError('This modest benchmark is capped at 30 seconds')
    ensure_idle()
    for name in ('validation.json','optimized-validation.json'):
        r=json.loads((ROOT/'runs'/name).read_text())
        if r.get('gpu_status')!='passed' or r.get('gpu_fingerprint')!=fingerprint('gpu'):
            raise RuntimeError('Run make test-gpu in this optimization directory first')
    manifest=json.loads((ROOT/'docs/baseline-manifest.json').read_text())
    if sha(ROOT/'bin/reference_gpu')!=manifest['baseline_gpu_binary_sha256']:
        raise ValueError('Frozen original GPU binary does not match baseline manifest')
    for name,digest in manifest.get('baseline_sources',{}).items():
        if sha(ROOT.parent/name)!=digest:raise ValueError('Production baseline source changed; rebuild references and revalidate')
    bound=1_000_000
    total=2*(bound//11)+1
    count=65536
    regions=[('negative_edge',0,count),('middle',(total-count)//2,(total+count)//2),('positive_edge',total-count,total)]
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'bound':bound,
            'fingerprint':fingerprint('gpu'),'samples':[],
            'coverage_note':'Overlapping sample row ranges; not a complete box search.',
            'max_seconds':args.max_seconds,'complete':False}
    deadline=time.monotonic()+args.max_seconds
    try:
        for label,start,stop in regions:
            expected=None
            for variant,block in [('reference',128),('cached',128),('pruned',128),('highword',128)]:
                remaining=deadline-time.monotonic()
                if remaining<0.1:raise subprocess.TimeoutExpired('benchmark budget',args.max_seconds)
                cmd=[str(ROOT/'bin'/('reference_gpu' if variant=='reference' else 'search_gpu')),
                     '--bound',str(bound),'--row-start',str(start),'--row-stop',str(stop)]
                if variant!='reference':cmd.extend(['--variant',variant,'--block-size',str(block)])
                begin=time.monotonic()
                r=run_command(cmd,remaining)
                for h in r['hits']:verify(h,bound,42)
                if expected is None:expected=r['hits']
                elif r['hits']!=expected:raise ValueError(f'Candidate mismatch: {label}, {variant}')
                report['samples'].append({'region':label,'variant':variant,'block_size':block,
                    'wall_seconds':time.monotonic()-begin,'result':r})
                atomic_json(args.output,report)
        report['complete']=True
    except subprocess.TimeoutExpired:
        report['stopped_reason']='30-second benchmark budget reached; no automatic continuation.'
    finally:
        atomic_json(args.output,report)
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError,subprocess.SubprocessError) as e:
        print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
