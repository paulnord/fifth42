"""Exact host certificates for a bounded CUDA coefficient-box prototype."""
import hashlib,importlib.util,json,sys
from fractions import Fraction as Q
from math import isqrt,prod
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MAX_BASE=100_000_000_000
MAX_I64=2**63-1
MAX_TASKS=4096
MAX_POINTS=50_000_000
MAX_PATCH_POINTS=10_000_000
FIXTURES=((13852184,27401825,27580409),(21137517920,21483066250,24482314857))

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def reference():
    metadata=json.loads((ROOT/'UPSTREAM.json').read_text())
    for name,row in metadata['files'].items():
        if sha(ROOT/name)!=row['sha256']:raise ValueError('Reference identity changed: '+name)
    name='gpu_lattice_frozen_reference'
    if name not in sys.modules:
        spec=importlib.util.spec_from_file_location(name,ROOT/'reference/lattice5.py')
        module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return sys.modules[name]
def rational(x):return [x.numerator,x.denominator]
def matrix_wire(a):return [[rational(Q(x)) for x in row] for row in a]
def matrix_read(a):return [[Q(*x) for x in row] for row in a]
def inverse(a):
    d=reference().det3(a)
    if not d:raise ValueError('Singular basis')
    result=[[Q(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3],d) for j in range(3)] for i in range(3)]
    if reference().matmul(a,result)!=[[Q(i==j) for j in range(3)] for i in range(3)]:raise ValueError('Inverse mismatch')
    return result
