"""Run only delegated claim31, then leave its exact sealed prefix to R5."""
from datetime import datetime,timezone
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import uuid

from early_support import atomic,command,load,read,require,sha,unit
import early_build
import early_guard
from phase_admission import freeze_phase,desired_changed,request_phase_drain

ROOT=Path(__file__).resolve().parent
LIVE=Path('/home/pnord/fifth42-deadline-extension-20261112')
SHARED=Path('/mnt/nfs_share/fifth42-integration-20261109/combined/ada-early-claim31-interim-20261112')
SETTINGS=Path('/mnt/nfs_share/fifth42-integration-20261109/SEARCH_SETTINGS.json')
PY='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
STOP=False


def checked(row,name):
    require(sha(row[name+'_file'])==row[name+'_sha256'],'Changed early input: '+name)
    return read(row[name+'_file'])


def verify(plan,path,pin):
    require(sha(path)==pin and plan.get('activation_enabled') is True,'Early controller plan is not admitted')
    for source,want in plan['source_files'].items():require(sha(source)==want,'Early controller source changed: '+source)
    checked(plan,'fence_ack');checked(plan,'fallback_retirement')


def desired(previous=None):
    try:return load(LIVE/'boundary_settings.py').read_request(SETTINGS)
    except (OSError,ValueError,TypeError):
        if previous is None:raise
        return previous


def launcher_commands(worker,config):
    code=('import json,sys;sys.path.insert(0,sys.argv[1]);'
          'import policy,launch_weekend;'
          'c=policy.load_config(sys.argv[2]);print(json.dumps(launch_weekend.commands(c)))')
    return json.loads(command([PY,'-B','-c',code,str(worker),str(config)],90))


def stop_owned(name):
    actual=unit(name)
    if actual['ActiveState']!='inactive' or actual.get('MainPID','0')!='0':
        subprocess.run(['systemctl','--user','stop',name],capture_output=True,timeout=25)
    actual=unit(name)
    require(actual['ActiveState']=='inactive' and actual.get('MainPID','0')=='0','Owned unit remains active: '+name)


def phase(plan,reference,index,request):
    old=checked(plan,'original_parent_grant')
    directory=SHARED/'admissions'/('phase-%04d-'%index+uuid.uuid4().hex[:12])
    capped=freeze_phase(directory,request,old,execution_request_id=plan['execution_request_id'])
    claim=checked(plan,'claim')
    inventory=directory/'PREPARED-INVENTORY.json'
    first=reference['next_patch'] if reference.get('same_claim') else claim['first']
    atomic(inventory,dict(status='prepared_exact_single_claim',ledger_job=claim['job'],
        first=first,last=claim['last'],native_coverage_imported=0,claim=claim,reference=reference),exclusive=True)
    name='ada-early31-p%04d-'%index+directory.name.rsplit('-',1)[1]
    prepared=early_build.prepare_runtime(ROOT/'stages'/name,claim,reference,inventory)
    g=dict(schema=early_guard.SCHEMA,generation=early_guard.GENERATION,status='admitted',TEST_ONLY=False,
        executor='ada',execution_request_id=plan['execution_request_id'],original_assignment=plan['original_assignment'],
        initial_patch=first,range_end=claim['last'],runtime_profile=early_guard.PROFILE,
        runtime_source_files=prepared['runtime_source_files'],runtime_external_files=prepared['runtime_external_files'],
        worker_guard_sha256=sha(Path(prepared['worker'])/'suballocation_guard.py'),
        native_binaries=old['native_binaries']['ada'],phase_settings_file=capped['deadline_settings_file'],
        original_guard_file=plan['original_guard_file'],original_guard_sha256=plan['original_guard_sha256'],
        original_parent_unit=plan['original_parent_unit'],original_parent_pid=plan['original_parent_pid'],
        original_parent_source_file=plan['original_parent_source_file'],
        original_parent_source_sha256=plan['original_parent_source_sha256'],
        stop_epoch=capped['stop_epoch'],stop_local=capped['stop_local'],
        phase_not_after_epoch=capped['phase_not_after_epoch'])
    for key in ('original_parent_grant','fence_ack','fallback_retirement'):
        for suffix in ('_file','_sha256'):g[key+suffix]=plan[key+suffix]
    for key in ('desired_deadline_authorization','phase_deadline_authorization'):
        for suffix in ('_file','_sha256'):g[key+suffix]=capped[key+suffix]
    grant=directory/'GRANT.json';atomic(grant,g,exclusive=True)
    cfg=early_build.bind_configuration(prepared,grant,reference,ROOT/'SOURCE-REVIEW.json',inventory)
    early_guard.check(cfg,force=True)
    stageplan=dict(plan,stop_epoch=g['stop_epoch'],stop_local=g['stop_local'],inventory_file=str(inventory),
                   controller_plan_file=plan['controller_plan_file'])
    from early_report_stage import prepare
    spec=prepare(prepared['root'],cfg,stageplan)
    atomic(directory/'CONFIG-BINDING.json',dict(spec=spec,config_sha256=spec['config_sha256']),exclusive=True)
    return spec,cfg,grant


