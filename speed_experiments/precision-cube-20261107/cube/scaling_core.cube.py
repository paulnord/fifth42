"""Exact, immutable plans for the multicore/persistent-engine experiment."""
from dataclasses import dataclass, asdict, replace
import hashlib
import importlib.util
import json
from math import gcd, isqrt, prod
import multiprocessing
import os
from pathlib import Path
import sys

MAX_BOUND=32000
MAX_TASKS=4096
MAX_POINTS=50_000_000
MAX_PATCH_POINTS=10_000_000
MAX_TOTAL_TASKS=16384
MAX_TOTAL_POINTS=250_000_000
MAX_I64=2**63-1
_ENGINE=None

def initialize(source, cpus=()):
    global _ENGINE
    sys.dont_write_bytecode=True
    if multiprocessing.current_process()._identity:
        import ctypes,signal
        parent=os.getppid()
        if ctypes.CDLL(None,use_errno=True).prctl(1,signal.SIGKILL,0,0,0) or os.getppid()!=parent:
            raise RuntimeError('Patch worker parent-lifetime guard failed')
    if cpus:
        identity=multiprocessing.current_process()._identity
        index=(identity[0]-1 if identity else 0)%len(cpus)
        os.sched_setaffinity(0,{cpus[index]})
    if _ENGINE is not None:
        if _ENGINE[0]!=str(source):raise RuntimeError('Exact source changed within a worker')
        return
    import importlib.metadata
    pins={'sympy':'1.14.0','fpylll':'0.6.4','cysignals':'1.12.5','numpy':'2.3.5','gmpy2':'2.2.2'}
    if sys.version_info[:2]!=(3,12) or any(importlib.metadata.version(k)!=v for k,v in pins.items()):
        raise RuntimeError('Pinned Python/dependency environment mismatch')
    source=Path(source)
    sys.path[:0]=[str(source),str(source/'compiled_experiment')]
    path=source/'compiled_experiment/benchmark_mpq.py'
    spec=importlib.util.spec_from_file_location('_scaling_exact_arithmetic',path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    lattice,_=module.engine('mpq')
    lattice.reduce_basis([[lattice.Q(int(i==j)) for j in range(3)] for i in range(3)],'fpylll')
    _ENGINE=(str(source),lattice)

def worker_identity(ignored):
    import time
    time.sleep(.005)
    return (os.getpid(),tuple(sorted(os.sched_getaffinity(0))))

def lattice():
    if _ENGINE is None:raise RuntimeError('Exact engine is not initialized')
    return _ENGINE[1]

def wire(matrix):return tuple(tuple((int(x.numerator),int(x.denominator)) for x in row) for row in matrix)
def read(matrix):
    q=lattice().Q
    return [[q(*value) for value in row] for row in matrix]

def ceil_sqrt(value):
    if value<0:raise ValueError('Negative square')
    n=isqrt(int(value.numerator//value.denominator))
    return n+int(n*n<value)

def coefficient_bounds(b):
    l=lattice();d=l.det3(b)
    if not d:raise ValueError('Singular basis')
    inv=[[(b[(j+1)%3][(i+1)%3]*b[(j+2)%3][(i+2)%3]
          -b[(j+1)%3][(i+2)%3]*b[(j+2)%3][(i+1)%3])/d for j in range(3)] for i in range(3)]
    if l.matmul(b,inv)!=[[int(i==j) for j in range(3)] for i in range(3)]:
        raise ValueError('Exact inverse certificate failed')
    # Every valid mapped point is in the normalized cube [-1,1]^3.
    # n = x B^-1 implies |n_j| <= sum_i |(B^-1)_ij|. Since n_j is
    # integer, floor is the exact outward integer bound. This intentionally
    # drops irrelevant sphere/box points, never a point in the covered cube.
    bounds=[sum(abs(inv[i][j]) for i in range(3)) for j in range(3)]
    return tuple(int(v.numerator//v.denominator) for v in bounds)

@dataclass(frozen=True)
class Task:
    id:int
    cmin:int
    cmax:int
    left:tuple
    right:tuple
    cap:int
    bits:int
    U:tuple
    J:tuple
    points:int
    A:tuple
    B:tuple

@dataclass(frozen=True)
class Batch:
    tasks:tuple
    packet:str
    points:int

@dataclass(frozen=True)
class VerifiedPlan:
    bound:int
    cap:int
    batches:tuple
    direct_hits:tuple
    tasks:int
    points:int
    certificate_sha256:str

def specs(bound,cap=42,width=2):
    if type(bound)!=int or not 1<=bound<=MAX_BOUND:raise ValueError('Scaling bound outside [1,32000]')
    if type(cap)!=int or not 0<=cap<=1_000_000:raise ValueError('Unsupported residual cap')
    if type(width)!=int or width<1:raise ValueError('Invalid patch width')
    l=lattice();rows=[];direct=[];lo=1
    while lo<=bound:
        hi=min(2*lo-1,bound)
        if l.Q(cap,lo**5)>l.Q(9049,50000):direct.append((lo,hi))
        else:
            count=(9*lo+10*width-1)//(10*width)
            if len(rows)+count>MAX_TOTAL_TASKS:raise ValueError('Full-domain task allowance exhausted')
            for i in range(count):
                def pair(n,d):
                    factor=gcd(n,d);return (n//factor,d//factor)
                rows.append((len(rows),lo,hi,pair(9*i,10*count),pair(9*(i+1),10*count),cap,48))
        lo*=2
    return rows,direct

def prepare_task(spec):
    ident,lo,hi,left,right,cap,bits=spec;l=lattice()
    p=l.make_patch(lo,hi,l.Q(*left),l.Q(*right),cap,bits)
    a=p.basis();b,u=l.reduce_basis(a,'fpylll');j=coefficient_bounds(b)
    return Task(ident,lo,hi,left,right,cap,bits,tuple(tuple(int(x) for x in row) for row in u),
                j,prod(2*x+1 for x in j),wire(a),wire(b))

def certify_task(task):
    l=lattice()
    if not 1<=task.cmin<=task.cmax<=MAX_BOUND:raise ValueError('Invalid certified denominator interval')
    if len(task.U)!=3 or any(len(row)!=3 for row in task.U):raise ValueError('Invalid transform shape')
    if len(task.J)!=3 or any(type(j)!=int or not 0<=j<=MAX_I64//2 for j in task.J):
        raise ValueError('Invalid coefficient bounds')
    if any(type(x)!=int or abs(x)>MAX_I64 for row in task.U for x in row):raise ValueError('Invalid integer transform')
    for col in range(3):
        if sum(task.J[i]*abs(task.U[i][col]) for i in range(3))>MAX_I64:
            raise ValueError('Integer transform can overflow')
    points=prod(2*x+1 for x in task.J)
    if points!=task.points or points>MAX_PATCH_POINTS:raise ValueError('Patch point allowance mismatch')
    a=read(task.A);b=read(task.B)
    p=l.make_patch(task.cmin,task.cmax,l.Q(*task.left),l.Q(*task.right),task.cap,task.bits)
    if a!=p.basis() or abs(l.det3(task.U))!=1 or l.matmul(task.U,a)!=b:
        raise ValueError('Exact reduction certificate mismatch')
    if coefficient_bounds(b)!=task.J:raise ValueError('Coefficient enclosure mismatch')
    return task_digest(task)

def task_digest(task):
    return hashlib.sha256(json.dumps(asdict(task),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def checked_tasks(specifications,tasks):
    if len(tasks)!=len(specifications):raise ValueError('Missing prepared patches')
    for specification,task in zip(specifications,tasks):
        expected=(task.id,task.cmin,task.cmax,task.left,task.right,task.cap,task.bits)
        if expected!=specification:raise ValueError('Prepared patch interval/order mismatch')

def encode_batch(tasks,cap):
    if len(tasks)>MAX_TASKS:raise ValueError('Packet task allowance exceeded')
    points=sum(t.points for t in tasks)
    if points>MAX_POINTS:raise ValueError('Packet point allowance exceeded')
    lines=[f'LATTICE_GPU_V1 0 {cap} {len(tasks)}']
    for local,t in enumerate(tasks):
        row=[local,t.cmin,t.cmax,*t.J,*(x for row in t.U for x in row)]
        lines.append(' '.join(map(str,row)))
    return Batch(tuple(tasks),'\n'.join(lines)+'\n',points)

def assemble(bound,cap,specifications,direct,tasks,certificates):
    checked_tasks(specifications,tasks)
    if len(certificates)!=len(tasks) or any(len(x)!=64 for x in certificates):
        raise ValueError('Missing exact patch certificates')
    if any(task_digest(task)!=digest for task,digest in zip(tasks,certificates)):
        raise ValueError('Patch certificates do not identify the prepared immutable tasks')
    total=sum(t.points for t in tasks)
    if total>MAX_TOTAL_POINTS:raise ValueError('Full-domain coefficient allowance exhausted')
    groups=[];pending=[];points=0
    for task in tasks:
        if task.points>MAX_POINTS:raise ValueError('Single task cannot fit a packet')
        if pending and (len(pending)==MAX_TASKS or points+task.points>MAX_POINTS):
            groups.append(encode_batch(pending,cap));pending=[];points=0
        pending.append(task);points+=task.points
    if pending:groups.append(encode_batch(pending,cap))
    hits=[]
    for lo,hi in direct:
        for c in range(lo,hi+1):
            for b in range(1,c):
                for a in range(1,b+1):
                    r=a**5+b**5-c**5
                    if abs(r)<=cap:hits.append((a,b,c,r))
    digest=hashlib.sha256(('\n'.join(certificates)+'\n').encode()).hexdigest()
    return VerifiedPlan(bound,cap,tuple(groups),tuple(sorted(set(hits))),len(tasks),total,digest)

def decode_batch(batch,result,backend):
    if result.get('backend')!=backend or result.get('box_complete') is not True:
        raise ValueError('Engine did not complete the requested backend')
    if result.get('points_visited')!=batch.points or len(result.get('counts',()))!=len(batch.tasks):
        raise ValueError('Incomplete packet coverage')
    for local,(task,count) in enumerate(zip(batch.tasks,result['counts'])):
        if count!=dict(id=local,expected=task.points,visited=task.points):raise ValueError('Task coverage mismatch')
    l=lattice();hits=set();seen=set();patches={}
    for h in result['hits']:
        if type(h['task'])!=int or not 0<=h['task']<len(batch.tasks):raise ValueError('Invalid candidate task')
        task=batch.tasks[h['task']];index=h['linear'];key=(h['task'],index)
        if type(index)!=int or not 0<=index<task.points or key in seen:raise ValueError('Duplicate/invalid candidate index')
        seen.add(key);ns=[]
        for j in task.J:ns.append(index%(2*j+1)-j);index//=2*j+1
        c,a,b=[sum(ns[i]*task.U[i][col] for i in range(3)) for col in range(3)]
        r=a**5+b**5-c**5
        if (a,b,c)!=(h['a'],h['b'],h['c']) or not (1<=a<=b<c and task.cmin<=c<=task.cmax) or abs(r)>task.cap:
            raise ValueError('Candidate reconstruction or exact residual failed')
        if task.id not in patches:
            patches[task.id]=l.make_patch(task.cmin,task.cmax,l.Q(*task.left),l.Q(*task.right),task.cap,task.bits)
        if patches[task.id].contains(a,b,c):hits.add((a,b,c,r))
    return hits
