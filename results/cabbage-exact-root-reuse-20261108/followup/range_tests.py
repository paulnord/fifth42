import json,random,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'baseline/source/lattice_gpu'))
from engine_session import EngineSession
B=200_000_000_000;mask=2**192-1
assert 3*B**5+2**63<2**191
values=[0,1,-1,2**32-1,2**32,2**32+1,100_000_000_000,-100_000_000_000,100_000_000_001,-100_000_000_001,B-1,-B+1,B,-B]
rng=random.Random(205942)
pairs=[(x,y) for x in values for y in values]+[(rng.randint(-B,B),rng.randint(-B,B)) for _ in range(512)]
packet='ARITH_V1 '+str(len(pairs))+'\n'+'\n'.join(f'{x} {y}' for x,y in pairs)+'\n'
records=[]
for name,backend in [('emulated','emulated'),('emulated_ubsan','emulated'),('cuda','gpu')]:
 start=time.perf_counter();proc=subprocess.run([str(root/'device/bin'/name),'--arithmetic'],input=packet,text=True,capture_output=True,timeout=30,check=True)
 (root/(name+'-arithmetic.json')).write_text(proc.stdout)
 result=json.loads(proc.stdout)
 assert result['backend']==backend and len(result['arithmetic'])==len(pairs)
 for (x,y),row in zip(pairs,result['arithmetic']):
  p,q=x**5,y**5
  for key,want in [('p',p),('q',q),('sum',p+q),('negative',-p-q),('square5',5*x*x)]:
   assert sum(int(w)<<(64*i) for i,w in enumerate(row[key]))==want&mask,(name,x,y,key)
  assert row['lt']==(p<q) and row['eq']==(p==q)
 records.append(dict(test='signed_arithmetic',binary=name,cases=len(pairs),seconds=time.perf_counter()-start))
# Tiny coefficient packets exercise new range boundaries and nonempty native hits.
# n0 in [-1,0,1], n1=n2=0: only +1 can satisfy the positive domain.
cases=[('old_limit_plus_one',100_000_000_001,100_000_000_001,99_999_999_999,100_000_000_000,0,42,False),
 ('new_limit',B,B,B-2,B-1,0,42,False),
 ('large_nonempty_healy',24482314857,24482314857,21137517920,21483066250,1,0,True)]
responses={};started=time.monotonic()
for binary,backend in [('scaling_cpu','emulated'),('scaling_cpu_ubsan','emulated'),('scaling_gpu','gpu')]:
 with EngineSession([str(root/'device/bin'/binary)],backend,time.monotonic()+60) as session:
  out=[]
  for label,lo,hi,a,b,mode,cap,nonempty in cases:
   data=f'LATTICE_GPU_V1 {mode} {cap} 1\n0 {lo} {hi} 1 0 0 {hi} {a} {b} 0 0 0 0 0 0\n'
   got,wall=session.run(data,timeout=10)
   assert got['box_complete'] is True and got['points_visited']==3
   assert got['counts']==[dict(id=0,expected=3,visited=3)]
   expected=[dict(task=0,linear=2,a=a,b=b,c=hi)] if nonempty else []
   assert got['hits']==expected,(binary,label,got)
   ref=subprocess.run([str(root/'native/bin/gmp_reference')],input=data,text=True,capture_output=True,check=True,timeout=10)
   independent=json.loads(ref.stdout)
   assert got['counts']==independent['counts'] and got['hits']==independent['hits']
   out.append(dict(label=label,response=got,wall_seconds=wall))
  # Deliberate fail-closed controls, with expected native rejection.
  for label,data in [('above_limit',f'LATTICE_GPU_V1 0 42 1\n0 1 {B+1} 0 0 0 1 0 0 0 1 0 0 0 1\n'),('transform_overflow',f'LATTICE_GPU_V1 0 42 1\n0 1 {B} 2 0 0 9223372036854775807 0 0 0 1 0 0 0 1\n')]:
   got,wall=session.run(data,timeout=10)
   assert got['box_complete'] is False and got['error']==('invalid base range' if label=='above_limit' else 'transform may overflow'),got
   out.append(dict(label=label,response=got,wall_seconds=wall))
  responses[binary]=out
(root/'range-test-results.json').write_text(json.dumps(dict(status='passed',arithmetic=records,enumeration=responses,range_guard_retained=True,production_coverage=False),indent=2)+'\n')
print('Passed:',len(pairs),'signed arithmetic cases per backend; boundary counts/hits/GMP; nonempty large fixture; out-of-range and overflow rejection controls.')
