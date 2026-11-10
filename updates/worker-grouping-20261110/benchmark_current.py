#!/usr/bin/env python3
"""Bounded TEST_ONLY 4/8 current-cursor benchmark using the previously tested harness."""
import argparse,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
from plan_update import choose,digest

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--harness',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--host',required=True,choices=['ada','boole','cabbage']);p.add_argument('--out',required=True);a=p.parse_args()
 root=Path(a.harness).resolve();cp=json.loads(Path(a.checkpoint).read_text());first=cp['next_patch']
 if first<1 or first+32768>cp['window']['last']:raise SystemExit('Need full current-cursor sample inside claim; otherwise retain group4')
 out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=False)
 py=root/'venv/bin/python';end=time.monotonic()+1200
 def idle():
  until=min(end,time.monotonic()+120)
  while True:
   r=subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],capture_output=True,text=True,check=True)
   if r.stdout.strip():raise RuntimeError('GPU busy; no concurrent production/testing permitted')
   if os.getloadavg()[0]<=4:return
   if time.monotonic()>=until:raise RuntimeError('Load guard expired; do not weaken it')
   time.sleep(5)
 for name,h in json.loads((root/'experiment-manifest.json').read_text())['worker_files'].items():
  if digest(root/'worker'/name)!=h:raise RuntimeError('Harness source changed: '+name)
 idle();env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 def run(cmd,label):
  with (out/(label+'.stdout')).open('w') as o,(out/(label+'.stderr')).open('w') as e:
   proc=subprocess.Popen(cmd,env=env,stdout=o,stderr=e,start_new_session=True)
   try:
    code=proc.wait(timeout=min(120,max(1,end-time.monotonic())))
    if code:raise RuntimeError(label+' exited '+str(code))
   except BaseException:
    try:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
    except ProcessLookupError:pass
    raise
 run([str(py),str(root/'controls.py')],'controls')
 rows=[]
 for repeat in range(3):
  for g in ((4,8) if repeat%2==0 else (8,4)):
   idle()
   if time.monotonic()>=end:raise TimeoutError('Finite budget exceeded')
   label=f'g{g}-r{repeat}';folder=out/label
   run([str(py),str(root/'trial_groups.py'),'--variant','cache_buffer8','--workers','16','--first',str(first),'--patches','32768','--group-limit',str(g),'--map-chunksize',str(16//g),'--output',str(folder)],label)
   r=json.loads((folder/'result.json').read_text());r.update(repeat=repeat,region='current');rows.append(r)
   (out/'samples.json').write_text(json.dumps(rows,indent=2)+'\n')
 decision=choose(rows,first,cp['identity']['source_identity'],a.host,a.host)
 receipt=dict(measured_host=a.host,source_identity=cp['identity']['source_identity'],parent_checkpoint_sha256=digest(a.checkpoint),samples_file='samples.json',samples_sha256=digest(out/'samples.json'),tested_harness_manifest_sha256=digest(root/'experiment-manifest.json'),production_coverage=False,decision=decision)
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
