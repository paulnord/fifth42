"""Run Dot's immutable package with an explicit correctness gate before timings."""
from pathlib import Path
import fcntl,hashlib,json,os,runpy,shlex,struct,subprocess,sys,tarfile,time,traceback
R=Path(__file__).resolve().parent;E=R/'evidence';P=R/'repo/experiments/gpu-root-prep-20261110'
PY='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python3'
COMMIT='e6979d463aa8c22f627f5d40955750c6472850ee'
ENV=dict(os.environ,PATH=str(R/'toolchain')+':'+str(Path(PY).parent)+':'+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
COMMANDS=[];START=time.time()
def save(path,row):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(row,indent=2)+'\n')
def run(name,args,cwd=R,env=None,timeout=600):
 print(name,shlex.join(map(str,args)),flush=True);start=time.time();stdout=E/'logs'/(name+'.stdout.log');stderr=E/'logs'/(name+'.stderr.log');stdout.parent.mkdir(exist_ok=True)
 with stdout.open('w') as out,stderr.open('w') as err:
  try:done=subprocess.run(list(map(str,args)),cwd=cwd,env=env or ENV,stdout=out,stderr=err,timeout=timeout);code=done.returncode
  except subprocess.TimeoutExpired:code=124
 row=dict(name=name,argv=list(map(str,args)),cwd=str(cwd),started_epoch=start,seconds=time.time()-start,returncode=code,stdout=str(stdout.relative_to(E)),stderr=str(stderr.relative_to(E)))
 COMMANDS.append(row);save(E/'commands.json',COMMANDS);return code
def must(name,args,**kwargs):
 code=run(name,args,**kwargs)
 if code:raise RuntimeError(f'{name} failed ({code}); retained full logs')
def reject_inputs(binary,backend):
 dest=E/'correctness'/backend/'rejections';dest.mkdir(parents=True,exist_ok=True)
 def packet(n,d,b):return struct.pack('<II',1,b)+n.to_bytes(256,'little')+d.to_bytes(256,'little')
 good=packet(1,2,88);cases={'overwidth':packet(1,(1<<2000)+1,222),'outside-unit-interval':packet(2,1,88),'zero-denominator':packet(1,0,88),'zero-bits':packet(1,2,0),'bits-223':packet(1,2,223),'truncated':good[:-1],'trailing':good+b'x','zero-count':struct.pack('<I',0)}
 result=[]
 for name,data in cases.items():
  src=dest/(name+'.input.bin');src.write_bytes(data);out=dest/(name+'.output.bin');code=run(f'{backend}-reject-{name}',[binary,src,out,'1'])
  assert code!=0 and not out.exists(),f'Unsupported input accepted: {backend} {name}'
  result.append(dict(case=name,status='rejected',returncode=code))
 save(dest/'RESULTS.json',result)
