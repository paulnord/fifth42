"""CPU-only reference/fixtures for exact GPU Newton root candidates."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,random,struct,sys,time
import gmpy2
R=Path(__file__).resolve().parent;E=R/'evidence';F=E/'fixtures'
def check(n,d,b):
 if not (0<=n<=d and d>0 and 1<=b<=222):raise ValueError('unsupported domain')
 width=max(n.bit_length(),d.bit_length())+5*(b+1)
 if width>2048:raise OverflowError('CPU fallback: fixed-width proof failed')
 return next(w for w in (512,1024,2048) if width<=w)
def exact(n,d,b,k):
 value=n<<(5*b)
 if not d*k**5<=value<d*(k+1)**5:raise ArithmeticError('bad root candidate')
def cpu_newton(n,d,b,seed=None):
 check(n,d,b);t=(n<<(5*b))//d
 if not t:return 0
 upper=1<<((t.bit_length()+4)//5)
 r=seed if seed is not None and seed>0 and seed<=upper and seed**5>=t else upper
 for steps in range(64):
  z=(4*r+t//r**4)//5
  if z>=r:exact(n,d,b,r);return r
  r=z
 raise RuntimeError('iteration guard')
def save(name,cases):
 folder=F/name;folder.mkdir(parents=True,exist_ok=True);accepted=[];rejected=[];expected=[];widths={str(x):0 for x in (512,1024,2048)}
 for n,d,b,meta in cases:
  try:w=check(n,d,b)
  except (ValueError,OverflowError) as exc:
   fallback=dict(numerator=str(n),denominator=str(d),bits=b,reason=str(exc),meta=meta)
   if 0<=n<=d and d>0 and 1<=b<=222:
    k=int(gmpy2.iroot((gmpy2.mpz(n)<<(5*b))//d,5)[0]);exact(n,d,b,k);fallback.update(cpu_fallback_root=str(k),cpu_fallback_certificate_passed=True)
   else:fallback['cpu_fallback_status']='invalid_domain_not_admissible'
   rejected.append(fallback);continue
  k=int(gmpy2.iroot((gmpy2.mpz(n)<<(5*b))//d,5)[0]);exact(n,d,b,k);assert cpu_newton(n,d,b)==k
  accepted.append((n,d,b));expected.append(k);widths[str(w)]+=1
 blob=struct.pack('<I',len(accepted))+b''.join(struct.pack('<I',b)+n.to_bytes(256,'little')+d.to_bytes(256,'little') for n,d,b in accepted)
 (folder/'input.bin').write_bytes(blob);(folder/'expected.bin').write_bytes(struct.pack('<I',len(expected))+b''.join(k.to_bytes(256,'little') for k in expected))
 info=dict(name=name,count=len(accepted),width_counts=widths,rejected=rejected,input_sha256=hashlib.sha256(blob).hexdigest());(folder/'metadata.json').write_text(json.dumps(info,indent=2)+'\n');return info
def read(path):
 raw=Path(path).read_bytes();count,=struct.unpack_from('<I',raw);assert len(raw)==4+516*count
 return [(int.from_bytes(raw[8+i*516:8+i*516+256],'little'),int.from_bytes(raw[8+i*516+256:4+(i+1)*516],'little'),struct.unpack_from('<I',raw,4+i*516)[0]) for i in range(count)]
def build():
 tests=0
 for d in range(1,65):
  for n in range(d+1):
   for b in (1,2,3,8,16):
    k=int(gmpy2.iroot((gmpy2.mpz(n)<<(5*b))//d,5)[0]);assert cpu_newton(n,d,b)==k
    for seed in [0,1,k-1,k,k+1,1<<(b+5)]:assert cpu_newton(n,d,b,seed)==k
    for bad in [k-1,k+1]:
     try:exact(n,d,b,bad)
     except ArithmeticError:pass
     else:raise AssertionError('bad candidate accepted')
    tests+=1
 actual=json.loads(Path('/home/pnord/scratch/fifth42-gpu-prep-profile-20261110/ACTUAL_ROOT_INPUTS.json').read_bytes());cases=[(int(x['numerator']),int(x['denominator']),x['bits'],x) for x in actual]
 out=[save('actual-768',cases)]
 for count in [4096,16384]:out.append(save('actual-'+str(count),[cases[i%len(cases)] for i in range(count)]))
 cusp=json.loads(Path('/home/pnord/scratch/fifth42-gpu-prep-profile-20261110/CUSP_AND_GROUP8_ROOT_INPUTS.json').read_bytes());out.append(save('actual-cusp-group8',[(int(x['numerator']),int(x['denominator']),x['bits'],x) for x in cusp]))
 for count in [256,1024,4096]:
  path=Path('/home/pnord/scratch/fifth42-gpu-root-test-r2-40cqred7/evidence')/f'tpi8-count{count}/input.bin';rows=read(path);out.append(save('dot-'+str(count),[(n,d,b,dict(kind='Dot original accepted fixture')) for n,d,b in rows]))
 rng=random.Random(54321);boundary=[]
 for b in [1,2,53,88,128,176,222]:
  for k in [0,1,2,(1<<b)//2,(1<<b)-1,1<<b]:
   for delta in [-1,0,1]:
    q=Q(k,1<<b)**5+Q(delta,1<<(5*b+8))
    if 0<=q<=1:boundary.append((q.numerator,q.denominator,b,dict(kind='root-boundary',k=str(k),delta=delta)))
 for _ in range(2048):
  d=rng.randrange(1,1<<rng.randrange(1,600));n=rng.randrange(d+1);b=rng.choice([1,53,88,128,176,222]);q=Q(n,d);boundary.append((q.numerator,q.denominator,b,dict(kind='random')))
 out.append(save('boundary-random',boundary))
 (E/'CPU_VALIDATION.json').write_text(json.dumps(dict(status='passed',exhaustive_cases=tests,adversarial_seed_variants=6,bad_candidate_rejections=2*tests,fixtures=out),indent=2)+'\n');print(json.dumps(dict(status='passed',exhaustive_cases=tests,fixture_counts=[(x['name'],x['count']) for x in out]),indent=2))
if __name__=='__main__':build()
