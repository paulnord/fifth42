#!/usr/bin/env python3
"""Bounded cloud tests of cube J against frozen native CPU emulation.
No ADA/GPU execution; no production code or run checkpoint is changed.
"""
import bisect,itertools,json,platform,random,statistics,subprocess,sys,time,hashlib
from fractions import Fraction as Q
from math import prod
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reference'))
import lattice5 as L
from cube_bounds import *


def properties():
    identity=[[Q(i==j) for j in range(3)] for i in range(3)]
    assert coefficient_bounds_sphere(identity)==(2,2,2)
    assert coefficient_bounds_cube(identity)==(1,1,1)
    assert prod(2*j+1 for j in coefficient_bounds_cube(identity))==27
    assert all(all(abs(n)<=j for n,j in zip(corner,coefficient_bounds_cube(identity)))
               for corner in itertools.product((-1,1),repeat=3))
    rng=random.Random(721196)
    checked=0
    for _ in range(32):
        a=[[Q(rng.choice([1,2,3]),2),Q(rng.randint(-2,2),3),Q(rng.randint(-2,2),3)],
           [Q(0),Q(rng.choice([1,2,3]),2),Q(rng.randint(-2,2),3)],
           [Q(0),Q(0),Q(rng.choice([1,2,3]),2)]]
        b,u=L.lll(a);old=coefficient_bounds_sphere(b);new=coefficient_bounds_cube(b)
        assert all(n<=o for n,o in zip(new,old))
        assert L.matmul(u,a)==b and abs(L.det3(u))==1
        for ns in itertools.product(*(range(-j,j+1) for j in old)):
            physical=[sum(ns[k]*b[k][j] for k in range(3)) for j in range(3)]
            if all(abs(v)<=1 for v in physical):
                assert all(abs(n)<=j for n,j in zip(ns,new));checked+=1
        certify_cube_bounds(b,new)
        try:certify_cube_bounds(b,(new[0]+1,*new[1:]))
        except ValueError:pass
        else:raise AssertionError('Tampering must fail')
    for bad in ([[1,0],[0,1]],[[0]*3 for _ in range(3)]):
        try:coefficient_bounds_cube(bad)
        except ValueError:pass
        else:raise AssertionError('Invalid basis must fail')
    return dict(random_bases=32,cube_integer_points_preserved=checked,corners=8,tampering_rejected=True)


def direct(bound,mode,cap):
    # Independent sorted fifth-power table and bisect. No root, lattice, or modular code.
    powers=[x**5 for x in range(bound+1)];hits=set()
    for c in range(2,bound+1):
        limit=5*c*c if mode=='healy' else cap
        for a in range(1,c):
            center=powers[c]-powers[a]
            lo=max(a,bisect.bisect_left(powers,center-limit))
            hi=min(c,bisect.bisect_right(powers,center+limit))
            for b in range(lo,hi):hits.add((a,b,c,powers[a]+powers[b]-powers[c]))
    return hits


def prepare(bound,mode,cap,width=8):
    patches=[];small=[];lo=1
    while lo<=bound:
        hi=min(2*lo-1,bound);limit=5*hi*hi if mode=='healy' else cap
        if Q(limit,lo**5)>Q(9049,50000):small.append((lo,hi))
        else:
            count=(9*lo+10*width-1)//(10*width)
            for i in range(count):
                p=L.make_patch(lo,hi,Q(9*i,10*count),Q(9*(i+1),10*count),limit,48)
                b,u=L.lll(p.basis());patches.append((p,b,u))
        lo*=2
    return patches,small


def packet(patches,mode,cap,kind):
    bounds=coefficient_bounds_cube if kind=='cube' else coefficient_bounds_sphere
    rows=[f'LATTICE_GPU_V1 {int(mode=="healy")} {0 if mode=="healy" else cap} {len(patches)}'];points=[]
    for index,(p,b,u) in enumerate(patches):
        j=bounds(b);old=coefficient_bounds_sphere(b)
        assert all(n<=o for n,o in zip(j,old))
        assert abs(L.det3(u))==1 and L.matmul(u,p.basis())==b
        if kind=='cube':certify_cube_bounds(b,j)
        assert all(sum(j[i]*abs(u[i][col]) for i in range(3))<=2**63-1 for col in range(3))
        count=prod(2*x+1 for x in j);assert count<=10_000_000;points.append(count)
        row=[index,p.cmin,p.cmax,*j,*(x for r in u for x in r)];rows.append(' '.join(map(str,row)))
    assert sum(points)<=50_000_000
    return '\n'.join(rows)+'\n',points


