"""Bounded exclusive GPU correctness then resident-kernel/host-latency timings."""
from pathlib import Path
import fcntl,json,os,selectors,statistics,struct,subprocess,time,hashlib,traceback
import gmpy2
import fixtures
R=Path(__file__).resolve().parent;E=R/'evidence';F=E/'fixtures'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def certify(rows,roots):
 for (n,d,b),k in zip(rows,roots):fixtures.exact(n,d,b,k)
def read_roots(path):
 raw=path.read_bytes();count,=struct.unpack_from('<I',raw);assert len(raw)==4+count*256
 return [int.from_bytes(raw[4+i*256:4+(i+1)*256],'little') for i in range(count)]
class Server:
 def __init__(self,binary,tag):
  self.err=(E/(tag+'.stderr.log')).open('w');self.started=time.perf_counter();self.p=subprocess.Popen([str(binary),'--server'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1);self.ready=self.line();self.startup=time.perf_counter()-self.started;assert self.ready['ready']
 def line(self):
  with selectors.DefaultSelector() as s:
   s.register(self.p.stdout,selectors.EVENT_READ)
   if not s.select(30):raise TimeoutError('GPU server response timeout')
  raw=self.p.stdout.readline()
  if not raw:raise RuntimeError('GPU server exited '+str(self.p.poll()))
  return json.loads(raw)
 def run(self,src,dest,reps):
  t=time.perf_counter();self.p.stdin.write(f'RUN {src} {dest} {reps}\n');self.p.stdin.flush();row=self.line();row['client_request_ms']=(time.perf_counter()-t)*1000;return row
 def close(self):
  if self.p.poll() is None:
   self.p.stdin.write('QUIT\n');self.p.stdin.flush()
   try:self.p.wait(timeout=3)
   except subprocess.TimeoutExpired:self.p.kill();self.p.wait()
  self.err.close()
def main():
 os.sched_setaffinity(0,set(range(8,12)));lock=Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock').open('r+');fcntl.lockf(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
 names=[p.name for p in sorted(F.iterdir()) if p.is_dir()];binaries=[R/'root_newton_power_tpi8',R/'root_newton_seeded_tpi8'];servers=[];checks=[];timings=[];begin=time.monotonic()
 try:
  rejected=[];bad=E/'native-rejections';bad.mkdir(exist_ok=True)
  def packet(n,d,b):return struct.pack('<II',1,b)+n.to_bytes(256,'little')+d.to_bytes(256,'little')
  valid=packet(1,2,88)
  cases={'overwidth':packet(1,(1<<2000)+1,222),'outside-domain':packet(2,1,88),'zero-denominator':packet(1,0,88),'zero-bits':packet(1,2,0),'bits-223':packet(1,2,223),'truncated':valid[:-1],'trailing':valid+b'x','zero-count':struct.pack('<I',0)}
  if os.environ.get('ROOT_SKIP_NATIVE')=='1':cases={}
  for name,data in cases.items():
   src=bad/(name+'.input.bin');src.write_bytes(data);dst=bad/(name+'.output.bin');done=subprocess.run([str(binaries[1]),str(src),str(dst),'1'],capture_output=True,text=True,timeout=3)
   (bad/(name+'.stderr.txt')).write_text(done.stderr);assert done.returncode!=0 and not dst.exists()
   rejected.append(dict(case=name,status='rejected',returncode=done.returncode,stderr=done.stderr))
  save(E/'NATIVE_REJECTIONS.json',dict(status='passed' if rejected else 'not_run_in_final_bounded_gpu_slot',cases=rejected,reason=None if rejected else 'Parent requested <=2-second correctness/timing slot; CPU width refusal/fallback tests remain executed'))
  for binary in binaries:
   server=Server(binary,binary.name);servers.append(server)
   for name in names:
    folder=F/name;dest=folder/(binary.name+'-correctness.bin');row=server.run(folder/'input.bin',dest,1);assert dest.read_bytes()==(folder/'expected.bin').read_bytes();rows=fixtures.read(folder/'input.bin');certify(rows,read_roots(dest));checks.append(dict(binary=binary.name,fixture=name,status='passed',response=row))
  save(E/'GPU_CORRECTNESS.json',dict(status='passed',checks=checks,cpu_certificate=True))
  for binary,server in zip(binaries,servers):
   for name in ['actual-768','actual-4096','actual-16384','dot-4096']:
    folder=F/name;rows=fixtures.read(folder/'input.bin');dest=folder/(binary.name+'-timing.bin');mpzrows=[(gmpy2.mpz(n),gmpy2.mpz(d),b) for n,d,b in rows];repeats=[]
    for repeat in range(5):
     start=time.perf_counter();cpu=[int(gmpy2.iroot((n<<(5*b))//d,5)[0]) for n,d,b in mpzrows];gmp_ms=(time.perf_counter()-start)*1000
     row=server.run(folder/'input.bin',dest,11);roots=read_roots(dest);assert roots==cpu;single=server.run(folder/'input.bin',dest,1);assert read_roots(dest)==cpu;start=time.perf_counter();certify(rows,roots);proof_ms=(time.perf_counter()-start)*1000
     start=time.perf_counter()
     for (n,d,b),k in zip(mpzrows,roots):
      k=gmpy2.mpz(k);target=n<<(5*b);assert d*k**5<=target<d*(k+1)**5
     gmp_proof_ms=(time.perf_counter()-start)*1000
     repeats.append(dict(repeat=repeat,gmp_root_ms=gmp_ms,python_proof_ms=proof_ms,gmp_proof_ms=gmp_proof_ms,response=row,single_request=single,warm_kernel_median_ms=statistics.median(row['kernel_ms'][1:])))
    timings.append(dict(binary=binary.name,fixture=name,count=len(rows),unique_input_keys=len(set(rows)),server_startup_ms=server.startup*1000,median_gmp_ms=statistics.median(x['gmp_root_ms'] for x in repeats),median_warm_kernel_ms=statistics.median(x['warm_kernel_median_ms'] for x in repeats),median_eleven_kernel_request_ms=statistics.median(x['response']['client_request_ms'] for x in repeats),median_single_request_ms=statistics.median(x['single_request']['client_request_ms'] for x in repeats),median_cpu_proof_ms=statistics.median(x['python_proof_ms'] for x in repeats),median_gmp_proof_ms=statistics.median(x['gmp_proof_ms'] for x in repeats),samples=repeats))
    save(E/'TIMINGS.json',timings)
  save(E/'RESULT.json',dict(status='passed',source_sha256=hashlib.sha256((R/'root_newton.cu').read_bytes()).hexdigest(),correctness_cases=len(checks),timing_cases=len(timings),seconds=time.monotonic()-begin,production_changed=False,production_restarted=False,timings=timings));print('PASS',len(checks),'correctness cases;',len(timings),'timing cases')
 finally:
  for server in servers:server.close()
  lock.close()
if __name__=='__main__':
 try:main()
 except BaseException as exc:save(E/'FAILURE.json',dict(error=repr(exc),traceback=traceback.format_exc()));raise
