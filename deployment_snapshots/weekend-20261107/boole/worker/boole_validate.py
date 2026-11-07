"""Bounded actual-worker validation on Boole; only TEST_ONLY ledger claims."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,signal,statistics,subprocess,sys,time
import policy,ada_export_store as store
from gpu_validation import audit
ROOT=Path(__file__).resolve().parent
VALID=ROOT/'boole-validation-v4';STAMP=datetime.now(timezone.utc).strftime('%H%M%S')
LEDGER=Path('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/boole-validation')/STAMP

def config(name,start,geometry,stop_seconds=90,chunks=32):
 coverage=ROOT/'boole-final-coverage.json';manifest=ROOT/'boole-release-manifest.json'
 ledger=LEDGER/name;s=store.Store(ledger)
 c=dict(TEST_ONLY=True,run_id='boole-test-'+name,parent_run='fresh disjoint interval; no inherited completed patches',parent_selected_patches=0,
 initial_patch=start,range_end=start+(8192 if chunks else 1000000),shell_lo=100000000001,shell_hi=200000000000,width=8,bits=222,cap=42,
 workers=16,physical_cpus=list(range(16)),chunk_patches=256,backend='gpu',gmp_audit_period=128,
 stop_epoch=min(1794236400,time.time()+stop_seconds),automatic_resume=False,publication=False,
 manifest_sha256=policy.digest(manifest),geometry_policy=geometry,prep_load_ceiling=17.,running_load_limit=20.,
 minimum_free_disk_bytes=8*1024**3,journal_limit_bytes=32*1024**3,test_chunk_limit=chunks,
 ledger_root=str(ledger),ledger_job='test-'+name,ledger_device=s.device,coverage_file=str(coverage),coverage_sha256=policy.digest(coverage))
 c['stop_local']=datetime.fromtimestamp(c['stop_epoch'],timezone.utc).isoformat();c['output']=str(ledger/'jobs'/c['ledger_job']/'run')
 claim=s.reserve(c['ledger_job'],start,c['range_end'],c['manifest_sha256'],dict(sha256=c['coverage_sha256'],manifest=json.loads(coverage.read_text())))
 c['ledger_claim_sha256']=claim['sha256'];path=VALID/(name+'.json');path.write_text(json.dumps(c,indent=2)+'\n');return c,path

def launch(name,start,geometry,seconds=90,chunks=32,signal_test=False):
 c,path=config(name,start,geometry,seconds,chunks)
 with (VALID/(name+'.stdout')).open('x') as stdout,(VALID/(name+'.stderr')).open('x') as stderr:
  p=subprocess.Popen([sys.executable,'-B',str(ROOT/'boole_supervisor.py'),'--config',str(path)],stdout=stdout,stderr=stderr,start_new_session=True)
  try:
   if signal_test:
    checkpoint=Path(c['output'])/'checkpoint.json';end=time.monotonic()+45
    while not checkpoint.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.1)
    policy.require(checkpoint.exists(),'Signal test never reached running journal')
    p.send_signal(signal.SIGTERM)
   p.wait(timeout=seconds+15)
  finally:
   if p.poll() is None:
    os.killpg(p.pid,signal.SIGTERM)
    try:p.wait(timeout=8)
    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
  policy.require(p.returncode==0,'Case failed '+name+'; see '+str(VALID/(name+'.stderr')))
 checked=audit(Path(c['output']),c)
 supervisor=json.loads((Path(c['output']).parent/'supervisor.json').read_text());policy.require(supervisor['leases_released'],'Leases not released')
 policy.require(datetime.fromisoformat(supervisor['all_owned_processes_exited_utc']).timestamp()<c['stop_epoch'],'All-process exit was not verified before hard deadline')
 if chunks:policy.require(checked['status']['status']=='completed_test' and checked['status']['chunks']==chunks,'Finite trial incomplete')
 else:policy.require(checked['status']['status']=='stopped','Stop did not preserve a clean journal')
 return c,checked

def main():
 VALID.mkdir(exist_ok=False)
 results=[]
 for i,start in enumerate([3000000000,3375000000,3750000000-8192]):
  pair=[]
  for geometry in (('baseline','adaptive') if i%2==0 else ('adaptive','baseline')):
   name=f'{i}-{geometry}';c,a=launch(name,start,geometry)
   policy.require(a['audits']>=1,'Independent GMP audit absent')
   row=dict(case=name,first=start,last=start+8192,geometry=geometry,rate=a['status']['patches_per_second'],chunks=a['status']['chunks'],hits=a['hits'],points=a['checkpoint']['points'],independent_audits=a['audits']);results.append(row);pair.append(a['hits']);print(json.dumps(row),flush=True)
  policy.require(pair[0]==pair[1],'Exact hit mismatch')
 c,a=launch('signal',3375000000,'adaptive',90,None,True);policy.require(a['status']['reason']=='Stop requested','Signal reason incorrect')
 c,a=launch('deadline',3375000000,'adaptive',20,None)
 supervisor=json.loads((Path(c['output']).parent/'supervisor.json').read_text())
 policy.require(supervisor.get('stop_trigger')=='absolute_deadline' and a['status']['reason'] in ('Stop requested','Absolute deadline reached; final cleanup'),'Deadline stop not attributed correctly')
 policy.require(datetime.fromisoformat(supervisor['updated_utc']).timestamp()<c['stop_epoch'],'Cleanup exceeded hard deadline')
 med={p:statistics.median(r['rate'] for r in results if r['geometry']==p) for p in ['baseline','adaptive']}
 report=dict(status='PASS',TEST_ONLY=True,mathematical_production_coverage=False,source_manifest_sha256=policy.digest(ROOT/'boole-release-manifest.json'),trials=results,median_rates=med,speedup=med['adaptive']/med['baseline'],signal_stop=True,deadline_stop=True,ledger=str(LEDGER),production_claims_created=False,production_launched=False,limitations=['Test-only exact enumeration; no coverage allocated to production.','Publisher and production launch configuration are separate readiness gates.'])
 (ROOT/'BOOLE_VALIDATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
