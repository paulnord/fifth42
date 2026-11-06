from pathlib import Path
import json,random,math
out={}
# Pure integer closed form for counts modulo 2^k; independently brute-check small k.
def n2(k,t):
 m=1<<k;t%=m
 if t&1:return m*m
 n=3*m*m//4
 if k<=5:
  return n+((m//2)**3 if t==0 else 0)
 return n+(4096*n2(k-5,t//32) if t%32==0 else 0)
for k in range(1,8):
 m=1<<k;hs=[0]*m
 for i in range(m):hs[pow(i,5,m)]+=1
 for t in range(m):
  actual=sum(nx*ny*hs[(x+y-t)%m] for x,nx in enumerate(hs) for y,ny in enumerate(hs))
  assert actual==n2(k,t),(k,t,actual,n2(k,t))
out['2adic_counts_small_exhaustive']=True
out['densities_2power']=[dict(k=k,target_either=(n2(k,42)+n2(k,-42))/(1<<k)**3,interval42=sum(n2(k,t) for t in range(-42,43))/(1<<k)**3,zero=n2(k,0)/(1<<k)**3) for k in (16,32,64)]
# Compare modular implementation and the source exact arithmetic against Python big ints via emitted nonempty hits.
for p in Path(__file__).parent.glob('*.json'):
 if '.target.' not in p.name and '.interval.' not in p.name:continue
 d=json.loads(p.read_text())
 for task,ix,a,b,c in d['hits']:
  r=a**5+b**5-c**5
  if '.target.' in p.name:assert r in (12,384,2951,-960)
  else:assert abs(r)<=(2951 if 'controls' in p.name else 42)
out['every_nonempty_hit_checked_python_bigint']=True
# Non-vacuous arbitrary signed controls, powers near overflow and factor identity.
rng=random.Random(20261106);checked=0
for _ in range(10000):
 x,y,z=[rng.randrange(-200000000000,200000000001) for i in range(3)]
 r=x**5+y**5+z**5
 for k in (16,32,64):
  m=(1<<k)-1
  lo=(((x&m)*(x&m)&m)**2*(x&m)+((y&m)*(y&m)&m)**2*(y&m)+((z&m)*(z&m)&m)**2*(z&m))&m
  assert lo==r&m
 if x+y:
  s=x+y;p=x*y;N=r-z**5
  assert N%s==0
  delta=5*s**4+20*(N//s)
  assert delta==(5*(x*x+y*y))**2 # discriminant = 25(x²+y²)²? check below
 checked+=1
out['random_bigint_modular_cases']=checked
(Path(__file__).parent/'checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