def seal(spec,cfg,grant,q,previous):
    worker=Path(spec['worker']);output=Path(cfg['output'])
    native=read(output/'status.json');supervisor=read(worker/'supervisor-report.json')
    require(supervisor.get('worker_exit_code')==0 and supervisor.get('error') is None
            and supervisor.get('leases_released') is True,'Early supervisor did not settle')
    require(native.get('status')=='stopped' and native.get('error') is None
            and all(native.get('journal_buffer',{}).get(k,0)==0 for k in ('pending_chunks','pending_bytes')),
            'Early native journal did not stop cleanly')
    cp=q.wait_replica(spec,cfg,final=True)
    q.settle_publication(spec,cfg,cp)
    archived=q.archive(spec,cfg,cp)
    folder=SHARED/'sealed'/cfg['run_id'];folder.mkdir(mode=0o700,parents=True,exist_ok=False)
    paths={}
    for key,source in (('publication_status',Path('/mnt/nfs_share/ada-preparation-publishing-20261110/status.json')),
                       ('publication_readback',Path(spec['reporter'])/'readiness.json')):
        raw=source.read_bytes();destination=folder/(key+'.json');destination.write_bytes(raw)
        paths[key+'_file']=str(destination);paths[key+'_sha256']=sha(destination)
    replica=Path(archived['archive']);receipt=replica/'ARCHIVE_RECEIPT.json'
    row=dict(schema='fifth42-early-child-seal-v1',status='verified_early_seal',TEST_ONLY=False,
        execution_request_id=read(grant)['execution_request_id'],host='ada',ledger_job=cfg['ledger_job'],
        first=cfg['initial_patch'],last=cp['next_patch'],initial_patch=cfg['initial_patch'],next_patch=cp['next_patch'],
        range_end=cfg['range_end'],parent_run=str(replica),config_file=spec['config'],config_sha256=spec['config_sha256'],
        source_manifest_file=cfg['manifest'],source_manifest_sha256=cfg['manifest_sha256'],
        checkpoint_sha256=sha(replica/'checkpoint.json'),raw_sha256=read(receipt)['raw_sha256'],
        audit_file=archived['audit'],audit_sha256=sha(archived['audit']),
        archive_receipt_file=str(receipt),archive_receipt_sha256=sha(receipt),
        early_grant_file=str(grant),early_grant_sha256=sha(grant),
        fence_ack_file=read(grant)['fence_ack_file'],fence_ack_sha256=read(grant)['fence_ack_sha256'],
        native_gmp_audit='passed',exact_terminal_readback='passed',**paths)
    if previous:row.update(previous_seal_file=str(previous),previous_seal_sha256=sha(previous))
    target=folder/'EARLY-SEAL.json';atomic(target,row,exclusive=True)
    atomic(ROOT/'EARLY-BOUNDARY.json',dict(execution_request_id=row['execution_request_id'],
        early_grant_file=str(grant),early_grant_sha256=sha(grant),seal_file=str(target),seal_sha256=sha(target)))
    return target,row


