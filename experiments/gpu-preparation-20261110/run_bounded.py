"""Exclusive finite experiments; never changes production state."""
import argparse,fcntl,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LOCK=Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock')
def run(command,output,timeout=120):
 output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 with LOCK.open('r+') as lease:
  fcntl.lockf(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
  deadline=time.monotonic()+30;guard_samples=[]
  while True:
   processes=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True).strip()
   assert not processes,('GPU compute owner present',processes)
   gpu=subprocess.check_output(['nvidia-smi','--query-gpu=utilization.gpu,memory.used','--format=csv,noheader,nounits'],text=True).strip()
   utilization,memory=map(int,gpu.split(','));guard_samples.append(dict(time=time.time(),utilization=utilization,memory_mib=memory))
   if utilization<=5 and memory<512:break
   if time.monotonic()>deadline:raise RuntimeError('GPU idle guard remained busy')
   time.sleep(1)
  # The one-minute load average includes our preceding finite test. Wait for it,
  # keeping the original <=4 threshold, rather than identifying it as another user.
  deadline=time.monotonic()+120
  while os.getloadavg()[0]>4:
   if time.monotonic()>deadline:raise RuntimeError('Load guard remained above4')
   time.sleep(2)
  before=dict(load=os.getloadavg(),gpu=gpu,gpu_guard_samples=guard_samples,time=time.time(),command=command)
  with output.open('w') as log:
   p=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
   try:p.wait(timeout=timeout)
   except BaseException:
    try:os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    except ProcessLookupError:pass
    output.with_suffix('.failure.json').write_text(json.dumps(dict(command=command,timeout=timeout,error='process interrupted or timed out',returncode=p.returncode),indent=2)+'\n')
    raise
  after=dict(returncode=p.returncode,elapsed=time.time()-before['time'],time=time.time())
  output.with_suffix('.metadata.json').write_text(json.dumps(dict(before=before,after=after),indent=2)+'\n')
  if p.returncode:raise RuntimeError(f'Failed {p.returncode}; see {output}')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--log',required=True);p.add_argument('--seconds',type=int,default=120);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args();run(a.command,a.log,a.seconds)
