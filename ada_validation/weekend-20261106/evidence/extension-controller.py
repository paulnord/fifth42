"""Ada sharing queue for claims30,31,34; existing R5 parent remains untouched.

Fresh per-stage child grants pin the prepared source. A desired-time edit drains
the current child at its durable batch, audits/publishes it, then pauses for a
new coordinator-issued deadline grant; no future old-deadline child is started.
"""
from datetime import datetime,timezone
from pathlib import Path
import argparse,fcntl,hashlib,importlib.util,json,os,subprocess,time,traceback

ROOT=Path(__file__).resolve().parent
PY='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
JOBS=['boole-delegated-20261109-'+str(n) for n in (30,31,34)]


def require(value,message):
    if not value:raise RuntimeError(message)
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,v):
    p=Path(p);p.parent.mkdir(mode=0o700,parents=True,exist_ok=True);temp=p.with_name(p.name+'.'+str(os.getpid())+'.tmp')
    with temp.open('w') as f:json.dump(v,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(temp,p)
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def command(args,timeout=90):
    p=subprocess.run(args,text=True,capture_output=True,timeout=timeout)
    require(p.returncode==0,repr(args)+' '+p.stderr[-4000:]);return p.stdout

def verify_plan(plan,path,pin):
    require(sha(path)==pin,'Sharing queue plan changed')
    require(plan['schema']=='fifth42-ada-sharing-queue-v1' and plan['jobs']==JOBS,'Unreviewed Ada queue scope/order')
    for p,h in plan['source_files'].items():require(sha(p)==h,'Pinned queue input changed: '+p)
    m=read(plan['ownership_file'])
    require(m['status']=='admitted' and all(m['executors'][job]=='ada' for job in JOBS),'Ownership differs from Ada queue')
    require(m['stop_epoch']==plan['parent_stop_epoch'],'Queue changed parent cutoff')
    return m

def effective_request(plan,previous,boundary):
    try:value=boundary.read_request(plan['settings_file'])
    except (OSError,ValueError,TypeError):return previous
    return dict(value,effective_stop_epoch=min(value['stop_epoch'],plan['parent_stop_epoch']))

def request_drain(cfg,request_id,reason):
    path=Path(cfg['suballocation_grant_file']).parent/'DRAIN-ada.json'
    value=dict(status='draining',host='ada',participants=['ada'],grant_sha256=cfg['suballocation_grant_sha256'],request_id=request_id,reason=reason)
    if path.exists():require(read(path)==value,'Another child drain request already exists')
    else:atomic(path,value)
    return dict(value,drain_file_sha256=sha(path))

def terminal(q,spec,cfg):
    owner=q.unit(cfg['service_name']);out=Path(cfg['output']);sup=read(Path(spec['worker'])/'supervisor-report.json');native=read(out/'status.json')
    require(owner['ActiveState']=='inactive' and owner['MainPID']=='0' and owner['Result']=='success','Sharing native owner did not exit cleanly')
    require(sup.get('error') is None and sup.get('worker_exit_code')==0 and sup.get('leases_released') is True,'Sharing supervisor failed/retained leases')
    buffer=native.get('journal_buffer')
    require(native.get('status')=='stopped' and native.get('error') is None and (buffer is None or all(buffer.get(k)==0 for k in ('pending_chunks','pending_bytes'))),'Sharing native journal is not cleanly drained')
    cp=read(out/'checkpoint.json');require(cfg['initial_patch']<=cp['next_patch']<=cfg['range_end'] and cp['patches']==cp['next_patch']-cfg['initial_patch'],'Sharing checkpoint escaped exact child interval')
    return cp


def main(path,pin):
    plan=read(path);ownership=verify_plan(plan,path,pin)
    lock=(ROOT/'queue.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    require(not (ROOT/'QUEUE-STATE.json').exists(),'Existing sharing queue state requires explicit reconciliation')
    q=load('sharing_queue_helpers',ROOT/'queue_helpers.py');q.ROOT=ROOT;q.STOP=ROOT/'STOP';q.atomic=atomic
    builder=load('sharing_builder',ROOT/'build_stage.py');issuer=load('sharing_grant_issuer',ROOT/'issue_grant.py');reporter=load('sharing_report_stage',ROOT/'report_stage.py')
    boundary=load('sharing_request_parser',plan['boundary_parser_file'])
    request=dict(stop_epoch=plan['parent_stop_epoch'],effective_stop_epoch=plan['parent_stop_epoch'],stop_local=ownership['stop_local'],setting_sha256=sha(plan['settings_file']))
    state=dict(status='starting',completed=[],active=None,error=None,parent_unchanged=True,plan_sha256=pin)
    def save():
        state['updated_utc']=datetime.now(timezone.utc).isoformat();atomic(ROOT/'QUEUE-STATE.json',state);atomic(Path(plan['shared_directory'])/'ADA-QUEUE-STATUS.json',state)
    previous=None
    try:
        for index,job in enumerate(plan['jobs']):
            ownership=verify_plan(plan,path,pin);request=effective_request(plan,request,boundary)
            if index and (request['effective_stop_epoch']!=plan['parent_stop_epoch'] or request['effective_stop_epoch']<=time.time()+120):
                state.update(status='paused_for_fresh_deadline_delegation',requested=request);save();return
            if index==0:
                bound=read(plan['first_bound_file']);prepared=bound['prepared'];cfg=read(bound['config_file'])
                require(sha(bound['config_file'])==bound['config_sha256'] and cfg['ledger_job']==job,'First running stage binding changed')
            else:
                task=next(t for t in ownership['tasks'] if t['ledger_job']==job)
                prepared=builder.prepare_runtime(task,task['predecessor_seal'],worker_guard_file=ROOT/'sharing_guard.py',worker_guard_sha256=ownership['guard_source_sha256'])
                issued=issuer.issue(plan['ownership_file'],'ada',job,Path(prepared['worker'])/'release-manifest.json','suballocation_guard.py',Path(plan['shared_directory'])/'children'/prepared['run_id']/'GRANT.json')
                cfg=builder.bind_configuration(prepared,issued['file'],deadline_settings_file=plan['effective_settings_file'],inventory_file=plan['inventory_file'],source_review_file=ROOT/'SOURCE-REVIEW.json',previous=previous)
            worker=Path(prepared['worker']);guard=load('sharing_worker_guard_'+str(index),worker/'suballocation_guard.py');guard.check(cfg,force=True)
            if previous:
                for key in ('publisher','collector'):command(['systemctl','--user','stop',previous[key]],20)
            context=dict(plan,adopt_running_run_id=cfg['run_id'] if index==0 else None,plan_file=str(path))
            spec=reporter.prepare(prepared['root'],cfg,context)
            command(q.service(spec['collector'].removesuffix('.service'),spec['reporter'],Path(spec['reporter'])/'collector.py',[],cfg['stop_epoch']))
            if index:
                command(q.service(cfg['run_id']+'-final-copy',spec['root'],worker/'finalize_replica.py',['--config',spec['config'],'--config-sha256',spec['config_sha256']],cfg['stop_epoch']))
                command([PY,'-B',str(worker/'launch_weekend.py'),'--launch'],90)
            state.update(status='running',active=spec);save()
            q.wait_replica(spec,cfg)
            command(q.service(spec['publisher'].removesuffix('.service'),spec['reporter'],Path(spec['reporter'])/'publish_bulk_worker.py',[],cfg['stop_epoch']))
            drain=None
            while q.unit(cfg['service_name'])['ActiveState'] in ('active','activating','deactivating'):
                verify_plan(plan,path,pin);request=effective_request(plan,request,boundary)
                if drain is None and (request['effective_stop_epoch']!=cfg['stop_epoch'] or (ROOT/'STOP').exists()):
                    drain=request_drain(cfg,'sharing-deadline-'+str(int(time.time())), 'Operator end time edit or explicit sharing queue stop')
                    state.update(status='draining_for_fresh_deadline_delegation',requested=request);save()
                time.sleep(2)
            cp=terminal(q,spec,cfg);q.wait_replica(spec,cfg,final=True);q.settle_publication(spec,cfg,cp);archived=q.archive(spec,cfg,cp)
            state['completed'].append(archived);state['active']=None;save()
            if drain:
                atomic(Path(cfg['suballocation_grant_file']).parent/'DRAIN_ACK-ada.json',dict(status='drained',host='ada',participants=['ada'],request_id=drain['request_id'],grant_sha256=cfg['suballocation_grant_sha256'],boundary_sha256=sha(Path(archived['audit'])),native_next_patch=cp['next_patch'],drain_file_sha256=drain['drain_file_sha256'],old_admission_fenced=True,compute_child_resource_leases_released=True))
            if drain or cp['next_patch']!=cfg['range_end']:
                state.update(status='paused_for_fresh_suffix_or_deadline_delegation',requested=request);save();return
            previous=dict(spec,config=spec['config'],config_sha256=spec['config_sha256'])
        state.update(status='all_assigned_ada_work_complete',active=None);save()
    except BaseException as error:
        state.update(status='attention_required',error=repr(error),traceback=traceback.format_exc());save();raise


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,required=True);p.add_argument('--plan-sha256',required=True);a=p.parse_args();main(a.plan,a.plan_sha256)
