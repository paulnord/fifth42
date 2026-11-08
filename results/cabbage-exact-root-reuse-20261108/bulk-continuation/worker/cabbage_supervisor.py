"""Console-independent Cabbage guard. One host GPU lease, bounded child lifetime."""
import argparse,ctypes,fcntl,json,os,signal,subprocess,sys,time
from pathlib import Path
import policy
ROOT=Path(__file__).resolve().parent

def parent_guard():
 libc=ctypes.CDLL(None,use_errno=True)
 if libc.prctl(1,signal.SIGKILL)!=0:raise OSError(ctypes.get_errno())
 if os.getppid()==1:os.kill(os.getpid(),signal.SIGKILL)
def gpu_pids():
 return [int(x) for x in subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True,timeout=5).split()]
def main():
 a=argparse.ArgumentParser();a.add_argument('--config',required=True);o=a.parse_args();c=policy.load_config(o.config);config_hash=policy.digest(o.config)
 stopping=[False];signal.signal(signal.SIGTERM,lambda *_:stopping.__setitem__(0,True));signal.signal(signal.SIGINT,lambda *_:stopping.__setitem__(0,True))
 child=None;lock=None;started=time.monotonic();report=dict(status='starting',error=None,config_sha256=config_hash,TEST_ONLY=c.get('TEST_ONLY',False),leases_released=False)
 report_path=Path(c['output']).parent/'supervisor.json'
 def save():
  report_path.write_text(json.dumps(dict(report,updated_utc=policy.utc(),load_average=os.getloadavg()),indent=2)+'\n')
 try:
  lock=Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock').open('a+');fcntl.lockf(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  policy.require(not gpu_pids(),'GPU already occupied')
  policy.require(os.getloadavg()[0]<c['prep_load_ceiling'],'CPU not idle enough to begin')
  mem={k:int(v.split()[0]) for k,v in (line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())};policy.require(mem['MemAvailable']>=4*1024**2,'Insufficient available memory')
  env=dict(os.environ,CUDA_VISIBLE_DEVICES='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
  child=subprocess.Popen([sys.executable,'-B','-u',str(ROOT/'packed_worker.py'),'--config',o.config],env=env,start_new_session=True,preexec_fn=parent_guard)
  report.update(status='running',worker_pid=child.pid);save();last_check=0;soft=None
  while child.poll() is None:
   if stopping[0] or time.time()>=c['stop_epoch']-8:
    if soft is None:
     report['stop_trigger']='signal' if stopping[0] else 'absolute_deadline'
     child.send_signal(signal.SIGTERM);soft=time.monotonic();save()
    elif time.monotonic()-soft>5:raise TimeoutError('Worker exceeded graceful stop allowance')
   policy.require(time.time()<c['stop_epoch'],'Absolute hard deadline')
   policy.require(os.getloadavg()[0]<=c['running_load_limit'],'Running load exceeded')
   if time.monotonic()-last_check>=5:
    policy.require(policy.digest(o.config)==config_hash,'Configuration changed');policy.verify_sources(c);policy.validate_ledger(c);policy.validate_parent(c,full=False);policy.validate_output(c)
    for pid in gpu_pids():
     try:policy.require(os.getpgid(pid)==child.pid,'Unrelated GPU owner')
     except ProcessLookupError:pass
    last_check=time.monotonic();save()
   time.sleep(.2)
  report.update(status='finished' if child.returncode==0 else 'failed',worker_exit_code=child.returncode)
  policy.require(child.returncode==0,'Worker failed')
  return 0
 except BaseException as e:
  report.update(status='failed',error=repr(e));raise
 finally:
  signal.signal(signal.SIGTERM,signal.SIG_IGN)
  if child:
   if child.poll() is None:
    child.send_signal(signal.SIGTERM)
    try:child.wait(timeout=5)
    except subprocess.TimeoutExpired:pass
   try:os.killpg(child.pid,signal.SIGTERM)
   except ProcessLookupError:pass
   time.sleep(.2)
   try:os.killpg(child.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   child.wait(timeout=3)
  if child:
   until=min(c['stop_epoch'],time.time()+2)
   while True:
    alive=[]
    for proc in Path('/proc').iterdir():
     if not proc.name.isdigit():continue
     try:
      fields=(proc/'stat').read_text().rsplit(')',1)[1].split()
      if int(fields[2])==child.pid and fields[0] not in ('Z','X'):alive.append(int(proc.name))
     except (FileNotFoundError,ProcessLookupError,PermissionError):pass
    if not alive:break
    if time.time()>=until:raise RuntimeError('Owned processes remained after cleanup: '+str(alive))
    time.sleep(.05)
   policy.require(not gpu_pids(),'GPU process remains after cleanup')
   report['all_owned_processes_exited_utc']=policy.utc()
   policy.require(time.time()<c['stop_epoch'],'Process cleanup exceeded hard deadline')
  if lock:lock.close()
  report['leases_released']=True;report['wall_seconds']=time.monotonic()-started;save()
if __name__=='__main__':raise SystemExit(main())