def run(plan,path,pin):
    global STOP
    verify(plan,path,pin)
    require(unit(plan['future_controller_unit'])['ActiveState']=='active','Complete overnight replacement is not armed')
    for name in plan['retired_reporting_units']:
        stop_owned(name)
    q=load(ROOT/'queue_helper.py');q.ROOT=ROOT;q.STOP=ROOT/'STOP_EARLY';q.atomic=atomic
    reference=checked(plan,'initial_reference');lastseal=None;index=0;request=desired()
    state=dict(status='preparing_early_phase',active=None,error=None,completed=[],future_cutover_epoch=1794526200)
    def save():
        state['updated_utc']=datetime.now(timezone.utc).isoformat();atomic(ROOT/'STATE.json',state)
        atomic(SHARED/'STATUS.json',state)
    save()
    while reference.get('same_claim') is not True or reference['next_patch']<plan['original_assignment']['last']:
        verify(plan,path,pin);request=desired(request)
        if STOP or (ROOT/'STOP_EARLY').exists() or time.time()>=min(request['stop_epoch'],1794524400)-120:
            state.update(status='early_phase_sealed_waiting_for_overnight',active=None);save();return
        index+=1;spec,cfg,grant=phase(plan,reference,index,request)
        state.update(status='launching_early_native',active=spec,effective_stop_epoch=cfg['stop_epoch'],
                     desired_stop_epoch=request['stop_epoch']);save()
        worker=Path(spec['worker'])
        command([PY,'-B',str(worker/'search_supervisor.py'),'--config',spec['config'],'--check-only'],90)
        command(q.service(cfg['run_id']+'-final-copy',spec['root'],worker/'finalize_replica.py',
                ['--config',spec['config'],'--config-sha256',spec['config_sha256'],'--wait'],cfg['stop_epoch']))
        command(q.service(spec['collector'].removesuffix('.service'),spec['reporter'],Path(spec['reporter'])/'collector.py',[],cfg['stop_epoch']))
        commands=launcher_commands(worker,spec['config'])
        command(commands['timer'])
        invocation=launcher_commands(worker,spec['config'])['service'];invocation.insert(1,'--wait')
        stdout=open(Path(spec['root'])/'systemd-run-wait.stdout','x');stderr=open(Path(spec['root'])/'systemd-run-wait.stderr','x')
        process=subprocess.Popen(invocation,stdout=stdout,stderr=stderr)
        try:
            q.wait_replica(spec,cfg)
            command(q.service(spec['publisher'].removesuffix('.service'),spec['reporter'],Path(spec['reporter'])/'publish_bulk_worker.py',[],cfg['stop_epoch']))
            state['status']='running_early_production';save()
            while process.poll() is None:
                verify(plan,path,pin);latest=desired(request)
                if STOP or (ROOT/'STOP_EARLY').exists() or desired_changed(request,latest):
                    request_phase_drain(cfg,request_id='early-time-edit-'+uuid.uuid4().hex)
                state['observed_requested_stop_epoch']=latest['stop_epoch'];save();time.sleep(1)
            require(process.returncode==0,'Early native systemd service did not finish successfully')
        finally:
            stdout.close();stderr.close()
        previous=lastseal;lastseal,row=seal(spec,cfg,grant,q,previous)
        drain=load(worker/'boundary_settings.py').read_drain(cfg)
        if drain:
            atomic(Path(grant).parent/'DRAIN_ACK-ada.json',dict(status='drained',host='ada',
                request_id=drain['request_id'],participants=drain['participants'],grant_sha256=cfg['suballocation_grant_sha256'],
                drain_file_sha256=drain['drain_file_sha256'],old_admission_fenced=True,
                compute_child_resource_leases_released=True,seal_file=str(lastseal),seal_sha256=sha(lastseal)),exclusive=True)
        for name in (spec['publisher'],spec['collector'],cfg['deadline_service_name'].replace('.service','.timer')):
            stop_owned(name)
        reference=dict(parent_run=row['parent_run'],checkpoint_sha256=row['checkpoint_sha256'],raw_sha256=row['raw_sha256'],
            audit_file=row['audit_file'],audit_sha256=row['audit_sha256'],archive_receipt_file=row['archive_receipt_file'],
            archive_receipt_sha256=row['archive_receipt_sha256'],config_file=row['config_file'],config_sha256=row['config_sha256'],
            same_claim=True,next_patch=row['next_patch'])
        state['completed'].append(dict(seal_file=str(lastseal),seal_sha256=sha(lastseal),next_patch=row['next_patch']))
        state.update(status='early_native_sealed',active=None);save()
    state['status']='early_claim31_complete';save()


def main():
    global STOP
    parser=argparse.ArgumentParser();parser.add_argument('--plan',type=Path,required=True);parser.add_argument('--plan-sha256',required=True)
    args=parser.parse_args();plan=read(args.plan);verify(plan,args.plan,args.plan_sha256)
    lock=(ROOT/'early-controller.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    require(not (ROOT/'STATE.json').exists(),'Existing early state requires explicit reconciliation')
    def stop(*_):
        global STOP
        STOP=True
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    try:run(plan,args.plan,args.plan_sha256)
    except BaseException as error:
        state=read(ROOT/'STATE.json') if (ROOT/'STATE.json').exists() else {}
        current=state.get('active')
        if current:
            try:command(['systemctl','--user','stop',current['service']],25)
            except BaseException:pass
        atomic(ROOT/'FAILURE.json',dict(status='attention_required',error=repr(error)))
        raise
    finally:lock.close()


if __name__=='__main__':main()
