import json,time,math
from fractions import Fraction as Q
import reference_geometry as l

def inverse(a):
    d=l.det3(a)
    r=[[(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3])/d for j in range(3)] for i in range(3)]
    assert l.matmul(a,r)==[[int(i==j) for j in range(3)] for i in range(3)]
    return r

def rootceil(x):
    k=math.isqrt(x.numerator//x.denominator)
    return k+(k*k<x)

def bounds(b):
    v=inverse(b)
    old=[rootceil(3*sum(v[i][j]**2 for i in range(3))) for j in range(3)]
    cube=[l.floor(sum(abs(v[i][j]) for i in range(3))) for j in range(3)]
    assert all(new<=prior for new,prior in zip(cube,old))
    return old,cube

lo,hi,width=100000000001,200000000000,8
count=(9*lo+10*width-1)//(10*width)
rows=[]
for index in [3750000000,3902545280,6250000000,10625000000]:
  for bits in [96,128,160,222]:
    start=time.perf_counter()
    patch=l.make_patch(lo,hi,Q(9*index,10*count),Q(9*(index+1),10*count),42,bits)
    basis=patch.basis()
    t1=time.perf_counter()
    b,u=l.lll(basis)
    t2=time.perf_counter()
    old,cube=bounds(b)
    t3=time.perf_counter()
    row=dict(index=index,ratio=float(patch.p),bits=bits,eps=float(patch.eps),geometry_seconds=t1-start,lll_seconds=t2-t1,bounds_seconds=t3-t2,total_seconds=t3-start,J_old=old,J_cube=cube,old_points=math.prod(2*x+1 for x in old),cube_points=math.prod(2*x+1 for x in cube),max_U_bits=max(abs(x).bit_length() for rr in u for x in rr))
    rows.append(row)
    print(json.dumps(row),flush=True)
with open('probe.json','w') as f:json.dump(dict(method='Python fractions exact LLL, not native mpq/fpylll and not ADA performance',rows=rows),f,indent=2)
