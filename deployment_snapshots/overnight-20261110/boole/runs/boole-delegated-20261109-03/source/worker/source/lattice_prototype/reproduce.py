#!/usr/bin/env python3
"""Rebuild the bounded coverage records and explicitly selected large regressions."""
import argparse,json,pathlib,time
from fractions import Fraction as Q
import lattice5 as l
ROOT=pathlib.Path(__file__).resolve().parent
PUBLISHED=[(13,16,17),(26,32,34),(39,48,51),(52,64,68),(42,71,72),
           (104,133,140),(84,142,144),(133,228,231),(262,328,347),(494,954,961)]

def save(name,data):
    (ROOT/'results').mkdir(exist_ok=True)
    json.dump(data,open(ROOT/'results'/name,'w'),indent=2)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bound',type=int,choices=[100,1000],default=100)
    args=ap.parse_args();n=args.bound
    healy=l.search_positive(n,mode='healy')
    expected_published={(a,b,c,a**5+b**5-c**5) for a,b,c in PUBLISHED if c<=n}
    assert set(map(tuple,healy['hits']))==expected_published
    t=time.perf_counter()
    direct=l.direct_positive(1,n,lambda c:5*c*c,lambda r,c:abs(r)<=5*c*c)
    assert set(map(tuple,healy['hits']))==direct
    save(f'healy-{n}.json',healy)
    save(f'reference-healy-{n}.json',dict(bound=n,complete=True,match=True,hit_count=len(direct),hits=sorted(direct),seconds=time.perf_counter()-t,method='independent integer fifth-root (a,c) enumeration'))
    signed=l.signed42(n)
    assert set(map(tuple,signed['signed_hits']))==l.signed_reference(n,42)
    save(f'signed42-{n}.json',signed)
    print(f'Complete through {n}: {len(direct)} published near misses, exact reference agreement, no target42 solution.',flush=True)
    controls=[]
    for a,b,c in [(13852184,27401825,27580409),(21137517920,21483066250,24482314857)]:
        C=1<<(c.bit_length()-1);D=2*C-1
        count=l.ceil(Q(9*C,20));i=l.floor(Q(a,c)*10*count/9)
        patch=l.make_patch(C,D,Q(9*i,10*count),Q(9*(i+1),10*count),5*D*D,bits=160)
        stats=l.Stats();t=time.perf_counter()
        hits=l.patch_search(patch,lambda r,c:abs(r)<=5*c*c,stats,l.Budget(start=t,max_seconds=60))
        r=a**5+b**5-c**5;assert (a,b,c,r) in hits
        stats.seconds=time.perf_counter()-t
        controls.append(dict(triple=[a,b,c],residual=r,patch_index=i,total_shell_patches=count,cmin=C,cmax=D,hits=sorted(hits),stats=l.asdict(stats),coverage='one fixture-selected patch only; NOT the full shell',bits=160))
    save('focused-large-controls.json',controls)
    print('Both selected large regression patches passed. These are NOT complete large-range searches.')

if __name__=='__main__': main()