def ceil_sqrt(x):
    if x<0:raise ValueError('Negative square')
    k=isqrt(x.numerator//x.denominator)
    return k+(k*k<x)
def coefficient_bounds(b):
    inv=inverse(b)
    # n = x B^-1 and ||x||^2 <= 3. Cauchy-Schwarz bounds each n_j.
    return [ceil_sqrt(3*sum(inv[i][j]**2 for i in range(3))) for j in range(3)]
def integer_task_checks(task):
    u=task['U'];j=task['J']
    if len(u)!=3 or any(len(row)!=3 for row in u) or len(j)!=3:raise ValueError('Invalid task shape')
    if any(type(x)!=int or abs(x)>MAX_I64 for row in u for x in row):raise ValueError('Transform outside signed 64-bit range')
    if any(type(x)!=int or not 0<=x<=MAX_I64//2 for x in j):raise ValueError('Invalid coefficient bounds')
    for col in range(3):
        if sum(j[i]*abs(u[i][col]) for i in range(3))>MAX_I64:raise ValueError('Transform can overflow signed 64 bits')
    n=prod(2*x+1 for x in j)
    if n>MAX_PATCH_POINTS or n!=task['points']:raise ValueError('Patch point budget exceeded or inconsistent')
    if not 1<=task['cmin']<=task['cmax']<=MAX_BASE:raise ValueError('Unsupported denominator range')
    return n
def task_from_patch(cmin,cmax,left,right,cap,bits,grid_index,grid_count):
    ref=reference();p=ref.make_patch(cmin,cmax,left,right,cap,bits);a=p.basis();b,u=ref.lll(a);j=coefficient_bounds(b)
    task=dict(cmin=cmin,cmax=cmax,U=u,J=j,points=prod(2*x+1 for x in j),grid_index=grid_index,grid_count=grid_count,bits=bits,cap=cap,left=rational(left),right=rational(right),A=matrix_wire(a),B=matrix_wire(b))
    integer_task_checks(task);return task
def expected_specs(bound,mode,cap,width,selected=False):
    if mode not in ('constant','healy') or type(cap)!=int or not 0<=cap<=MAX_I64 or type(width)!=int or width<1:raise ValueError('Unsupported mode, cap, or width')
    specs=[];direct=[]
    if selected:
        if mode!='healy':raise ValueError('Fixture patches require Healy mode')
        for a,b,c in FIXTURES:
            lo=1<<(c.bit_length()-1);hi=2*lo-1;n=(9*lo+10*width-1)//(10*width);i=(a*10*n)//(c*9)
            specs.append((lo,hi,Q(9*i,10*n),Q(9*(i+1),10*n),5*hi*hi,160,i,n))
        return specs,direct
    if type(bound)!=int or not 1<=bound<=1000:raise ValueError('Full-domain preparation is capped at bound 1000')
    lo=1
    while lo<=bound:
        hi=min(2*lo-1,bound);rmax=cap if mode=='constant' else 5*hi*hi
        if Q(rmax,lo**5)>Q(9049,50000):direct.append([lo,hi])
        else:
            n=(9*lo+10*width-1)//(10*width)
            if len(specs)+n>MAX_TASKS:raise ValueError('Patch budget exceeded')
            for i in range(n):specs.append((lo,hi,Q(9*i,10*n),Q(9*(i+1),10*n),rmax,48,i,n))
        lo*=2
    return specs,direct
def make_plan(bound=100,mode='constant',cap=42,width=2,selected=False):
    specs,direct=expected_specs(bound,mode,cap,width,selected)
    if selected:bound=max(spec[1] for spec in specs)
    tasks=[];points=0
    for spec in specs:
        t=task_from_patch(*spec);points+=t['points']
        if points>MAX_POINTS:raise ValueError('Packet point budget exceeded')
        t['id']=len(tasks);tasks.append(t)
    return dict(schema=1,kind='selected-fixture-patches' if selected else 'full-positive-domain',bound=bound,mode=mode,cap=cap,width=width,tasks=tasks,direct_shells=direct,points=points,upstream_commit='ddf28f04725b29b2f1d53b5d33c16379b0f66a20')
def verify_plan(plan):
    if plan['schema']!=1 or plan['kind'] not in ('selected-fixture-patches','full-positive-domain'):raise ValueError('Unknown certificate')
    specs,direct=expected_specs(plan['bound'],plan['mode'],plan['cap'],plan['width'],plan['kind']=='selected-fixture-patches')
    if plan['kind']=='selected-fixture-patches' and plan['bound']!=max(spec[1] for spec in specs):raise ValueError('Fixture range mismatch')
    if len(specs)!=len(plan['tasks']) or direct!=plan['direct_shells'] or len(specs)>MAX_TASKS:raise ValueError('Missing domain intervals')
    ref=reference();points=0
    for index,(spec,task) in enumerate(zip(specs,plan['tasks'])):
        lo,hi,left,right,cap,bits,i,n=spec
        if (task['id'],task['cmin'],task['cmax'],task['left'],task['right'],task['cap'],task['bits'],task['grid_index'],task['grid_count'])!=(index,lo,hi,rational(left),rational(right),cap,bits,i,n):raise ValueError('Patch interval mismatch')
        p=ref.make_patch(lo,hi,left,right,cap,bits);a=matrix_read(task['A']);b=matrix_read(task['B']);u=task['U']
        if a!=p.basis() or abs(ref.det3(u))!=1 or ref.matmul(u,a)!=b:raise ValueError('Invalid lattice certificate')
        if coefficient_bounds(b)!=task['J']:raise ValueError('Coefficient enclosure was changed')
        points+=integer_task_checks(task)
    if points!=plan['points'] or points>MAX_POINTS:raise ValueError('Packet count mismatch or budget exceeded')
    return True
def packet(plan):
    verify_plan(plan);mode=1 if plan['mode']=='healy' else 0;cap=0 if mode else plan['cap']
    lines=[f'LATTICE_GPU_V1 {mode} {cap} {len(plan["tasks"])}']
    for t in plan['tasks']:
        values=[t['id'],t['cmin'],t['cmax'],*t['J'],*(x for row in t['U'] for x in row)]
        lines.append(' '.join(map(str,values)))
    return '\n'.join(lines)+'\n'
def patch_for_task(t):return reference().make_patch(t['cmin'],t['cmax'],Q(*t['left']),Q(*t['right']),t['cap'],t['bits'])
def decode(plan,result,backend):
    verify_plan(plan)
    if result.get('backend')!=backend or result.get('box_complete') is not True:raise ValueError('Backend did not complete')
    if result.get('points_visited')!=plan['points'] or len(result.get('counts',[]))!=len(plan['tasks']):raise ValueError('Incomplete point counts')
    for t,count in zip(plan['tasks'],result['counts']):
        if count!=dict(id=t['id'],expected=t['points'],visited=t['points']):raise ValueError('Missing or duplicate task count')
    hits=set();patches={};emitted=set()
    for h in result['hits']:
        if type(h['task'])!=int or not 0<=h['task']<len(plan['tasks']):raise ValueError('Invalid candidate task')
        key=(h['task'],h['linear'])
        if key in emitted:raise ValueError('Duplicate candidate coefficient')
        emitted.add(key)
        t=plan['tasks'][h['task']];index=h['linear']
        if not 0<=index<t['points']:raise ValueError('Candidate coefficient outside box')
        ns=[]
        for j in t['J']:ns.append(index%(2*j+1)-j);index//=2*j+1
        c,a,b=[sum(ns[i]*t['U'][i][col] for i in range(3)) for col in range(3)]
        if [a,b,c]!=[h['a'],h['b'],h['c']] or not 1<=a<=b<c or not t['cmin']<=c<=t['cmax']:raise ValueError('Candidate reconstruction mismatch')
        r=a**5+b**5-c**5;cap=plan['cap'] if plan['mode']=='constant' else 5*c*c
        if abs(r)>cap:raise ValueError('Incorrect exact residual')
        if t['id'] not in patches:patches[t['id']]=patch_for_task(t)
        if patches[t['id']].contains(a,b,c):hits.add((a,b,c,r))
    ref=reference();stats=ref.Stats();budget=ref.Budget(max_nodes=2_000_000,start=ref.perf_counter())
    cap_at=(lambda c:plan['cap']) if plan['mode']=='constant' else (lambda c:5*c*c)
    for lo,hi in plan['direct_shells']:hits|=ref.direct_positive(lo,hi,cap_at,lambda r,c:abs(r)<=cap_at(c),stats,budget)
    return sorted(hits)
