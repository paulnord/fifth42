"""Run frozen Ada jobs once; settle, publish, audit and archive before advancing."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
STOP=ROOT/'STOP_ADA_R3'

def require(ok,message):
    if not ok:raise RuntimeError(message)
def read(path):return json.loads(Path(path).read_bytes())
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda:stream.read(4*1024**2),b''):h.update(data)
    return h.hexdigest()
def atomic(path,row):
    sys.path.insert(0,str(ROOT));from allocation_guard import atomic as save;save(Path(path),row)
def command(args,timeout=40):
    p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
    require(p.returncode==0,str(args)+' '+p.stderr[-2000:]);return p.stdout
def unit(name):
    return dict(line.split('=',1) for line in command(['systemctl','--user','show',name,'-p','ActiveState','-p','MainPID','-p','Result']).splitlines() if '=' in line)
def service(name,cwd,script,args,deadline):
    require(not name.startswith('fifth'),'Service name conflicts with the legacy resource guard')
    return ['systemd-run','--user','--unit='+name,'--collect','--service-type=exec','--property=Restart=no','--property=Nice=19','--property=UMask=0077','--property=RuntimeMaxSec='+str(max(1,int(deadline+1800-time.time()))),'--working-directory='+str(cwd),'--property=StandardOutput=append:'+str(Path(cwd)/(name+'.stdout.log')),'--property=StandardError=append:'+str(Path(cwd)/(name+'.stderr.log')),PYTHON,'-B','-u',str(script),*args]

def terminal_is_clean(owner,supervisor,status,cp,c):
    require(owner['ActiveState']=='inactive' and owner['MainPID']=='0','Compute owner is not quiescent')
    require(supervisor.get('error') is None and supervisor.get('worker_exit_code')==0 and supervisor.get('leases_released') is True,'Supervisor failed or retained ownership')
    require(status.get('status')=='stopped' and status.get('error') is None,'Worker did not stop cleanly')
    require(status.get('journal_buffer',{}).get('pending_chunks')==0 and status['journal_buffer'].get('pending_bytes')==0,'Pending journal records')
    require(cp['next_patch']==c['range_end'] and cp['patches']==c['range_end']-c['initial_patch'],'Partial interval; manual review required')

def wait_replica(spec,c,final=False):
    out=Path(c['output']);rep=Path(c['replica_output']);until=time.monotonic()+(900 if final else 315)
    while True:
        if STOP.exists() and not final:return False
        try:
            raw=(rep/'checkpoint.json').read_bytes();cp=json.loads(raw);proof=read(rep/'replica-state.json')
            ready=(proof['status']=='verified' and proof['checkpoint_sha256']==hashlib.sha256(raw).hexdigest() and proof['identity']==cp['identity'] and proof['committed_bytes']==cp['journal_offset'] and proof['journal_sha256']==cp['journal_sha256'])
            if final:
                ended=read(out/'final-replica.json');ready=ready and raw==(out/'checkpoint.json').read_bytes() and ended['status']=='verified' and ended['receipt']==proof
            if ready:return cp
        except FileNotFoundError:pass
        if not final:require(unit(c['service_name'])['ActiveState']!='failed','Compute service failed before first replica')
        require(time.monotonic()<until,'Verified replica did not arrive');time.sleep(1)

def settle_publication(spec,c,cp):
    reporter=Path(spec['reporter']);until=time.monotonic()+300
    while time.monotonic()<until:
        ready=reporter/'readiness.json'
        if ready.exists():
            proof=read(ready);push=proof.get('latest_push',{});verified=proof.get('latest_readback',{})
            if (push.get('run_id')==c['run_id'] and push.get('phase')=='stopped' and proof.get('latest_checkpoint')==cp and proof.get('final_replica_verified') is True and verified.get('status')=='passed' and verified.get('commit')==push.get('commit')):return
        if unit(spec['publisher'])['ActiveState'] not in ('active','activating','deactivating'):
            snapshot=read('/mnt/nfs_share/ada-preparation-publishing-20261110/status.json')
            if snapshot.get('run_id')==c['run_id'] and snapshot.get('checkpoint')==cp and snapshot.get('phase')=='stopped' and snapshot.get('final_replica_verified') is True:
                command([PYTHON,'-B',str(reporter/'publish_bulk_worker.py'),'--once'],timeout=150)
        time.sleep(2)
    raise TimeoutError('Exact final checkpoint has not been published and read back')

def archive(spec,c,cp):
    out=Path(c['output']);rep=Path(c['replica_output']);final=read(out/'final-replica.json');receipt=final['receipt']
    require((out/'coverage.jsonl').stat().st_size==(rep/'coverage.jsonl').stat().st_size==cp['journal_offset'],'Final journal size mismatch')
    require(sha(out/'coverage.jsonl')==receipt['raw_sha256'],'Final raw hash differs from verified mirror')
    sys.path.insert(0,'/home/pnord/ada-preparation-release-20261110');from parallel_audit_ref import audit
    checked=audit(out,c,workers=16);checked.update(captured_checkpoint_sha256=sha(out/'checkpoint.json'),committed_chain_sha256=cp['journal_sha256'],committed_raw_sha256=receipt['raw_sha256'],selected_interval=[c['initial_patch'],cp['next_patch']],uncommitted_trailing_bytes=0,owner_lock_released=True,local_and_replica_equal=True)
    evidence=ROOT/'completed-audits'/c['run_id'];evidence.mkdir(mode=0o700,parents=True,exist_ok=False);atomic(evidence/'parent-audit.json',checked)
    ar=dict(status='verified',raw_sha256=receipt['raw_sha256'],committed_bytes=cp['journal_offset'],captured_checkpoint_sha256=sha(out/'checkpoint.json'),captured_status_sha256=sha(rep/'status.json'),source=str(out),archive=str(rep),audit_sha256=sha(evidence/'parent-audit.json'),method='Full committed receipt/GMP audit, source raw hash and independent final mirror byte comparison')
    require(not(rep/'ARCHIVE_RECEIPT.json').exists(),'Archive receipt already exists; review required');atomic(rep/'ARCHIVE_RECEIPT.json',ar)
    local=out/'coverage.jsonl';pending=out/'coverage.OFFLOAD_PENDING.jsonl';require(not local.is_symlink() and not pending.exists(),'Unexpected archive state');os.rename(local,pending)
    try:local.symlink_to(rep/'coverage.jsonl');require(local.stat().st_size==cp['journal_offset'],'Archive link length mismatch');pending.unlink()
    except BaseException:
        if local.is_symlink():local.unlink()
        if pending.exists():os.rename(pending,local)
        raise
    atomic(out/'LOCAL_JOURNAL_ARCHIVED.json',dict(status='archived_verified_copy_with_original_path_preserved',archive=str(rep/'coverage.jsonl'),bytes=cp['journal_offset'],raw_sha256=receipt['raw_sha256']))
    return dict(run_id=c['run_id'],next_patch=cp['next_patch'],patches=cp['patches'],audit=str(evidence/'parent-audit.json'),archive=str(rep))

def launch(spec,c,previous):
    if previous:
        until=time.monotonic()+30
        while unit(previous['publisher'])['ActiveState'] in ('active','activating','deactivating'):
            require(time.monotonic()<until,'Previous publisher has not exited');time.sleep(1)
        command(['systemctl','--user','stop',previous['collector']])
    root=Path(spec['root']);w=Path(spec['worker']);reporter=Path(spec['reporter'])
    for script in ('prepare_launch.py','prepare_reporting.py'):command([PYTHON,'-B',str(root/script)])
    command(service(c['run_id']+'-final-copy',root,w/'finalize_replica.py',['--config',spec['config'],'--config-sha256',spec['config_sha256'],'--wait'],c['stop_epoch']))
    command(service(spec['collector'].removesuffix('.service'),reporter,reporter/'collector.py',[],c['stop_epoch']))
    command([PYTHON,'-B',str(w/'launch_weekend.py'),'--launch'],timeout=90)
    if not wait_replica(spec,c):return False
    command(service(spec['publisher'].removesuffix('.service'),reporter,reporter/'publish_bulk_worker.py',[],c['stop_epoch']))
    return True

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--plan',required=True);parser.add_argument('--plan-sha256',required=True);args=parser.parse_args()
    require(sha(args.plan)==args.plan_sha256,'Frozen plan changed');plan=read(args.plan);require(sha(__file__)==plan['controller_sha256'],'Frozen controller changed')
    status_path=ROOT/'QUEUE_STATUS.json';require(not status_path.exists(),'Existing queue state requires manual review')
    state=dict(status='starting',active=None,completed=[],error=None,stop_epoch=plan['stop_epoch'],plan_sha256=args.plan_sha256)
    previous=plan['previous']
    def save():state['updated_utc']=datetime.now(timezone.utc).isoformat();atomic(status_path,state);atomic(Path(plan['shared_status_file']),state)
    try:
        for spec in plan['stages']:
            if STOP.exists() or time.time()>=plan['stop_epoch']-120:state['status']='stopped';save();return
            require(sha(args.plan)==args.plan_sha256 and sha(__file__)==plan['controller_sha256'],'Frozen queue changed')
            require(sha(spec['config'])==spec['config_sha256'],'Frozen stage config changed');c=read(spec['config'])
            require(not Path(c['output']).exists() and not Path(c['replica_output']).exists(),'Existing output; automatic failure resume is forbidden')
            state.update(status='launching',active=spec);save()
            if not launch(spec,c,previous):return
            state['status']='running';save()
            while unit(c['service_name'])['ActiveState'] in ('active','activating','deactivating'):
                if STOP.exists() or time.time()>=c['stop_epoch']-10:command(['systemctl','--user','stop',c['service_name']])
                save();time.sleep(2)
            cp=wait_replica(spec,c,final=True);sup=read(Path(spec['worker'])/'supervisor-report.json');native=read(Path(c['output'])/'status.json')
            if STOP.exists() or time.time()>=c['stop_epoch']-10:
                state['status']='stopped_at_deadline_or_request';save();return
            terminal_is_clean(unit(c['service_name']),sup,native,cp,c)
            settle_publication(spec,c,cp);state['completed'].append(archive(spec,c,cp));previous=spec;state['active']=None;save()
        state['status']='all_assigned_jobs_complete';save()
    except BaseException as error:state.update(status='attention_required',error=repr(error));save();raise

if __name__=='__main__':main()
