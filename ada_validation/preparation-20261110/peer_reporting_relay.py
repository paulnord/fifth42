"""Read-only admission/relay of explicitly authorized overnight peer stages."""
import argparse,errno,fcntl,hashlib,json,math,os,re,shutil,subprocess,sys,tarfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OLDROOT=Path('/home/pnord/ada-overnight-20261109')
DELEGATED=Path('/mnt/nfs_share/boole-delegated-publishing-20261109')
sys.path.insert(0,str(ROOT/'worker'))
import audit_grouped,policy
from durable_mirror import atomic
DEADLINE=1794438000
VALID_DEADLINES=(1794351600,1794438000)
LEDGER=Path('/mnt/nfs_share/fifth42-shared-20261107')
BULK=Path('/mnt/localstorage/pnord/fifth42-storage')
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
def read(p):return json.loads(Path(p).read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def file_sha(p):return policy.digest(p)
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def locked(path):
    with Path(path).open('r+b') as f:
        try:fcntl.lockf(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as e:
            if e.errno in (errno.EACCES,errno.EAGAIN):return True
            raise
        fcntl.lockf(f,fcntl.LOCK_UN);return False
def server_path(path):
    p=Path(path)
    if p.is_relative_to('/mnt/fifth42-storage'):return BULK/p.relative_to('/mnt/fifth42-storage')
    require(p.is_relative_to(BULK),'Unexpected shared-data path');return p

def source_for(host):
    base=OLDROOT/'peer-bundles'/host
    if host=='boole':
        if (DELEGATED/'active-publication-spec.json').exists():
            spec=read(DELEGATED/'active-publication-spec.json');run=spec['run_id']
            require(re.fullmatch(r'boole-[A-Za-z0-9_.-]+',run),'Unexpected delegated Boole stage')
            evidence=DELEGATED/'runs'/run
            for name,h in spec['evidence_sha256'].items():
                require(Path(name).name==name and file_sha(evidence/name)==h,'Delegated Boole evidence changed: '+name)
            cf=(evidence/'configuration.json').read_bytes();mf=(evidence/'source-manifest.json').read_bytes()
            require(sha(cf)==spec['config_sha256'] and sha(mf)==spec['manifest_sha256'],'Delegated Boole specification hash mismatch')
            require(read(DELEGATED/'status.json')['run_id']==run,'Delegated Boole collector has not switched yet')
            return DELEGATED,cf,mf,evidence,evidence/'source.tar.gz',None
        plan=read(base/'controller/production-plan.json')
        live=read('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole/PRODUCTION_STATUS.json')
        active=live.get('active')
        run=active['run_id'] if active else ((live.get('completed') or [{}])[-1].get('run_id') or plan['stages'][0]['root'].split('/')[-1])
        candidates=[x for x in plan['stages'] if x['root'].split('/')[-1]==run]
        require(len(candidates)==1,'Boole active stage is not in its frozen plan')
        stage=candidates[0];folder=base/run;cf=folder/'worker/production-config.json'
        require(file_sha(cf)==stage['config_sha256'],'Boole stage configuration changed')
        share=Path('/mnt/nfs_share/boole-overnight-publishing-20261109') if run=='boole-overnight-20261109' else Path('/mnt/nfs_share')/(run+'-publishing')
        return share,cf.read_bytes(),(folder/'worker/release-manifest.json').read_bytes(),folder/'worker',None,live
    share=Path('/mnt/nfs_share/cabbage-extended-publishing-20261109')
    spec=read(share/'active-publication-spec.json');run=spec['run_id']
    require(re.fullmatch(r'cabbage-extended-[A-Za-z0-9_.-]+',run),'Unexpected Cabbage stage id')
    evidence=share/'runs'/run
    for name,h in spec['evidence_sha256'].items():
        require(Path(name).name==name and file_sha(evidence/name)==h,'Cabbage evidence changed: '+name)
    cf=(evidence/'configuration.json').read_bytes();mf=(evidence/'source-manifest.json').read_bytes()
    require(sha(cf)==spec['config_sha256'] and sha(mf)==spec['manifest_sha256'],'Cabbage specification hash mismatch')
    return share,cf,mf,evidence,evidence/'source.tar.gz',None

def validate_common(host,cf,mf,source,archive):
    c=json.loads(cf);m=json.loads(mf)
    require(c['TEST_ONLY'] is False and c['automatic_resume'] is False and c['stop_epoch'] in VALID_DEADLINES,'Peer authorization/deadline changed')
    require(c['manifest_sha256']==sha(mf),'Peer runtime manifest mismatch')
    require((c['shell_lo'],c['shell_hi'],c['width'],c['bits'],c['cap'],c['chunk_patches'],c['geometry_policy'])==(100000000001,200000000000,8,222,42,256,'adaptive'),'Peer arithmetic/grid changed')
    require(c['workers']==16 and c['physical_cpus']==list(range(16)) and c['backend']=='gpu' and c['group_limit'] in (1,2,4,8,16) and c['dispatch_chunksize']==max(1,16//c['group_limit']),'Unadmitted peer execution policy')
    require(c['journal_buffer_records']==8 and c['ready_queue_limit']==(3 if c.get('preparation_windows',1)==1 else 1) and c['gmp_audit_period']==128 and c['replica_interval_seconds']==60 and c['maximum_replica_lag_seconds']==300,'Peer buffering/audit policy changed')
    baseline=read('/home/pnord/ada-group4-20261109/worker/release-manifest.json')['files']
    critical=[n for n in baseline if n.startswith(('source/lattice_gpu/','source/lattice_prototype/','native-baseline/')) and 'bin' not in Path(n).parts]
    critical+=['runtime_initialize.py','width_coverage.py','buffered_pipeline.py','scheduling.py','audit_grouped.py','durable_mirror.py','finalize_replica.py']
    deployed=read(ROOT/'worker/release-manifest.json')['files']
    release=read('/mnt/nfs_share/fifth42-integration-20261109/combined/preparation-r1-20261110/READY.json')['files']
    for n in critical:
        allowed={baseline[n],deployed.get(n),release.get('common/'+n)}
        require(m['files'].get(n) in allowed,'Unadmitted scientific source: '+n)
    if archive:
        spec=read((DELEGATED/'active-publication-spec.json') if host=='boole' else '/mnt/nfs_share/cabbage-extended-publishing-20261109/active-publication-spec.json')
        require(file_sha(archive)==spec['source_archive_sha256'],'Cabbage source archive changed')
        with tarfile.open(archive,'r:gz') as t:
            members={x.name:x for x in t.getmembers()}
            for n,h in m['files'].items():
                member=members.get('worker/'+n)
                require(member is not None and member.isfile() and sha(t.extractfile(member).read())==h,'Cabbage archived source changed: '+n)
            require(t.extractfile(members['production-config.json']).read()==cf,'Cabbage archived configuration differs')
    else:
        for n,h in m['files'].items():require(file_sha(source/n)==h,'Boole archived runtime changed: '+n)
    import ada_export_store
    delegated=host=='boole' and c.get('allocation_role')=='boole'
    if delegated:
        import suballocation_guard
        grant=suballocation_guard.check(c,observer_role='boole')
        require(m['files'].get('bin/scaling_gpu')==grant['boole_native_gpu_sha256'] and m['files'].get('bin/scaling_gmp')==grant['boole_native_gmp_sha256'],'Delegated Boole native binaries changed')
    else:require(Path(c['ledger_root'])==LEDGER,'Unadmitted peer ledger')
    ledger=Path(c['ledger_root']);store=ada_export_store.Store(ledger);claim=policy.claim_with_retry(store,c['ledger_job'])
    require(claim['sha256']==c['ledger_claim_sha256'] and claim['first']<=c['initial_patch']<c['range_end']==claim['last'],'Peer reservation changed')
    # Validate the complete signed reservation snapshot without holding it for auditing.
    until=time.monotonic()+5
    while True:
        try:
            with store.locked(ledger/'reservations.jsonl') as fd:claims=store.claims(fd)
            break
        except ada_export_store.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.05)
    ordered=sorted(claims,key=lambda x:x['first'])
    require(all(a['last']<=z['first'] for a,z in zip(ordered,ordered[1:])),'Shared reservations overlap')
    replica=server_path(c['replica_output'])
    require(replica==BULK/'runs'/c['ledger_job']/c['run_id']/'run','Peer replica directory changed')
    fingerprint=sha(json.dumps(dict(manifest_sha256=c['manifest_sha256'],config=c),sort_keys=True,separators=(',',':')).encode())
    raw=(replica/'checkpoint.json').read_bytes();cp=json.loads(raw);receipt=read(replica/'replica-state.json')
    require(cp['identity']==receipt['identity']==dict(trial=c['run_id'],source_identity=fingerprint),'Replicated checkpoint source mismatch')
    require(sha(raw)==receipt['checkpoint_sha256'] and cp['journal_offset']==receipt['committed_bytes'] and cp['journal_sha256']==receipt['journal_sha256'],'Replica receipt changed during capture')
    evidence={}
    for name,key in [('parent-audit.json','parent_audit_file'),('original-claim.json','origin_claim_file')]:
        path=source/name if archive else source/Path(c[key]).name
        expected=c['parent_audit_sha256'] if name=='parent-audit.json' else c['origin_claim_file_sha256']
        require(file_sha(path)==expected,'Parent/origin evidence changed: '+name);evidence[name]=path.read_bytes()
    parent=server_path(c['parent_run']);receipt_path=server_path(c['parent_archive_receipt'])
    require(file_sha(receipt_path)==c['parent_archive_receipt_sha256'],'Sealed parent archive receipt changed')
    audit=json.loads(evidence['parent-audit.json']);prior=read(parent/'checkpoint.json')
    require(audit['status']=='passed' and file_sha(parent/'checkpoint.json')==c['parent_checkpoint_sha256'],'Parent audit/checkpoint mismatch')
    if c['parent_selected_patches']:
        require(prior['next_patch']==c['initial_patch'],'Continuation skipped its exact parent cursor')
    else:require(c['initial_patch']==claim['first'],'Fresh work must start at its uncomputed reservation boundary')
    require(json.loads(evidence['original-claim.json'])==claim,'Original claim proof differs from shared ledger')
    checked=audit_grouped.audit_suffix(replica,dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',c['gmp_audit_period'])
    controls=read(replica/'controls.json')
    require(controls['status']=='passed' and all(x['full_oracle_equal'] and x['hits'] for x in controls['cases']),'Peer nonempty controls failed')
    evidence.update({'configuration.json':cf,'source-manifest.json':mf,'parent-archive-receipt.json':receipt_path.read_bytes()})
    return c,fingerprint,evidence,checked

def admit(host,share,cf,mf,source,archive):
    c,fingerprint,evidence,audit=validate_common(host,cf,mf,source,archive)
    folder=OLDROOT/'peer-reporting'/host/c['run_id'];folder.mkdir(mode=0o700,parents=True,exist_ok=True)
    if (folder/'publication-spec.json').exists():
        require(read(folder/'publication-spec.json')['config_sha256']==sha(cf),'Existing relay binding belongs to another configuration')
    view=folder/'view';(view/'evidence').mkdir(mode=0o700,parents=True,exist_ok=True)
    hashes={}
    for name,raw in evidence.items():(view/'evidence'/name).write_bytes(raw);hashes[name]=sha(raw)
    spec=dict(run_id=c['run_id'],manifest_sha256=c['manifest_sha256'],config_sha256=sha(cf),source_identity=fingerprint,ledger_claim_sha256=c['ledger_claim_sha256'],evidence=hashes)
    atomic(view/'publication-spec.json',spec)
    private=dict(spec,host=host,collector_spec_sha256=file_sha(view/'publication-spec.json'),reserved_interval=[c['initial_patch'],c['range_end']],stop_epoch=c['stop_epoch'],parent_selected_patches=c['parent_selected_patches'],parent_committed_interval=[c['initial_patch']-c['parent_selected_patches'],c['initial_patch']],parent_audit_sha256=c['parent_audit_sha256'],**{k:c[k] for k in ['workers','backend','geometry_policy','journal_limit_bytes','minimum_free_disk_bytes']})
    atomic(folder/'publication-spec.json',private)
    bridge=Path('/home/pnord/ada-overnight-reporting-20261109/bridge_base.py').read_text()
    (folder/'bridge_base.py').write_text(bridge)
    publisher=(OLDROOT/'publish_buffered.py').read_text().replace('The fresh trial starts at the exact final parent cursor under the unchanged original reservation.','Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.')
    (folder/'publish_bulk_worker.py').write_text(publisher)
    old=read(Path('/home/pnord')/(host+'-bulk-reporting-20261108')/'publisher-settings.json')
    unit=host+'-overnight-publisher-'+sha(c['run_id'].encode())[:12]
    old.update(host=host,share=str(view),service_name=unit+'.service',bridge_base_sha256=file_sha(folder/'bridge_base.py'))
    atomic(folder/'publisher-settings.json',old);atomic(folder/'binding.json',dict(status='verified',source_collector=str(share),audit=audit,config_sha256=sha(cf),manifest_sha256=c['manifest_sha256']))
    active=subprocess.run(['systemctl','--user','is-active','--quiet',unit+'.service'],capture_output=True,timeout=5).returncode==0
    return dict(folder=str(folder),view=str(view),source=str(share),config=c,spec=spec,unit=unit,started=active,audit=audit)

def forward(binding,row):
    c=binding['config'];spec=binding['spec']
    for key in ['run_id','manifest_sha256','config_sha256','source_identity','ledger_claim_sha256']:require(row[key]==spec[key],'Collector identity changed: '+key)
    require(row['stop_epoch']==c['stop_epoch'] and row['stop_epoch'] in VALID_DEADLINES and row['reserved_interval']==[c['initial_patch'],c['range_end']] and row['completed_bound'] is None,'Collector range/deadline changed')
    age=time.time()-__import__('datetime').datetime.fromisoformat(row['snapshot_utc']).timestamp()
    require(-5<=age<=120 or row['phase'] in ('failed','stopped'),'Collector is stale')
    if row['phase']=='running':
        if c.get('allocation_role')=='boole':
            import suballocation_guard
            suballocation_guard.check(c,observer_role='boole')
        require(locked(Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl'),'Peer owner lock is not held')
    atomic(Path(binding['view'])/'status.json',row)
    if not binding['started']:
        folder=Path(binding['folder']);command=['systemd-run','--user','--unit='+binding['unit'],'--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(max(1,math.floor(DEADLINE+1800-time.time()))),'--working-directory='+str(folder),'--property=StandardOutput=append:'+str(folder/'stdout.log'),'--property=StandardError=append:'+str(folder/'stderr.log'),PYTHON,'-B','-u',str(folder/'publish_bulk_worker.py')]
        subprocess.run(command,check=True,capture_output=True,text=True,timeout=20);binding['started']=True
        atomic(Path(binding['source'])/'ADA_PUBLISHER_ADMISSION.json',dict(status='publisher_started',run_id=c['run_id'],service=binding['unit']+'.service',audit=binding['audit'],checked_epoch=time.time(),reporter=str(folder)))
    ready=Path(binding['folder'])/'readiness.json'
    if ready.exists():atomic(Path(binding['source'])/'ada-publisher-readiness.json',read(ready))

def finalize_view(binding):
    from datetime import datetime,timezone
    c=binding['config'];view=Path(binding['view']);row=read(view/'status.json')
    replica=server_path(c['replica_output']);raw=(replica/'checkpoint.json').read_bytes()
    cp=json.loads(raw);receipt=read(replica/'replica-state.json');native=read(replica/'status.json')
    require(sha(raw)==receipt['checkpoint_sha256'] and cp['journal_sha256']==receipt['journal_sha256'] and cp['journal_offset']==receipt['committed_bytes'],'Terminal replica is not consistent')
    require(cp['identity']==receipt['identity']==dict(trial=c['run_id'],source_identity=binding['spec']['source_identity']),'Terminal stage identity changed')
    require(native['status'] in ('stopped','failed','completed_test'),'Previous stage is not terminal')
    row.update(snapshot_utc=datetime.now(timezone.utc).isoformat(),phase='failed' if native.get('error') else 'stopped',checkpoint=cp,replica=receipt,local_next_patch=cp['next_patch'],committed_interval=[c['initial_patch'],cp['next_patch']],service=dict(ActiveState='inactive',SubState='dead',MainPID='0',NRestarts='0'),combined_selected_patches=c['parent_selected_patches']+cp['patches'],combined_committed_interval=[c['initial_patch']-c['parent_selected_patches'],cp['next_patch']],alerts=[native['error']] if native.get('error') else [],terminal_relay_source='Verified final bulk replica after the next stage was admitted')
    row['worker_metrics']={k:native[k] for k in row['worker_metrics'] if k in native}
    atomic(view/'status.json',row)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('host',choices=['boole','cabbage']);args=parser.parse_args()
    base=OLDROOT/'peer-reporting'/args.host;base.mkdir(mode=0o700,parents=True,exist_ok=True)
    bindings={};last=None
    while time.time()<DEADLINE+1800:
        try:
            share,cf,mf,source,archive,controller=source_for(args.host);c=json.loads(cf);run=c['run_id']
            if run not in bindings:
                binding=admit(args.host,share,cf,mf,source,archive);bindings[run]=binding
            row=read(share/'status.json')
            if row['run_id']!=run:time.sleep(2);continue
            # Preserve the old stage's terminal view across a successful handoff.
            if last and last!=run:
                old=bindings[last]
                finalize_view(old)
                until=time.monotonic()+45
                while subprocess.run(['systemctl','--user','is-active','--quiet',old['unit']+'.service'],capture_output=True,timeout=5).returncode==0:
                    require(time.monotonic()<until,'Previous terminal publisher has not finished; newer publication waits')
                    time.sleep(1)
                # Refresh after the ordered terminal publication wait.
                row=read(share/'status.json')
            forward(bindings[run],row);last=run
            atomic(base/'health.json',dict(status='ok',run_id=run,checked_epoch=time.time(),binding=bindings[run]['folder']))
        except Exception as error:
            atomic(base/'health.json',dict(status='error',error=repr(error),checked_epoch=time.time()))
            print(repr(error),flush=True)
        time.sleep(5)
if __name__=='__main__':main()
