#!/usr/bin/env python3
"""Bounded, reproducible 100–200 billion precision experiment. No service edits."""
import argparse,hashlib,itertools,json,math,platform,statistics,time,sys
from pathlib import Path
import reference_geometry as reference
from precision_policy import geometry_bits

def inverse(l,a):
    d=l.det3(a)
    r=[[(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3])/d for j in range(3)] for i in range(3)]
    assert l.matmul(a,r)==[[int(i==j) for j in range(3)] for i in range(3)]
    return r

def old_bounds(l,b):
    v=inverse(l,b);bounds=[]
    for j in range(3):
        s=3*sum(v[i][j]**2 for i in range(3));root=math.isqrt(int(s.numerator//s.denominator))
        bounds.append(root+int(root*root<s))
    return bounds

def prepare(l,lo,hi,left,right,cap,bits):
    start=time.perf_counter();p=l.make_patch(lo,hi,left,right,cap,bits)
    a=p.basis();g=time.perf_counter()
    b,u=l.reduce_basis(a,'fpylll') if hasattr(l,'reduce_basis') else l.lll(a)
    r=time.perf_counter();j=old_bounds(l,b)
    assert abs(l.det3(u))==1 and l.matmul(u,a)==b
    end=time.perf_counter()
    return p,u,j,dict(geometry_seconds=g-start,reduction_seconds=r-g,bounds_seconds=end-r,total_seconds=end-start)

def enumerate_hits(p,u,j,max_points=2000000):
    points=math.prod(2*x+1 for x in j)
    if points>max_points:raise RuntimeError(f'Probe point guard: {points}>{max_points}')
    hits=set();tested=0;start=time.perf_counter()
    for ns in itertools.product(*(range(-x,x+1) for x in j)):
        c,a,b=[sum(ns[k]*u[k][col] for k in range(3)) for col in range(3)]
        if not (1<=a<=b<c and p.contains(a,b,c)):continue
        tested+=1;r=a**5+b**5-c**5
        if abs(r)<=p.residual_cap:hits.add((int(a),int(b),int(c),int(r)))
    return sorted(hits),dict(box_points=points,exact_tests=tested,enumeration_seconds=time.perf_counter()-start)

def local_oracle(a,c,cap):
    hits=set()
    for cc in range(c-2,c+3):
      for aa in range(a-2,a+3):
        lower=max(aa,reference.iroot(max(0,cc**5-aa**5-cap)))
        upper=min(cc-1,reference.iroot(max(0,cc**5-aa**5+cap)))
        if upper-lower>10:raise RuntimeError('Local oracle candidate guard')
        for b in range(lower,upper+1):
            r=aa**5+b**5-cc**5
            if abs(r)<=cap:hits.add((aa,b,cc,r))
    return hits

def main():
    if sys.flags.optimize:raise RuntimeError('Exact validation requires ordinary Python, not -O')
    ap=argparse.ArgumentParser();ap.add_argument('--repeats',type=int,default=3)
    ap.add_argument('--output',default='precision_results.json')
    ap.add_argument('--ada-source',help='Optional pinned lattice_prototype path; needs ADA gmpy2/fpylll environment and sibling lattice_gpu/scaling_core.py')
    args=ap.parse_args();l=reference;engine='cloud stdlib Fraction + exact Python LLL'
    if args.ada_source:
        source=Path(args.ada_source).resolve();sys.path.insert(0,str(source.parent/'lattice_gpu'))
        import scaling_core
        scaling_core.initialize(source);l=scaling_core.lattice();engine='ADA pinned mpq + fpylll (caller-selected machine)'
    lo,hi,width=100000000001,200000000000,8;count=(9*lo+10*width-1)//(10*width)
    cases=[dict(name=f'ratio-index-{i}',index=i,cap=42,known=None) for i in [3750000000,3902545280,6250000000,10625000000]]
    for name,a,b,c,k in [('healy-scaled-5',21137517920,21483066250,24482314857,5),('healy-scaled-4000',13852184,27401825,27580409,4000)]:
        a,b,c=a*k,b*k,c*k;r=a**5+b**5-c**5
        i=a*10*count//(c*9)
        cases.append(dict(name=name,index=i,cap=abs(r),known=(a,b,c,r)))
    results=[]
    for case in cases:
        i=case['index'];left,right=l.Q(9*i,10*count),l.Q(9*(i+1),10*count)
        adaptive=geometry_bits(l,lo,hi,left,right,case['cap']);baseline=max(48,5*hi.bit_length()+32)
        entries={};timings={bits:[] for bits in (baseline,adaptive)}
        for repeat in range(args.repeats):
          for bits in ((baseline,adaptive) if repeat%2==0 else (adaptive,baseline)):
            p,u,j,t=prepare(l,lo,hi,left,right,case['cap'],bits);timings[bits].append(t)
            if bits not in entries:
                hits,stats=enumerate_hits(p,u,j)
                entries[bits]=dict(bits=bits,J=list(map(int,j)),U=[[int(x) for x in rr] for rr in u],hits=hits,stats=stats,eps=float(p.eps))
                if case['known'] is not None:
                    assert tuple(case['known']) in hits
                    expected=local_oracle(case['known'][0],case['known'][2],case['cap'])
                    expected={h for h in expected if p.contains(*h[:3])}
                    assert expected and expected.issubset(set(hits))
        assert entries[baseline]['hits']==entries[adaptive]['hits']
        medians={bits:statistics.median(x['total_seconds'] for x in rows) for bits,rows in timings.items()}
        row=dict(case=case,ratio=float((left+right)/2),baseline=entries[baseline],adaptive=entries[adaptive],timings=timings,median_prepare_seconds=medians,prepare_speed_ratio=medians[baseline]/medians[adaptive],validation='exact lattice certificates; complete coefficient boxes; baseline/adaptive exact hit equality; known controls and 5x5 direct local oracle when nonempty')
        results.append(row);print(json.dumps(dict(name=case['name'],bits=[baseline,adaptive],points=[entries[baseline]['stats']['box_points'],entries[adaptive]['stats']['box_points']],hits=len(entries[adaptive]['hits']),median_prepare_seconds=medians,speed_ratio=row['prepare_speed_ratio'])),flush=True)
    report=dict(status='passed',engine=engine,python=platform.python_version(),shell=[lo,hi],width=width,grid_count=count,repeats=args.repeats,source_commit='9a1ccf86eb8c8adae2e00e3cecbbb358345a0a45',limitations=['Selected patches only, not full-shell coverage or a new mathematical exclusion.','Timings exclude interprocess transport, serialization, GPU work, and persistent coordinator.','The default runtime uses Python Fraction/LLL, not ADA mpq/fpylll.','Both implementations share patch mathematics; local controls are independently searched, not an independent whole-shell oracle.'],results=results)
    report['source_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
