#!/usr/bin/env python3
"""Bounded timing of the validated 192-bit GPU code; never launches a long job."""
import argparse
import json
from pathlib import Path
import time
import subprocess
import sys
import run
from check_idle import ensure_idle
ROOT=Path(__file__).resolve().parent

def main():
    ensure_idle();run.gpu_gate()
    output=ROOT/'runs/calibration.json'
    bound=10_000_000;count=65536;total=run.rows(bound,'mod11')
    r={'arithmetic_bits':192,'bound':bound,'fingerprint':run.fingerprint('gpu'),
       'samples':[],'complete':False,'max_seconds':30,'created_utc':run.now()}
    deadline=time.monotonic()+30
    regions=[('negative_edge',0,count),('middle',(total-count)//2,(total+count)//2),('positive_edge',total-count,total)]
    try:
        for label,start,stop in regions:
            remaining=deadline-time.monotonic()
            if remaining<=0:raise subprocess.TimeoutExpired('calibration',30)
            command=[str(ROOT/'bin/search_gpu'),'--bound',str(bound),'--row-start',str(start),'--row-stop',str(stop)]
            begin=time.monotonic();sample=run.execute_engine(command,remaining)
            run.validate_result(sample,{'backend':'gpu','bound':bound,'target':42,'filter':'mod11'},start,stop)
            r['samples'].append({'region':label,'wall_seconds':time.monotonic()-begin,'result':sample})
            run.atomic_json(output,r)
        r['complete']=True
        mean=sum(s['wall_seconds'] for s in r['samples'])/len(r['samples'])
        e=run.estimate(70_000_000,65536)
        r['rough_projected_70million_seconds']=mean*e['z_rows']/count*7
        r['uncertainty']='Three sample regions and quadratic scaling; larger memory footprint may slow further. Not a promised completion time.'
    except subprocess.TimeoutExpired:
        r['stopped_reason']='30-second timing budget exhausted; no automatic continuation.'
    finally:run.atomic_json(output,r)
    print(json.dumps(r,indent=2))
    if not r['complete']:sys.exit(2)
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:
        print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
