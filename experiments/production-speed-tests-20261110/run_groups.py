"""Finite isolated group benchmark. No production state is read or written."""
import argparse,hashlib,json,os,signal,statistics,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REGIONS={'ada':4564955776,'cabbage':2572492928,'dense':9562500096}

def main():
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=1200);p.add_argument('--repeats',type=int,default=3);p.add_argument('--patches',type=int,default=32768);p.add_argument('--region',choices=REGIONS);a=p.parse_args()
 if not 1<=a.seconds<=3600 or not 1<=a.repeats<=5 or not 256<=a.patches<=32768 or a.patches%256:raise SystemExit('Invalid bounded configuration')
 for name,digest in json.loads((ROOT/'experiment-manifest.json').read_text())['worker_files'].items():
  if hashlib.sha256((ROOT/'worker'/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Manifest mismatch: '+name)
 if len(os.sched_getaffinity(0))<16:raise SystemExit('Need 16 available logical CPUs')
 out=ROOT/('results-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()));out.mkdir()
 def idle():
  r=subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],capture_output=True,text=True,check=True)
  if r.stdout.strip():raise RuntimeError('GPU compute process present: '+r.stdout)
  if os.getloadavg()[0]>4:raise RuntimeError('Load guard: CPU load >4; retry on idle machine')
 idle();(out/'hardware.txt').write_text(subprocess.check_output(['nvidia-smi'],text=True)+subprocess.check_output(['uname','-a'],text=True))
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 # This control proves nonempty hits against independent brute force and GMP.
 subprocess.run([sys.executable,str(ROOT/'controls.py')],env=env,check=True,timeout=120,stdout=(out/'controls.json').open('w'))
 deadline=time.monotonic()+a.seconds;rows=[];same={};hits={}
 for repeat in range(a.repeats):
  for region,first in REGIONS.items():
   if a.region and region!=a.region:continue
   order=(4,8,16);order=order[repeat%3:]+order[:repeat%3]
   for group in order:
    idle();remaining=deadline-time.monotonic()
    if remaining<1:raise TimeoutError('Overall finite budget exhausted')
    name=f'{region}-g{group}-r{repeat}';folder=out/name
    cmd=[sys.executable,str(ROOT/'trial_groups.py'),'--variant','cache_buffer8','--workers','16','--first',str(first),'--patches',str(a.patches),'--group-limit',str(group),'--map-chunksize',str(16//group),'--output',str(folder)]
    with (out/(name+'.stdout')).open('w') as stdout,(out/(name+'.stderr')).open('w') as stderr:
     proc=subprocess.Popen(cmd,env=env,stdout=stdout,stderr=stderr,start_new_session=True)
     try:
      code=proc.wait(timeout=min(120,remaining))
      if code:raise RuntimeError(f'{name}: exit {code}')
     except BaseException:
      try:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
      except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
      except ProcessLookupError:pass
      raise
    r=json.loads((folder/'result.json').read_text());key=(region,group)
    sig=(r['signatures_sha256'],r['points'],r['physical_tasks'])
    if key in same and same[key]!=sig:raise RuntimeError('Repeat geometry/count mismatch')
    same[key]=sig
    if region in hits and hits[region]!=r['hits']:raise RuntimeError('Cross-group hit mismatch')
    hits[region]=r['hits'];r.update(region=region,repeat=repeat);rows.append(r)
    (out/'samples.json').write_text(json.dumps(rows,indent=2)+'\n')
 summary={f'{reg}/g{g}':statistics.median(r['patches_per_second'] for r in rows if r['region']==reg and r['group_limit']==g) for reg in REGIONS if any(r['region']==reg for r in rows) for g in (4,8,16)}
 (out/'READY.json').write_text(json.dumps({'status':'passed','production_coverage':False,'median_original_cells_per_second':summary,'samples':len(rows)},indent=2)+'\n')
 print(out)
if __name__=='__main__':main()
