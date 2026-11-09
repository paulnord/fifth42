"""Prepare and start a peer collector; put a verifiable publisher request on NFS."""
import argparse,hashlib,json,math,os
from pathlib import Path
import shutil,subprocess,time
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,row):
    path.write_text(json.dumps(row,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('config','manifest','supervisor','runtime-validation','reporter-root'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--python',required=True)
    args=parser.parse_args();host=os.uname().nodename.split('.')[0]
    assert host in ('boole','cabbage')
    cfg=json.loads(args.config.read_bytes());assert cfg['TEST_ONLY'] is False
    assert cfg['run_id']==host+'-overnight-20261109' and cfg['stop_epoch']==1794351600
    assert sha(args.manifest)==cfg['manifest_sha256'] and time.time()<cfg['stop_epoch']
    runtime=json.loads(args.runtime_validation.read_bytes());assert runtime['status']=='passed'
    share=Path('/mnt/nfs_share')/(host+'-overnight-publishing-20261109');evidence=share/'evidence'
    evidence.mkdir(mode=0o700,parents=True,exist_ok=True);args.reporter_root.mkdir(mode=0o700,parents=True,exist_ok=False)
    sources={'configuration.json':args.config,'source-manifest.json':args.manifest,
      'original-claim.json':Path(cfg['origin_claim_file']),'parent-audit.json':Path(cfg['parent_audit_file']),
      'parent-archive-receipt.json':Path(cfg['parent_archive_receipt']),'runtime-validation.json':args.runtime_validation}
    hashes={}
    for name,path in sources.items():
        shutil.copy2(path,evidence/name);hashes[name]=sha(evidence/name)
    fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=cfg['manifest_sha256'],config=cfg),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    spec=dict(run_id=cfg['run_id'],manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(args.config),source_identity=fingerprint,ledger_claim_sha256=cfg['ledger_claim_sha256'],evidence=hashes)
    write(share/'publication-spec.json',spec)
    shutil.copy2(ROOT/'collector.py',args.reporter_root/'collector.py')
    write(args.reporter_root/'collector-settings.json',dict(host=host,config=str(args.config.resolve()),manifest=str(args.manifest.resolve()),config_sha256=sha(args.config),manifest_sha256=cfg['manifest_sha256'],supervisor_report=str(args.supervisor.resolve()),output=str(share),stop_epoch=cfg['stop_epoch']))
    unit=host+'-overnight-collector-20261109'
    cmd=['systemd-run','--user','--unit='+unit,'--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(math.floor(cfg['stop_epoch']+1800-time.time())),'--working-directory='+str(args.reporter_root),'--property=StandardOutput=append:'+str(args.reporter_root/'stdout.log'),'--property=StandardError=append:'+str(args.reporter_root/'stderr.log'),args.python,'-B','-u',str(args.reporter_root/'collector.py')]
    subprocess.run(cmd,check=True,timeout=15)
    until=time.monotonic()+90
    while time.monotonic()<until:
        if (share/'status.json').exists():
            row=json.loads((share/'status.json').read_bytes())
            if row['run_id']==cfg['run_id'] and row['phase']=='running' and row['checkpoint'] and not row['alerts']:break
        time.sleep(2)
    else:raise RuntimeError('Collector has not observed a clean running replicated checkpoint')
    ready=dict(host=host,run_id=cfg['run_id'],collector_share=str(share),config_sha256=sha(args.config),manifest_sha256=cfg['manifest_sha256'],source_identity=fingerprint,ledger_claim_sha256=cfg['ledger_claim_sha256'],stop_epoch=cfg['stop_epoch'],local_output=cfg['output'],replica_output=cfg['replica_output'],service_name=cfg['service_name'],deadline_service_name=cfg['deadline_service_name'],runtime_validation_sha256=sha(args.runtime_validation))
    dest=Path('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110')/host;dest.mkdir(mode=0o700,parents=True,exist_ok=True)
    write(dest/'READY_FOR_PUBLISHER.json',ready)
    print(json.dumps(dict(status='collector_running_publisher_requested',host=host,share=str(share)),indent=2))
if __name__=='__main__':main()
