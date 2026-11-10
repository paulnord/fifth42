"""Generate bounded fixtures, run isolated binary, certify every result with bigint."""
import argparse,json,random,struct,subprocess,time
from pathlib import Path
from fractions import Fraction as Q
from prototype import check_input,finish,newton_bracket
p=argparse.ArgumentParser();p.add_argument('--binary');p.add_argument('--output',default='evidence');p.add_argument('--count',type=int,default=1024);a=p.parse_args()
if a.count<1:raise SystemExit('count must be positive')
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
r=random.Random(42);cases=[]
for b in [1,53,88,128,176,222]:
 for x in [Q(0),Q(1),Q(1,2),Q(1,3)]:cases.append((x,b))
 for n in [1,(1<<b)-1]:
  for e in [-1,0,1]:
   x=Q(n,1<<b)**5+Q(e,1<<(5*b))
   if 0<=x<=1:cases.append((x,b))
lo=100000000001;count=(9*lo+79)//80
for i in [0,1,3751385984,7192000000,count-4]:
 left=Q(9*i,10*count);right=Q(9*min(i+4,count),10*count);mid=(left+right)/2
 for b in [88,176,222]:
  for x in [1-mid**5,1-right**5,1-right**5-Q(42,lo**5)]:cases.append((x,b))
while len(cases)<a.count:
 den=r.randrange(1,1<<350);cases.append((Q(r.randrange(den+1),den),r.choice([53,88,128,176,222])))
cases=cases[:max(a.count,len(cases))]
records=[];fallback=0
for x,b in cases:
 try:check_input(x,b,2048)
 except OverflowError:fallback+=1;continue
 records.append((x,b))
blob=struct.pack('<I',len(records))+b''.join(struct.pack('<I',b)+x.numerator.to_bytes(256,'little')+x.denominator.to_bytes(256,'little') for x,b in records)
(out/'input.bin').write_bytes(blob)
start=time.perf_counter();brackets=[newton_bracket(x,b)[0] for x,b in records];expected=[q.numerator*(1<<b)//q.denominator for q,(_,b) in zip(brackets,records)];cpu=time.perf_counter()-start
try:
 import gmpy2
 start=time.perf_counter();gmp_roots=[int(gmpy2.iroot((x.numerator<<(5*b))//x.denominator,5)[0]) for x,b in records];gmp_seconds=time.perf_counter()-start
 assert gmp_roots==expected
except ImportError:gmp_seconds=None
report={'gmp_iroot_seconds':gmp_seconds,'records':len(records),'width_fallbacks':fallback,'python_reference_seconds_not_GMP':cpu,'gpu':'not run'}
if a.binary:
 start=time.perf_counter();run=subprocess.run([str(Path(a.binary).resolve()),str(out/'input.bin'),str(out/'output.bin'),'6'],capture_output=True,text=True);wall=time.perf_counter()-start
 (out/'gpu.stdout').write_text(run.stdout);(out/'gpu.stderr').write_text(run.stderr)
 if run.returncode:raise SystemExit('GPU binary failed; inspect gpu.stderr')
 data=(out/'output.bin').read_bytes()
 assert len(data)==4+256*len(records),'output size mismatch'
 assert struct.unpack('<I',data[:4])[0]==len(records)
 cert_start=time.perf_counter()
 for i,(x,b) in enumerate(records):
  n=int.from_bytes(data[4+i*256:4+(i+1)*256],'little');finish(x,b,n);assert n==expected[i]
 report['python_certificate_seconds']=time.perf_counter()-cert_start
 report.update(gpu='all exact certificates passed',process_wall_seconds=wall)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