def execute(patches,mode,cap,kind,binary='emulated'):
    raw,points=packet(patches,mode,cap,kind)
    proc=subprocess.run([str(ROOT/'bin'/binary)],input=raw,text=True,capture_output=True,timeout=30,check=True)
    result=json.loads(proc.stdout)
    assert result['box_complete'] is True and result['points_visited']==sum(points)
    assert result['counts']==[dict(id=i,expected=n,visited=n) for i,n in enumerate(points)]
    hits=set();seen=set()
    for h in result['hits']:
        index=h['task'];p,b,u=patches[index];j=(coefficient_bounds_cube if kind=='cube' else coefficient_bounds_sphere)(b)
        linear=h['linear'];assert (index,linear) not in seen;seen.add((index,linear))
        assert 0<=linear<points[index]
        ns=[]
        for bound in j:ns.append(linear%(2*bound+1)-bound);linear//=2*bound+1
        c,a,b=[sum(ns[i]*u[i][col] for i in range(3)) for col in range(3)]
        assert (a,b,c)==(h['a'],h['b'],h['c'])
        r=a**5+b**5-c**5;limit=5*c*c if mode=='healy' else cap
        assert 1<=a<=b<c and p.cmin<=c<=p.cmax and abs(r)<=limit
        if p.contains(a,b,c):hits.add((a,b,c,r))
    return hits,result


def case(bound,mode,cap):
    t=time.perf_counter();patches,small=prepare(bound,mode,cap);prep=time.perf_counter()-t
    expected=direct(bound,mode,cap)
    fallback={h for h in expected if any(lo<=h[2]<=hi for lo,hi in small)}
    results={};samples={'sphere':[],'cube':[]}
    for repeat in range(5):
        for kind in (('sphere','cube') if repeat%2==0 else ('cube','sphere')):
            hits,result=execute(patches,mode,cap,kind)
            assert hits|fallback==expected,(bound,mode,cap,kind,sorted((hits|fallback)^expected))
            samples[kind].append(result['engine_seconds']);results[kind]=result
    for kind in ('sphere','cube'):
        hits,_=execute(patches,mode,cap,kind,'emulated-ubsan');assert hits|fallback==expected
    row=dict(bound=bound,mode=mode,cap=cap,width=8,root_bits=48,patches=len(patches),geometry_seconds=prep,
        reduction_backend='original exact Fraction LLL, not production fpylll',hit_set=sorted(expected),independent_match=True,
        ubsan_passed=True,points={k:v['points_visited'] for k,v in results.items()},engine_samples=samples,
        engine_medians={k:statistics.median(v) for k,v in samples.items()})
    print(json.dumps(row),flush=True);return row


def fixtures():
    rows=[]
    for a,b,c in ((9,9,10),(13852184,27401825,27580409),(21137517920,21483066250,24482314857)):
        if c==10:p=L.make_patch(10,10,Q(4,5),Q(9,10),18098);mode='constant';cap=18098
        else:
            lo=1<<(c.bit_length()-1);hi=2*lo-1;count=(9*lo+80-1)//80;i=(a*10*count)//(c*9)
            p=L.make_patch(lo,hi,Q(9*i,10*count),Q(9*(i+1),10*count),5*hi*hi,160);mode='healy';cap=0
        reduced,u=L.lll(p.basis());patches=[(p,reduced,u)];target=(a,b,c,a**5+b**5-c**5);results={};sets={}
        for kind in ('sphere','cube'):
            hits,result=execute(patches,mode,cap,kind);assert target in hits
            sanitize,_=execute(patches,mode,cap,kind,'emulated-ubsan');assert sanitize==hits
            results[kind]=result;sets[kind]=hits
        assert sets['sphere']==sets['cube']
        row=dict(fixture=target,scope='one selected patch, not full shell',width=8 if c!=10 else None,
            points={k:v['points_visited'] for k,v in results.items()},exact_hit_set_match=True,ubsan_passed=True)
        print(json.dumps(row),flush=True);rows.append(row)
    return rows


def main():
    began=time.perf_counter();out=dict(source_commit='9a1ccf86eb8c8adae2e00e3cecbbb358345a0a45',
        python=platform.python_version(),environment='isolated x86_64 cloud, no ADA/GPU',properties=properties())
    out['cases']=[case(*args) for args in [(34,'constant',384),(100,'constant',2951),(1000,'constant',42),(1000,'healy',0)]]
    out['fixtures']=fixtures();out['elapsed_seconds']=time.perf_counter()-began
    (ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',out['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
