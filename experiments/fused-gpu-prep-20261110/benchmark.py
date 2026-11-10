"""Complete patch-preparation microbenchmark, not production search throughput."""
import argparse,json,struct,subprocess,time,sys,re,statistics,hashlib,collections
from pathlib import Path
import gmpy2 as g
from reference import from_packet,radicands,calculate_packet,certify_packet
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import lattice,precision_policy
lattice.Q=g.mpq
lattice.iroot=lambda n,k=5:int(g.iroot(n,k)[0])
# Use GMP rational arithmetic for independent certification, without root solves.
import reference
reference.Q=g.mpq

def fixtures(count,region,group):
 lo,hi=100000000001,200000000000;grid=(9*lo+79)//80
 start={'edge':0,'middle':3751385984,'cabbage':1500000000,'boole':7192000000}[region]
 result=[]
 for j in range(count):
  i=start+j*group;L,R,D=9*i,9*(i+group),10*grid
  b=precision_policy.geometry_bits(lattice,lo,hi,g.mpq(L,D),g.mpq(R,D),42)
  fields=(lo,hi,L,R,D,42,b);from_packet(*fields);result.append(fields)
 return result

def baseline(fields):
 lo,hi,L,R,D,cap,b=fields
 return lattice.make_patch(lo,hi,g.mpq(L,D),g.mpq(R,D),cap,b)

def cpu_values(fields):
 # Mathematical oracle with exact GMP roots rather than Python bitwise search.
 original=reference.root_floor
 reference.root_floor=lambda N,D,b:int(g.iroot((g.mpz(N)<<(5*b))//D,5)[0])
 try:return calculate_packet(fields)
 finally:reference.root_floor=original

def finish(fields,values):
 a=from_packet(*fields);v=certify_packet(fields,values)
 return lattice.Patch(a.cmin,a.cmax,g.mpq(fields[2],fields[4]),g.mpq(fields[3],fields[4]),v['p'],v['q'],v['m'],v['eps'],a.cap)

def reduce_cert(patch):
 A=patch.basis();B,U=lattice.reduce_basis(A,'fpylll')
 assert abs(lattice.det3(U))==1 and lattice.matmul(U,A)==B
 # exact coefficient enclosure from inverse triangular basis, same formula as exact_host_opt.
 det=lattice.det3(U)
 inv=[[ (U[(j+1)%3][(i+1)%3]*U[(j+2)%3][(i+2)%3]-U[(j+1)%3][(i+2)%3]*U[(j+2)%3][(i+1)%3])//det for j in range(3)] for i in range(3)]
 d=patch.cmax;h=(patch.right-patch.left)/2
 inverse=[[d*(inv[0][j]+patch.p*inv[1][j]+patch.q*inv[2][j]) for j in range(3)], [d*h*(inv[1][j]+patch.m*inv[2][j]) for j in range(3)], [d*patch.eps*inv[2][j] for j in range(3)]]
 assert lattice.matmul(B,inverse)==[[int(i==j) for j in range(3)] for i in range(3)]
 def ceilroot(q):
  n=int(g.isqrt(q.numerator//q.denominator));return n+int(n*n<q)
 J=tuple(ceilroot(3*sum(inverse[i][j]**2 for i in range(3))) for j in range(3))
 return tuple(map(tuple,U)),J

def run(a):
 out=Path(a.output);out.mkdir(parents=True,exist_ok=False);rows=fixtures(a.count,a.region,a.group)
 # Independent expected outputs, outside all timed regions.
 expected=[baseline(f) for f in rows];values=[cpu_values(f) for f in rows]
 assert all(finish(f,v)==p for f,v,p in zip(rows,values,expected))
 reduce_cert(expected[0]) # warm imports and fpylll initialization for both paths
 timings=[];cpu_results=[]
 for repeat in range(a.repeats):
  start=time.perf_counter();patches=[baseline(f) for f in rows];prep=time.perf_counter()-start
  start=time.perf_counter();cert_patches=[baseline(f) for f in rows];assert patches==cert_patches;cert=time.perf_counter()-start
  start=time.perf_counter();reduced=[reduce_cert(p) for p in patches];lll=time.perf_counter()-start
  cpu_results=reduced;timings.append({'prepare_s':prep,'rebuild_certificate_s':cert,'lll_and_bounds_s':lll,'total_s':prep+cert+lll})
 blob=struct.pack('<I',len(rows))+b''.join(struct.pack('<6QI',*f) for f in rows)
 (out/'input.bin').write_bytes(blob)
 report={'scope':'patch geometry + CPU rational normalization, LLL and exact certificates; no enumeration/production IO', 'region':a.region,'group':a.group,'count':len(rows),'bits':sorted(set(f[-1] for f in rows)), 'cpu':timings,'gpu':'not run','input_sha256':hashlib.sha256(blob).hexdigest(),'precision_histogram':dict(collections.Counter(f[-1] for f in rows)),'adjusted_root_reuse':sum(v[2]==v[3] for v in values),'max_output_bits':max(x.bit_length() for v in values for x in v),'output_bytes_per_patch':8192}
 if a.binary:
  # Every repeat includes a fresh subprocess: cold start intentionally included in measured wall result.
  trials=[]
  for r in range(a.repeats):
   start=time.perf_counter();p=subprocess.run([str(Path(a.binary).resolve()),str(out/'input.bin'),str(out/f'output{r}.bin'),'2'],capture_output=True,text=True);wall=time.perf_counter()-start
   (out/f'gpu{r}.stderr').write_text(p.stderr)
   if p.returncode:raise RuntimeError('GPU failed: '+p.stderr)
   raw=(out/f'output{r}.bin').read_bytes();assert len(raw)==4+len(rows)*16*512 and struct.unpack('<I',raw[:4])[0]==len(rows)
   start=time.perf_counter();packets=[tuple(int.from_bytes(raw[4+(i*16+j)*512:4+(i*16+j+1)*512],'little') for j in range(16)) for i in range(len(rows))]
   patches=[finish(f,v) for f,v in zip(rows,packets)];assert patches==expected
   decode_cert=time.perf_counter()-start
   start=time.perf_counter();reduced=[reduce_cert(p) for p in patches];assert reduced==cpu_results;lll=time.perf_counter()-start
   get=lambda pat:[float(x)/1000 for x in re.findall(pat,p.stderr)]
   kernels=get(r'kernel_ms=([0-9.]+)');h2d=get(r'h2d_ms=([0-9.]+)')[0];d2h=get(r'd2h_ms=([0-9.]+)')[0]
   trials.append({'cold_subprocess_s':wall,'kernels_s':kernels,'h2d_s':h2d,'d2h_s':d2h,'decode_and_exact_cert_s':decode_cert,'lll_and_bounds_s':lll,'cold_total_s':wall+decode_cert+lll,'warm_component_estimate_NOT_measured_pipeline_s':kernels[-1]+h2d+d2h+decode_cert+lll,'output_sha256':hashlib.sha256(raw).hexdigest()})
   if r>0:(out/f'output{r}.bin').unlink() # generated duplicate outputs; retain repeat0 and all hashes
  report['gpu']=trials;report['correctness']='all roots, geometry, basis, LLL transforms and coefficient bounds match'
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--binary');p.add_argument('--count',type=int,default=128);p.add_argument('--region',choices=['edge','middle','cabbage','boole'],default='cabbage');p.add_argument('--group',type=int,choices=[4,8,16],default=4);p.add_argument('--repeats',type=int,default=3);p.add_argument('--output',required=True);a=p.parse_args();assert 1<=a.count<=4096 and 1<=a.repeats<=10;run(a)
