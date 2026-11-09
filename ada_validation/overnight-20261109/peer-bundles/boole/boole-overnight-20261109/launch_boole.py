"""Start the frozen, validated Boole continuation and independent final cleanup."""
import hashlib,json,os,shutil,sys,tarfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path.insert(0,str(W))
import policy
from durable_mirror import atomic
from validate_boole_services import launch,unit,wait_for,PYTHON

def main():
 config_path=W/'production-config.json';c=policy.load_config(config_path)
 validation=json.loads((ROOT/'runtime-validation.json').read_bytes())
 policy.require(validation['status']=='passed' and validation['manifest_sha256']==c['manifest_sha256'],'Actual service validation not current')
 policy.require(time.time()<c['stop_epoch']-60,'Deadline too near for startup')
 return_dir=Path('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole')
 policy.require(not (return_dir/'READY_FOR_PUBLISHER.json').exists(),'A production admission request already exists')
 stage=return_dir/'frozen-runtime';stage.mkdir(mode=0o700,parents=True,exist_ok=False)
 # Keep all per-host code and configuration available for Ada to review.
 with tarfile.open(stage/'source.tar.gz','w:gz') as tar:
  for p in sorted(W.rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:tar.add(p,arcname='worker/'+str(p.relative_to(W)),recursive=False)
  for p in sorted(ROOT.glob('*.py')):tar.add(p,arcname=p.name,recursive=False)
 for source,name in [(config_path,'configuration.json'),(W/'release-manifest.json','source-manifest.json'),
   (ROOT/'runtime-validation.json','runtime-validation.json'),(ROOT/'parent-archive-receipt.json','parent-archive-receipt.json'),
   (ROOT/'parent-audit.json','parent-audit.json'),(ROOT/'FROZEN.json','FROZEN.json')]:shutil.copy2(source,stage/name)
 atomic(stage/'SHA256.json',{p.name:policy.digest(p) for p in stage.iterdir() if p.is_file()})
 folder=ROOT/'production-service';folder.mkdir(mode=0o700)
 commands,cleanup,timer=launch(c,config_path,folder,cleanup_extension=1800)
 def started():
  p=Path(c['output'])/'checkpoint.json'
  return p.exists() and json.loads(p.read_bytes())['chunks']>0
 wait_for(started,90,'Production did not commit: inspect '+str(folder))
 cp=json.loads((Path(c['output'])/'checkpoint.json').read_bytes())
 report=dict(status='running',run_id=c['run_id'],config_sha256=policy.digest(config_path),manifest_sha256=c['manifest_sha256'],
  local_next_patch=cp['next_patch'],local_output=c['output'],replica_output=c['replica_output'],group_limit=c['group_limit'],
  stop_local=c['stop_local'],service=unit(c['service_name']),timer=unit(timer),final_copy=unit(cleanup),commands=commands)
 policy.require(all(report[key]['ActiveState']=='active' for key in ('service','timer','final_copy')),'Worker/timer/final-copy service not active')
 atomic(ROOT/'RUN_STATUS.json',report);atomic(return_dir/'RUN_STATUS.json',report)
 print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
