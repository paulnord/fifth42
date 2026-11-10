"""Identity-bound publication evidence and one collector for the stable delegated share."""
import hashlib,json,math,shutil,subprocess,sys,tarfile,time
from pathlib import Path
SHARE=Path('/mnt/nfs_share/boole-delegated-publishing-20261109')

def archive(root,destination,ctl):
 w=root/'worker';manifest=json.loads((w/'release-manifest.json').read_bytes())
 with tarfile.open(destination,'w:gz') as tar:
  for name in manifest['files']:tar.add(w/name,arcname='worker/'+name,recursive=False)
  for name in ('release-manifest.json','production-config.json','base-config.json'):tar.add(w/name,arcname='worker/'+name,recursive=False)
  for path in manifest.get('external_files',{}):tar.add(path,arcname=Path(path).name,recursive=False)
  tar.add(w/'production-config.json',arcname='production-config.json',recursive=False)
 with tarfile.open(destination,'r:gz') as tar:
  for name,expected in manifest['files'].items():ctl.require(hashlib.sha256(tar.extractfile('worker/'+name).read()).hexdigest()==expected,'Archived runtime source changed')
  ctl.require(tar.extractfile('production-config.json').read()==(w/'production-config.json').read_bytes(),'Archived configuration differs')
 return ctl.sha(destination)

def start(stage,c,ctl):
 root=Path(stage['root']);name=c['run_id'];SHARE.mkdir(mode=0o700,parents=True,exist_ok=True)
 # Stop the previous stable-share collector only after its verified stage completion.
 spec_path=SHARE/'active-publication-spec.json'
 if spec_path.exists():
  prior=json.loads(spec_path.read_bytes())['run_id']
  if prior!=name:subprocess.run(['systemctl','--user','stop',prior+'-collector.service'],check=True,capture_output=True,text=True,timeout=15)
 evidence=SHARE/'runs'/name;evidence.mkdir(mode=0o700,parents=True,exist_ok=False)
 files={'configuration.json':Path(stage['config']),'source-manifest.json':Path(c['manifest']),'parent-audit.json':Path(c['parent_audit_file']),
        'original-claim.json':Path(c['origin_claim_file']),'runtime-validation.json':root/'runtime-validation.json'}
 for dest,source in files.items():shutil.copy2(source,evidence/dest)
 archive_hash=archive(root,evidence/'source.tar.gz',ctl)
 hashes={p.name:ctl.sha(p) for p in evidence.iterdir() if p.is_file()}
 fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=c['manifest_sha256'],config=c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 publication=dict(run_id=name,manifest_sha256=c['manifest_sha256'],config_sha256=stage['config_sha256'],source_identity=fingerprint,ledger_claim_sha256=c['ledger_claim_sha256'],evidence=hashes)
 folder=root/('controller-reporter-'+name);folder.mkdir(mode=0o700)
 shutil.copy2(root/'collector.py',folder/'collector.py')
 ctl.atomic(folder/'collector-settings.json',dict(host='boole',config=stage['config'],manifest=c['manifest'],config_sha256=stage['config_sha256'],manifest_sha256=c['manifest_sha256'],supervisor_report=str(Path(c['output']).parent/'supervisor.json'),output=str(SHARE),stop_epoch=c['stop_epoch']))
 cmd=['systemd-run','--user','--unit='+name+'-collector','--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077',
 '--property=RuntimeMaxSec='+str(max(1,math.floor(c['stop_epoch']+1800-time.time()))),'--property=StandardOutput=append:'+str(folder/'stdout.log'),'--property=StandardError=append:'+str(folder/'stderr.log'),sys.executable,'-B','-u',str(folder/'collector.py')]
 subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=15)
 until=time.monotonic()+100
 while time.monotonic()<until:
  p=SHARE/'status.json'
  if p.exists():
   row=json.loads(p.read_bytes())
   if row.get('run_id')==name and row['phase']=='running' and row.get('checkpoint') and not row['alerts']:
    ctl.require(row['config_sha256']==stage['config_sha256'] and row['manifest_sha256']==c['manifest_sha256'] and row['source_identity']==fingerprint,'Stable collector identity mismatch')
    cp=row['checkpoint'];receipt=row['replica']
    ctl.require(cp['identity']==receipt['identity']==dict(trial=name,source_identity=fingerprint),'First verified replica identity mismatch')
    break
  ctl.require(ctl.unit(c['service_name'])['ActiveState']=='active','Production stopped before first verified replica')
  time.sleep(1)
 else:raise TimeoutError('Stable collector never observed a healthy verified replica')
 ctl.atomic(SHARE/'publication-spec.json',publication)
 ctl.atomic(SHARE/'active-publication-spec.json',dict(run_id=name,config_sha256=stage['config_sha256'],manifest_sha256=c['manifest_sha256'],source_archive_sha256=archive_hash,evidence_sha256=hashes))
 ctl.atomic(root/'PUBLICATION_READY.json',dict(status='publisher_requested',share=str(SHARE),source_archive_sha256=archive_hash,evidence_sha256=hashes))
 return str(SHARE)
