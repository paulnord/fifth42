"""Balanced bounded whole-pipeline comparisons, isolated scratch journals."""
import argparse,hashlib,json,os,signal,statistics,subprocess,sys,time
from pathlib import Path
from run_bounded import run
ROOT=Path(__file__).resolve().parent
REGIONS={'ada':(4564955776,4),'cabbage':(2572492928,8),'dense':(9562500096,4)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--repeats',type=int,default=3);p.add_argument('--patches',type=int,default=32768);p.add_argument('--seconds',type=int,default=1200);p.add_argument('--region',choices=REGIONS);a=p.parse_args()
 assert 1<=a.repeats<=3 and 256<=a.patches<=32768 and a.patches%256==0 and 1<=a.seconds<=2400
 for name,digest in json.loads((ROOT/'experiment-manifest.json').read_text())['worker_files'].items():
  assert hashlib.sha256((ROOT/'worker'/name).read_bytes()).hexdigest()==digest,name
 a.output.mkdir(parents=True,exist_ok=False);deadline=time.monotonic()+a.seconds
 rows=[];same={};hits={};modes=[('cpu',1),('cpu',16),('gpu',16)]
 os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 for rep in range(a.repeats):
  for region,(first,group) in REGIONS.items():
   if a.region and region!=a.region:continue
   for backend,batch in modes[rep%3:]+modes[:rep%3]:
    assert time.monotonic()<deadline,'Overall finite deadline exhausted'
    name=f'{region}-{backend}-w{batch}-r{rep}';folder=a.output/name
    cmd=[sys.executable,str(ROOT/'trial_preparation.py'),'--variant','cache_buffer8','--workers','16','--first',str(first),'--patches',str(a.patches),'--group-limit',str(group),'--map-chunksize',str(16//group),'--preparation-backend',backend,'--window-batch',str(batch),'--output',str(folder)]
    run(cmd,a.output/(name+'.log'),min(120,int(deadline-time.monotonic())))
    r=json.loads((folder/'result.json').read_text());key=(region,backend,batch)
    sig=(r['signatures_sha256'],r['points'],r['physical_tasks'])
    if key in same:assert same[key]==sig,('Repeated geometry/count mismatch',key)
    same[key]=sig
    if region in hits:assert hits[region]==r['hits'],('Cross-mode hits differ',region)
    hits[region]=r['hits'];r.update(region=region,repeat=rep);rows.append(r)
    (a.output/'samples.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(name,round(r['patches_per_second'],2),'cells/s',flush=True)
 summary={f'{reg}/{backend}/w{batch}':statistics.median(r['patches_per_second'] for r in rows if r['region']==reg and r['preparation_backend']==backend and r['preparation_window_batch']==batch) for reg in REGIONS if any(r['region']==reg for r in rows) for backend,batch in modes}
 (a.output/'SUMMARY.json').write_text(json.dumps(dict(status='passed',TEST_ONLY=True,production_coverage=False,median_cells_per_second=summary,samples=len(rows)),indent=2)+'\n')
if __name__=='__main__':main()
