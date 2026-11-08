from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,signal,subprocess,sys,time
r=Path(__file__).resolve().parent;w=r/'cabbage-runtime'
sys.path.insert(0,str(w));import policy,ada_export_store as store
from gpu_validation import audit
out=r/'runtime-tests';out.mkdir(exist_ok=False)
ledger_parent=Path('/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk')
assert not ledger_parent.exists(),'Use fresh runtime test namespace'
manifest=w/'cabbage-release-manifest.json';meta=w/'admission-plan.json'
results=[]
def launch(name,first,chunks=2,seconds=90,signal_test=False):
 s=store.Store(ledger_parent/name)
 c=dict(TEST_ONLY=True,run_id='cabbage-test-'+name,parent_run='fresh TEST_ONLY allocation; no inherited coverage',parent_selected_patches=0,initial_patch=first,range_end=first+(512 if chunks else 1000000),shell_lo=100000000001,shell_hi=200000000000,width=8,bits=222,cap=42,workers=16,physical_cpus=list(range(16)),chunk_patches=256,backend='gpu',gmp_audit_period=128,stop_epoch=min(1794236400,time.time()+seconds),automatic_resume=False,publication=False,manifest_sha256=policy.digest(manifest),geometry_policy='adaptive',prep_load_ceiling=17.,running_load_limit=20.,minimum_free_disk_bytes=8*1024**3,journal_limit_bytes=2*1024**3,test_chunk_limit=chunks,ledger_root=str(s.root),ledger_job='test-'+name,ledger_device=s.device,coverage_file=str(meta),coverage_sha256=policy.digest(meta))
 c['stop_local']=datetime.fromtimestamp(c['stop_epoch'],timezone.utc).isoformat();c['output']=str(s.root/'jobs'/c['ledger_job']/'run')
 claim=s.reserve(c['ledger_job'],c['initial_patch'],c['range_end'],c['manifest_sha256'],dict(sha256=c['coverage_sha256'],manifest=json.loads(meta.read_text())))
 c['ledger_claim_sha256']=claim['sha256'];path=out/(name+'.json');path.write_text(json.dumps(c,indent=2)+'\n')
 with (out/(name+'.stdout.txt')).open('x') as stdout,(out/(name+'.stderr.txt')).open('x') as stderr:
  p=subprocess.Popen(['nice','-n','19',sys.executable,'-B',str(w/'cabbage_supervisor.py'),'--config',str(path)],stdout=stdout,stderr=stderr,start_new_session=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  try:
   if signal_test:
    checkpoint=Path(c['output'])/'checkpoint.json';end=time.monotonic()+30
    while not checkpoint.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.05)
    assert checkpoint.exists(),'Signal test never committed'
    p.send_signal(signal.SIGTERM)
   p.wait(timeout=seconds+10)
  finally:
   if p.poll() is None:
    os.killpg(p.pid,signal.SIGTERM)
    try:p.wait(timeout=6)
    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
 assert p.returncode==0,(name,'see stderr')
 checked=audit(Path(c['output']),c)
 status=checked['status'];sup=json.loads((Path(c['output']).parent/'supervisor.json').read_text())
 assert sup['leases_released'] and sup['error'] is None
 assert datetime.fromisoformat(sup['all_owned_processes_exited_utc']).timestamp()<c['stop_epoch']
 assert checked['audits']>=1 and checked['checkpoint']['chunks']>=1
 if chunks:assert status['status']=='completed_test' and status['chunks']==chunks
 else:assert status['status']=='stopped'
 if signal_test:assert status['reason']=='Stop requested' and sup['stop_trigger']=='signal'
 if name=='deadline':assert sup['stop_trigger']=='absolute_deadline' and ('Absolute deadline' in status['reason'] or status['reason']=='Stop requested')
 controls=json.loads((Path(c['output'])/'controls.json').read_text());assert controls['status']=='passed' and all(case['hits'] for case in controls['cases'])
 row=dict(name=name,config_sha256=policy.digest(path),manifest_sha256=c['manifest_sha256'],TEST_ONLY=True,first=first,last=checked['checkpoint']['next_patch'],chunks=status['chunks'],points=checked['checkpoint']['points'],exact_hits=checked['hits'],gmp_audits=checked['audits'],reason=status['reason'],controls=controls,supervisor=sup,production_coverage=False)
 (out/(name+'-result.json')).write_text(json.dumps(row,indent=2)+'\n');results.append(row);print(json.dumps({k:row[k] for k in ('name','first','last','chunks','points','gmp_audits','reason')}),flush=True)
for name,first in [('start',2250000000),('middle',2625000000),('end',3000000000-512)]:launch(name,first)
launch('signal',2625000000,None,60,True)
launch('deadline',2625000000,None,16)
# Policy fail-closed checks perform no production-file access: validation rejects
# each edit before source/ledger verification.
base=json.loads((out/'start.json').read_text())
for key,value in [('journal_limit_bytes',2*1024**3+1),('automatic_resume',True),('geometry_policy','float'),('range_end',3000000001),('physical_cpus',[0]*16),('stop_epoch',time.time()-1)]:
 edited=dict(base,**{key:value});path=out/('rejected-'+key+'.json');path.write_text(json.dumps(edited))
 try:policy.load_config(path);raise AssertionError('Invalid policy accepted '+key)
 except RuntimeError:pass
report=dict(status='PASS',TEST_ONLY=True,production_coverage=False,production_claims_created=False,production_launched=False,manifest_sha256=policy.digest(manifest),adapter_sha256=policy.digest(w/'ada_export_store.py'),workers=16,physical_cpus=list(range(16)),journal_cap_bytes=2*1024**3,proposed_interval=[2250000000,3000000000],results=results,signal_stop_passed=True,deadline_cleanup_passed=True,process_ownership_cleanup_passed=True,policy_rejections_passed=True,limitations=['Actual Cabbage worker/supervisor with fresh TEST_ONLY NFS claims.','Cross-host protocol results and production admission/publisher remain separate gates.'])
(r/'runtime-acceptance-results.json').write_text(json.dumps(report,indent=2)+'\n')
print('Actual staged runtime acceptance passed.',flush=True)
