#!/usr/bin/env python3
"""TEST_ONLY: isolated LLL warm-seed benchmark, not production deployment.

Requires production fpylll=0.6.4 and gmpy2. Timings separate geometry/reduction;
not pipeline/GPU speed. Outputs coefficient box volumes: differing reduction
bases can increase enumeration work even when LLL itself is faster.
"""
import argparse
from dataclasses import asdict
import importlib.util
import json
from math import isqrt,prod
from pathlib import Path
import sys,time
from warm_reduction import WarmReducer,verify

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

def bounds(l,b):
    d=l.det3(b)
    inv=[[(b[(j+1)%3][(i+1)%3]*b[(j+2)%3][(i+2)%3]-b[(j+1)%3][(i+2)%3]*b[(j+2)%3][(i+1)%3])/d for j in range(3)]for i in range(3)]
    if l.matmul(b,inv)!=[[int(i==j)for j in range(3)]for i in range(3)]:raise ValueError('bad inverse')
    def ceil_sqrt(x):
        n=isqrt(int(x.numerator//x.denominator));return n+int(n*n<x)
    return tuple(ceil_sqrt(3*sum(inv[i][j]**2 for i in range(3)))for j in range(3))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True,help='lattice5_snapshot.py')
    p.add_argument('--precision-policy',type=Path,required=True)
    p.add_argument('--patches',type=int,default=16)
    p.add_argument('--repeats',type=int,default=3)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if not 1<=a.patches<=256 or not 1<=a.repeats<=10:raise ValueError('bounded test only')
    import gmpy2,fpylll
    if gmpy2.__version__!='2.2.2' or fpylll.__version__!='0.6.4':raise ValueError('use pinned production versions')
    l=load(a.source,'warm_lattice');policy=load(a.precision_policy,'warm_policy')
    l.Q=gmpy2.mpq
    def root(n,k=5):
        if n<0:raise ValueError('negative radicand')
        return int(gmpy2.iroot(n,k)[0])
    l.iroot=root
    lo,hi=100000000001,200000000000;grid=(9*lo+79)//80
    reports=[]
    for first in (0,3750000000,7192000000):
        start=time.perf_counter();bases=[];bits=[]
        for offset in range(a.patches):
            index=first+4*offset
            left,right=l.Q(9*index,10*grid),l.Q(9*(index+4),10*grid)
            precision=policy.geometry_bits(l,lo,hi,left,right,42)
            bases.append(l.make_patch(lo,hi,left,right,42,precision).basis());bits.append(precision)
        geometry=time.perf_counter()-start
        for repeat in range(a.repeats):
            for mode in (('cold','warm')if repeat%2==0 else ('warm','cold')):
                r=WarmReducer(l)
                start=time.perf_counter();reductions=[]
                for basis in bases:
                    b,u=r(basis)if mode=='warm' else r.cold(basis)
                    reductions.append((b,u))
                elapsed=time.perf_counter()-start
                volumes=[]
                for basis,(b,u)in zip(bases,reductions):
                    verify(l,basis,b,u);j=bounds(l,b);volumes.append(prod(2*x+1 for x in j))
                reports.append(dict(first=first,repeat=repeat,mode=mode,patches=len(bases),geometry_seconds=geometry,reduction_seconds=elapsed,coefficient_points=sum(volumes),max_coefficient_points=max(volumes),precision_bits=bits,stats=asdict(r.stats)))
    report=dict(status='passed_exact_transform_and_inverse_checks',scope='LLL microbenchmark only; no native enumeration/GPU/pipeline result',versions=dict(gmpy2=gmpy2.__version__,fpylll=fpylll.__version__),records=reports)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x')as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
