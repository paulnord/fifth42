import importlib.util,json,random,sys,time
from fractions import Fraction as Q
from pathlib import Path
from prototype import newton_bracket,division_free_bracket
source=Path(sys.argv[1]); spec=importlib.util.spec_from_file_location('fifth42_oracle',source); oracle=importlib.util.module_from_spec(spec);sys.modules[spec.name]=oracle;spec.loader.exec_module(oracle)
cases=[]
for b in [1,2,16,53,80,128,180,222]:
 for q in [Q(0),Q(1),Q(1,2),Q(1,3),Q(1,10**120)]:cases.append((q,b,'edge'))
 for n in [1,2,(1<<b)//2,(1<<b)-1]:
  if n>(1<<b):continue
  q=Q(n,1<<b)**5
  for delta in [-1,0,1]:
   t=q+Q(delta,1<<(5*b+8))
   if 0<=t<=1:cases.append((t,b,'boundary'))
r=random.Random(42192)
for _ in range(100):
 den=r.randrange(1,1<<180);cases.append((Q(r.randrange(den+1),den),r.choice([53,80,128,180,222]),'random'))
lo=100000000001;count=(9*lo+79)//80
for idx in [0,1,3751385984,6000000000,7192000000,count-2,count-1]:
 for group in [1,4,8]:
  end=min(idx+group,count);left=Q(9*idx,10*count);right=Q(9*end,10*count);p=(left+right)/2
  for b in [80,128,222]:
   for x in [1-p**5,1-right**5,1-right**5-Q(42,lo**5)]:cases.append((x,b,'production-shape'))
for x,b,kind in cases:
 if kind=='production-shape':
  assert newton_bracket(x,b,2048)==division_free_bracket(x,b,2048)
totals={};maxwidth=max(max(x.numerator.bit_length(),x.denominator.bit_length())+5*(b+1) for x,b,_ in cases)
for name,fn in [('source-reference',oracle.root_bracket),('newton',lambda x,b:newton_bracket(x,b,4096)),('division-free',lambda x,b:division_free_bracket(x,b,4096))]:
 start=time.perf_counter();res=[fn(x,b) for x,b,_ in cases];totals[name]=time.perf_counter()-start
 if name=='source-reference':reference=res
 else:assert res==reference,name
for fn in [newton_bracket,division_free_bracket]:
 try:fn(Q(1,3),222,256)
 except OverflowError:pass
 else:raise AssertionError('overflow not rejected')
print(json.dumps({'cases':len(cases),'matching_backends':3,'max_proven_intermediate_bits':maxwidth,'cpu_python_seconds_not_gpu_benchmark':totals,'source':str(source),'gpu_compile':'not run: nvcc absent','production_changed':False},indent=2))