def main():
 os.sched_setaffinity(0,set(range(16)))
 lease=Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock').open('r+')
 fcntl.lockf(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
 try:
  assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPU occupied'
  assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R/'repo',text=True).strip()==COMMIT
  must('package-checksums',['sha256sum','--check','SHA256SUMS'],cwd=P)
  for name,args in [('nvidia-smi',['nvidia-smi','-q']),('nvcc-version',['nvcc','--version']),('host-compiler',['g++-13','--version']),('cpu',['lscpu']),('memory',['free','-h']),('unrelated-cpu-activity',['ps','-eo','pid,comm,pcpu,pmem','--sort=-pcpu']),('python-gmp',[PY,'-c','import sys,gmpy2;print(sys.version);print(gmpy2.version());print(gmpy2.mp_version())'])]:must(name,args)
  save(E/'environment.json',dict(source_commit=COMMIT,package=str(P),python=PY,nvcc_wrapper=str(R/'toolchain/nvcc'),nvcc_actual='/home/pnord/scratch/fifth42-gpu-root-test-d3wai41j/installation-check/cuda-local-layout/bin/nvcc',host_compiler='/usr/bin/g++-13',cuda_arch='sm_86',cpu_affinity=list(range(16)),gmp_available=True,gpu_lease_held=True,production_restart=False))
  must('exact-cpu-correctness',[PY,P/'test_cpu.py'])
  must('archived-oracle-correctness',[PY,P/'validate.py',R/'repo/lattice_prototype/compiled_experiment/lattice5_snapshot.py'])
  # Record each rejected rational explicitly; the unchanged checker reports
  # totals, while this read-only execution exposes its generated fixture list.
  fixture_code='''import json,runpy,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));count=sys.argv[2];out=Path(sys.argv[3]);sys.argv=[str(p),'--count',count,'--output',str(out)]
g=runpy.run_path(str(p),run_name='__main__');rejected=[]
for x,b in g['cases']:
 try:g['check_input'](x,b,2048)
 except OverflowError as e:rejected.append(dict(numerator=str(x.numerator),denominator=str(x.denominator),bits=b,required_bits=max(x.numerator.bit_length(),x.denominator.bit_length())+5*(b+1),reason=str(e)))
(out/'unsupported-cases.json').write_text(json.dumps(rejected,indent=2)+'\\n')
'''
  (R/'record_fixtures.py').write_text(fixture_code)
  for count in (256,1024,4096):must(f'fixture-gmp-{count}',[PY,R/'record_fixtures.py',P/'gpu_check.py',count,E/'correctness'/f'fixtures-{count}'])
  if not (E/'CGBN/.git').exists():must('cgbn-download',['git','clone','https://github.com/NVlabs/CGBN.git',E/'CGBN'])
  must('cgbn-pin',['git','checkout','--detach','114601b07ae8c3e4d46b250208ea8d9def7a12f0'],cwd=E/'CGBN')
  archive=E/'cupqc.tar.gz'
  if not archive.exists():must('cupqc-download',['curl','--fail','--location','--retry','2','https://developer.nvidia.com/downloads/compute/cupqc/downloads/secure/cupqc-sdk-0.6.0-x86_64.tar.gz','-o',archive])
  digest=hashlib.sha256(archive.read_bytes()).hexdigest();assert digest=='8026ac00d81130180d2ff0afb3eb9bce852b76cc6a02141f9e45b799a17ae571','SDK hash mismatch'
  save(E/'dependency-identities.json',dict(cgbn_commit='114601b07ae8c3e4d46b250208ea8d9def7a12f0',cupqc_version='0.6.0',cupqc_archive_sha256=digest,cupqc_archive_bytes=archive.stat().st_size))
  if not (E/'cupqc-sdk-0.6.0-x86_64').exists():
   with tarfile.open(archive) as tar:tar.extractall(E,filter='data')
  sdk=E/'cupqc-sdk-0.6.0-x86_64';assert (sdk/'include/cupqc/bigint.hpp').exists() or (sdk/'include/bigint.hpp').exists()
  env=dict(ENV,CUPQC_ROOT=str(sdk),LD_LIBRARY_PATH=str(sdk/'lib')+':'+str(sdk/'lib64')+':'+ENV.get('LD_LIBRARY_PATH',''))
  backends={};failures=[]
  for backend,source in [('cgbn','root_cuda.cu'),('cupqc','root_cupqc.cu')]:
   passed=True
   for tpi in (4,8,16,32):
    binary=E/(('root' if backend=='cgbn' else 'cupqc')+f'-tpi{tpi}')
    cmd=['nvcc','-O3','-std=c++17','-arch=sm_86',f'-DROOT_TPI={tpi}']
    if backend=='cgbn':cmd += ['-I'+str(E/'CGBN/include'),P/source,'-o',binary]
    else:cmd += ['-dlto','-DROOT_SM=860','-I'+str(sdk/'include/cupqc'),'-I'+str(sdk/'include'),'-L'+str(sdk/'lib'),'-L'+str(sdk/'lib64'),P/source,'-lcupqc-bigint','-o',binary]
    code=run(f'{backend}-build-tpi{tpi}',cmd,env=env)
    if code:
     failures.append(dict(backend=backend,phase='build',tpi=tpi,returncode=code));passed=False;break
    code=run(f'{backend}-correctness-tpi{tpi}',[PY,P/'gpu_check.py','--binary',binary,'--count','256','--output',E/'correctness'/f'{backend}-tpi{tpi}'],env=env)
    if code:
     failures.append(dict(backend=backend,phase='exact-certificate',tpi=tpi,returncode=code));passed=False;break
   if passed:reject_inputs(E/(('root' if backend=='cgbn' else 'cupqc')+'-tpi8'),backend)
   backends[backend]=dict(status='passed' if passed else 'failed',correctness_before_timing=True)
   save(E/'CORRECTNESS.json',dict(backends=backends,failures=failures))
  if failures:
   save(E/'SUMMARY.json',dict(status='blocked_before_timing',backends=backends,errors=failures,timing_sweep_started=False,production_restarted=False));return 2
  # Only after both independent GPU/GMP correctness gates pass, execute Dot's
  # published sweep unchanged, with the already verified local dependencies.
  save(E/'CORRECTNESS.json',dict(status='both_gpu_backends_passed',backends=backends,failures=[],completed_epoch=time.time()))
  code=run('published-timing-sweep',['bash',P/'run.sh',E],env=env,timeout=3600)
  save(E/'RUN_STATUS.json',dict(status='passed' if code==0 else 'failed_during_timing',returncode=code,correctness_before_timing=True,source_commit=COMMIT,started_epoch=START,finished_epoch=time.time(),production_restarted=False))
  return code
 finally:lease.close()
if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception as exc:
  save(E/'RUN_STATUS.json',dict(status='failed',error=repr(exc),source_commit=COMMIT,production_restarted=False,finished_epoch=time.time()));traceback.print_exc();raise
