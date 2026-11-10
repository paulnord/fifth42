"""Exact fused geometry specification. No floating point or truncated arithmetic.
GPU returns six positive rational pairs; m is represented by its magnitude.
CPU normalizes these pairs and sums four epsilon terms. LLL stays on CPU.
"""
from fractions import Fraction as Q
from math import lcm
from dataclasses import dataclass

@dataclass(frozen=True)
class Input:
    P:int; H:int; R:int; S:int
    cmin:int; cmax:int; cap:int; bits:int

def pack(cmin,cmax,left,right,cap,bits):
    left,right=Q(left),Q(right)
    p,h=(left+right)/2,(right-left)/2
    S=lcm(p.denominator,h.denominator,right.denominator)
    a=Input(int(p*S),int(h*S),int(right*S),S,cmin,cmax,cap,bits)
    validate(a)
    return a

def validate(a,width=4096):
    if not all(type(x) is int for x in a.__dict__.values()): raise ValueError('integer fields required')
    if not (1<=a.cmin<=a.cmax and 0<a.P<a.R<a.S and 0<a.H<=a.P and a.R==a.P+a.H and a.cap>=0 and 1<=a.bits<=222):
        raise ValueError('invalid domain')
    s,c,z=a.S.bit_length(),a.cmin.bit_length(),max(1,a.cap.bit_length())
    # Strict upper bounds on every unsigned intermediate, including root trial T+1.
    bound=max(5*s+5*c+5*(a.bits+1)+2,5*s+9*(a.bits+1)+2,z+5*s+2,z+4*(a.bits+1)+2)
    if bound>width: raise OverflowError('width proof fails: use CPU fallback')
    if (a.S**5-a.R**5)*a.cmin**5 <= a.cap*a.S**5: raise ValueError('singular patch')
    return bound

def root_floor(N,D,b):
    A=N<<(5*b)
    lo,hi=0,1<<b
    while lo<hi:
        mid=(lo+hi+1)//2
        if D*mid**5<=A: lo=mid
        else: hi=mid-1
    return lo

def radicands(a):
    s5,p5,r5,c5=a.S**5,a.P**5,a.R**5,a.cmin**5
    return ((s5-p5,s5),(s5-r5,s5),((s5-r5)*c5-a.cap*s5,s5*c5))

def calculate(a):
    validate(a)
    (qn,qd),(vn,vd),(an,ad)=radicands(a)
    b,T=a.bits,1<<a.bits
    nq=root_floor(qn,qd,b)
    nqh=nq if nq**5*qd == qn<<(5*b) else nq+1
    nv=root_floor(vn,vd,b)
    reuse=nv**5*ad<=an<<(5*b)
    na=nv if reuse else root_floor(an,ad,b)
    if min(nq,nv,na)<=0:raise ValueError('root precision too low')
    P,H,R,S=a.P,a.H,a.R,a.S
    x,y=nq**4,nqh**4
    pairs=(
       (nq+nqh,2*T),
       (P**4*T**4*(x+y),2*S**4*x*y),
       (nqh-nq,2*T),
       (P**4*T**4*(y-x)*H,2*S**5*x*y),
       (2*R**3*H**2*T**9,S**5*nv**9),
       (a.cap*T**4,5*a.cmin**5*na**4),
    )
    return {'roots':(nq,nqh,nv,na),'reuse':reuse,'pairs':pairs}

def certify(a,out):
    """Checks root brackets and recomputes arithmetic, without solving roots again."""
    validate(a)
    nq,nqh,nv,na=out['roots'];T=1<<a.bits
    for k,(N,D) in zip((nq,nv,na),radicands(a)):
        if not isinstance(k,int) or not 0<k<=T:raise ValueError('invalid root')
        if not D*k**5<=N<<(5*a.bits)<D*(k+1)**5:raise ValueError('root certificate')
    N,D=radicands(a)[0]
    expected_hi=nq if D*nq**5==N<<(5*a.bits) else nq+1
    if nqh!=expected_hi:raise ValueError('upper root certificate')
    # Independent Fraction path from the original patch formulas.
    p,h,r=Q(a.P,a.S),Q(a.H,a.S),Q(a.R,a.S)
    qlo,qhi,vlo,vmin=Q(nq,T),Q(nqh,T),Q(nv,T),Q(na,T)
    eta=Q(a.cap,a.cmin**5)
    ml,mh=-p**4/qlo**4,-p**4/qhi**4
    expected=((qlo+qhi)/2,-(ml+mh)/2,(qhi-qlo)/2,(mh-ml)*h/2,2*r**3*h*h/vlo**9,eta/(5*vmin**4))
    got=tuple(Q(n,d) for n,d in out['pairs'])
    if got!=expected:raise ValueError('geometry certificate')
    return {'p':p,'h':h,'q':got[0],'m':-got[1],'eps':sum(got[2:])}

def from_packet(lo,hi,L,R,D,cap,bits):
    """Packet wire fields lo,hi,L,R,D,cap uint64 and bits uint32."""
    values=(lo,hi,L,R,D,cap,bits)
    if not all(type(v) is int for v in values):raise ValueError('noninteger packet')
    if not (1<=lo<=hi<=2**40 and 0<=L<R<D<=2**40 and 0<=cap<=42 and 1<=bits<=222):
        raise ValueError('unsupported packet domain; CPU fallback')
    return Input(L+R,R-L,2*R,2*D,lo,hi,cap,bits)

def calculate_packet(fields):
    a=from_packet(*fields)
    o=calculate(a)
    nq,nqh,nv,na=o['roots']
    return (nq,nqh,nv,na)+tuple(z for pair in o['pairs'] for z in pair)

def certify_packet(fields,values):
    if len(values)!=16:raise ValueError('expected 16 values')
    if any(type(v) is not int or not 0<=v<2**4096 for v in values):raise ValueError('invalid unsigned output')
    if any(d==0 for d in values[5::2]):raise ValueError('zero denominator')
    a=from_packet(*fields)
    nq,nqh,nv,na=values[:4]
    N,D=radicands(a)[0]
    out={'roots':(nq,nqh,nv,na),'pairs':tuple(zip(values[4::2],values[5::2]))}
    return certify(a,out)
