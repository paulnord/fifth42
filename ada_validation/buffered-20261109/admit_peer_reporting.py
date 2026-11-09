"""Ada-only, read-only peer admission followed by a local status publisher."""
import argparse,errno,fcntl,hashlib,json,math,os
from pathlib import Path
import shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'worker'))
import audit_grouped
from durable_mirror import atomic
DEADLINE=1794265200
SHARED=Path('/mnt/nfs_share/fifth42-shared-20261107')
BULK=Path('/mnt/localstorage/pnord/fifth42-storage')
EXPECTED={
 'boole':('boole-precision-20261107T222232Z',3000000000,3750000000,'5ca9cd96357e7f0261e320ca42ded98a1affe2efc9cba379dec8bd0cea2e3342'),
 'cabbage':('cabbage-saved-root-20261108T222040Z',2250000000,3000000000,'364221db0023ea69fa18b47eb512e9e83362f6d598fc19c101e74b72f4f3d1c8')}

def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_bytes())
def stable(row):return json.dumps(row,sort_keys=True,separators=(',',':')).encode()
def owner_locked(path):
    with path.open('r+b') as stream:
        try:fcntl.lockf(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno in (errno.EACCES,errno.EAGAIN):return True
            raise
        fcntl.lockf(stream,fcntl.LOCK_UN);return False

def validate(host,ready):
    job,first,last,claim_hash=EXPECTED[host]
    share=Path('/mnt/nfs_share')/(host+'-buffered-publishing-20261109')
    require(ready['host']==host and ready['run_id']==host+'-buffered-20261109' and ready['collector_share']==str(share),'Wrong peer readiness identity')
    require(ready['stop_epoch']==DEADLINE,'Wrong peer deadline')
    spec=read(share/'publication-spec.json');evidence=share/'evidence'
    for name,digest in spec['evidence'].items():
        require(Path(name).name==name and sha(evidence/name)==digest,'Peer evidence hash changed: '+name)
    cfg=read(evidence/'configuration.json');manifest=read(evidence/'source-manifest.json')
    require(sha(evidence/'configuration.json')==ready['config_sha256'] and sha(evidence/'source-manifest.json')==ready['manifest_sha256']==cfg['manifest_sha256'],'Peer config/manifest hash changed')
    fingerprint=hashlib.sha256(stable(dict(manifest_sha256=cfg['manifest_sha256'],config=cfg))).hexdigest()
    for key,value in dict(run_id=cfg['run_id'],manifest_sha256=cfg['manifest_sha256'],config_sha256=ready['config_sha256'],source_identity=fingerprint,ledger_claim_sha256=claim_hash).items():
        require(ready[key]==value and spec[key]==value,'Peer identity mismatch: '+key)
    require(cfg['TEST_ONLY'] is False and cfg['automatic_resume'] is False and cfg['stop_epoch']==DEADLINE,'Peer production/deadline policy changed')
    require(cfg['dispatch_chunksize'] in (4,8) and cfg['journal_buffer_records']==8 and cfg['ready_queue_limit']==3,'Peer buffered runtime policy changed')
    require(cfg['workers']==16 and cfg['backend']=='gpu' and cfg['group_limit'] in (1,2,4) and cfg['replica_interval_seconds']==60 and cfg['maximum_replica_lag_seconds']==300,'Peer execution/replication policy changed')
    require((cfg['shell_lo'],cfg['shell_hi'],cfg['width'],cfg['bits'],cfg['cap'],cfg['chunk_patches'],cfg['geometry_policy'])==(100000000001,200000000000,8,222,42,256,'adaptive'),'Peer arithmetic changed')
    require(cfg['ledger_root']==str(SHARED) and cfg['ledger_job']==job and cfg['ledger_claim_sha256']==claim_hash and first<=cfg['initial_patch']<cfg['range_end']==last,'Peer reservation changed')
    require(Path(cfg['output']).is_relative_to('/home/pnord/fifth42-local-runs'),'Peer journal is not configured on its local disk')
    require(ready['local_output']==cfg['output'] and ready['replica_output']==cfg['replica_output'],'Peer storage binding changed')
    own=read(ROOT/'worker/release-manifest.json')['files'];actual=manifest['files']
    critical=[n for n in own if n.startswith('source/lattice_gpu/') or n.startswith('source/lattice_prototype/') or n.startswith('native-baseline/')]
    critical += ['runtime_initialize.py','width_coverage.py','durable_mirror.py','audit_grouped.py','finalize_replica.py','buffered_pipeline.py','scheduling.py']
    for name in critical:require(actual.get(name)==own[name],'Peer selected compute source differs: '+name)
    require('bin/scaling_gpu' in actual and 'packed_worker.py' in actual and 'policy.py' in actual,'Peer runtime/binary manifest is incomplete')
    require(sha(evidence/'parent-audit.json')==cfg['parent_audit_sha256'] and read(evidence/'parent-audit.json')['status']=='passed','Peer parent audit changed')
    require(sha(evidence/'parent-archive-receipt.json')==cfg['parent_archive_receipt_sha256'],'Peer parent archive receipt changed')
    receipt=read(evidence/'parent-archive-receipt.json')
    require(receipt['status']=='verified' and receipt['raw_sha256']==cfg['parent_journal_raw_sha256'] and receipt['captured_checkpoint_sha256']==cfg['parent_checkpoint_sha256'],'Peer parent archive links changed')
    require(sha(evidence/'runtime-validation.json')==ready['runtime_validation_sha256'] and read(evidence/'runtime-validation.json')['status']=='passed','Peer runtime tests missing')
    claim=read(evidence/'original-claim.json');require(claim['sha256']==claim_hash,'Wrong original claim')
    with (SHARED/'reservations.jsonl').open('r+b') as stream:
        fcntl.lockf(stream,fcntl.LOCK_SH|fcntl.LOCK_NB)
        claims=[json.loads(raw) for raw in stream.read().splitlines()]
    require([c for c in claims if c['job']==job]==[claim],'Original shared claim differs')
    ordered=sorted(claims,key=lambda c:c['first']);require(all(a['last']<=b['first'] for a,b in zip(ordered,ordered[1:])),'Shared reservations overlap')
    relative=Path(cfg['replica_output']).relative_to('/mnt/fifth42-storage')
    replica=BULK/relative
    require(replica==BULK/'runs'/job/cfg['run_id']/'run','Peer replica escaped its reserved output')
    raw=(replica/'checkpoint.json').read_bytes();cp=json.loads(raw);copy=read(replica/'replica-state.json')
    require(cp['identity']==dict(trial=cfg['run_id'],source_identity=fingerprint)==copy['identity'] and hashlib.sha256(raw).hexdigest()==copy['checkpoint_sha256'],'Peer replicated checkpoint identity changed')
    require(cp['journal_offset']==copy['committed_bytes'] and cp['journal_sha256']==copy['journal_sha256'],'Peer replica receipt differs from checkpoint')
    audit=audit_grouped.audit_suffix(replica,dict(checkpoint=dict(next_patch=cfg['initial_patch']),config=cfg),cp,'fresh',cfg['gmp_audit_period'])
    row=read(share/'status.json')
    require(row['host']==host and row['run_id']==cfg['run_id'] and row['source_identity']==fingerprint and row['checkpoint'],'Peer collector does not describe new production')
    require(row['phase'] in ('running','stopped') and not row['alerts'],'Peer collector is not clean')
    if row['phase']=='running':require(owner_locked(SHARED/'jobs'/job/'journal.jsonl'),'Peer original claim has no active owner')
    return cfg,spec,audit

def launch(host,ready,cfg,spec,audit):
    share=Path(ready['collector_share']);folder=Path('/home/pnord')/(host+'-buffered-reporting-20261109')
    folder.mkdir(mode=0o700,exist_ok=True)
    atomic(folder/'admission-audit.json',dict(status='passed',checked_epoch=time.time(),**audit))
    settings=read(Path('/home/pnord')/(host+'-bulk-reporting-20261108')/'publisher-settings.json')
    private=dict(spec,host=host,collector_spec_sha256=sha(share/'publication-spec.json'),reserved_interval=[cfg['initial_patch'],cfg['range_end']],original_reserved_interval=list(EXPECTED[host][1:3]),collector_reserved_interval=[cfg['initial_patch'],cfg['range_end']],stop_epoch=DEADLINE,parent_selected_patches=cfg['parent_selected_patches'],parent_committed_interval=[cfg['initial_patch']-cfg['parent_selected_patches'],cfg['initial_patch']],parent_audit_sha256=cfg['parent_audit_sha256'],**{k:cfg[k] for k in ('workers','backend','geometry_policy','journal_limit_bytes','minimum_free_disk_bytes')})
    atomic(folder/'publication-spec.json',private)
    bridge=(Path('/home/pnord/ada-buffered-reporting-20261109')/'bridge_base.py').read_text()
    (folder/'bridge_base.py').write_text(bridge)
    shutil.copy2(ROOT/'publish_buffered.py',folder/'publish_bulk_worker.py')
    unit=host+'-buffered-publisher-20261109'
    settings.update(host=host,share=str(share),service_name=unit+'.service',bridge_base_sha256=sha(folder/'bridge_base.py'))
    atomic(folder/'publisher-settings.json',settings);atomic(folder/'binding.json',dict(status='verified',ready=ready))
    py='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
    cmd=['systemd-run','--user','--unit='+unit,'--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(math.floor(DEADLINE+1800-time.time())),'--working-directory='+str(folder),'--property=StandardOutput=append:'+str(folder/'stdout.log'),'--property=StandardError=append:'+str(folder/'stderr.log'),py,'-B','-u',str(folder/'publish_bulk_worker.py')]
    subprocess.run(cmd,check=True,timeout=15)
    atomic(share/'ADA_PUBLISHER_ADMISSION.json',dict(status='publisher_started',ready=ready,admission_audit=audit,started_epoch=time.time(),service=unit+'.service'))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('host',choices=EXPECTED);parser.add_argument('--wait',action='store_true');args=parser.parse_args()
    require(os.uname().nodename.split('.')[0]=='ada','Publisher credential stays on Ada')
    dest=Path('/mnt/nfs_share/fifth42-integration-20261109/restart-buffered')/args.host;dest.mkdir(mode=0o700,parents=True,exist_ok=True)
    while time.time()<DEADLINE+1800:
        try:
            ready=read(dest/'READY_FOR_PUBLISHER.json');cfg,spec,audit=validate(args.host,ready);launch(args.host,ready,cfg,spec,audit)
            atomic(dest/'ADA_PUBLISHER_ADMISSION.json',dict(status='publisher_started',run_id=cfg['run_id'],checked_epoch=time.time(),audit=audit));return 0
        except Exception as exc:
            atomic(dest/'ADA_ADMISSION_HEALTH.json',dict(status='awaiting_ready' if isinstance(exc,FileNotFoundError) else 'evidence_rejected',error=str(exc),updated_epoch=time.time()))
            if not args.wait:raise
            time.sleep(15)
    raise TimeoutError('Peer reporting handoff did not arrive before cleanup ended')
if __name__=='__main__':raise SystemExit(main())
