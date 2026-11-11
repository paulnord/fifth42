"""Frozen Ada memory-r2 queue with exact-prefix recovery and analytic tail stop."""
from pathlib import Path
import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import time

ROOT=Path(__file__).resolve().parent
SHARE=Path('/mnt/nfs_share/fifth42-integration-20261109/combined/range-extension-r3-20261111/ada-memory-r2-20261111')
STATUS=Path('/mnt/nfs_share/ada-preparation-publishing-20261110')
STOP=ROOT/'STOP_MEMORY_R2'

def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def atomic(p,row):
    p=Path(p);temp=p.with_suffix('.tmp');temp.write_text(json.dumps(row,indent=2,sort_keys=True)+'\n');os.replace(temp,p)

def load_helpers(admission):
    p=Path(admission['queue_helper']['path'])
    require(sha(p)==admission['queue_helper']['sha256'],'Reviewed queue helper changed')
    spec=importlib.util.spec_from_file_location('_ada_memory_r2_queue_helpers',p)
    q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
    # Reuse the unchanged launch/replica/publication/audit helpers with this
    # independently frozen queue's state, audit directory and explicit stop file.
    q.ROOT=ROOT;q.STOP=STOP
    return q

def verify(admission,pin):
    require(sha(ROOT/'ADMISSION-v2.json')==pin,'Memory-r2 admission changed')
    require(sha(__file__)==admission['controller_sha256'],'Memory-r2 controller changed')
    for name,digest in admission['original_r3_pins'].items():
        require(sha(Path(admission['r3_directory'])/name)==digest,'Original r3 evidence changed: '+name)
    for name,digest in admission['review_evidence_sha256'].items():
        require(sha(ROOT/name)==digest,'Frozen review evidence changed: '+name)
    for name,digest in admission.get('current_publisher_sources_sha256',{}).items():
        require(sha(name)==digest,'Reviewed current publisher adapter changed: '+name)
    proof=read(ROOT/'ANALYTIC-TAIL-ADMISSION.json')
    require(proof['status']=='approved_analytic_exclusion' and proof['analytic_interval']==[10881882043,11250000001]
            and proof['native_stop_threshold']==10881882112,'Unexpected analytic tail admission')
    require(sha(Path(proof['source_certificate']))==proof['source_certificate_sha256'],'Analytic source certificate changed')
    return proof

def verify_stage(spec):
    c=read(spec['config']);w=Path(spec['worker'])
    require(sha(spec['config'])==spec['config_sha256'] and sha(w/'release-manifest.json')==spec['manifest_sha256']==c['manifest_sha256'],
            'Frozen stage configuration/manifest changed')
    for name,digest in read(w/'release-manifest.json')['files'].items():
        require(sha(w/name)==digest,'Frozen stage source changed: '+name)
    for name,digest in spec['root_files_sha256'].items():
        require(sha(Path(spec['root'])/name)==digest,'Frozen stage preparation input changed: '+name)
    return c

def tail_trigger(cp,threshold):
    return cp is not None and type(cp.get('next_patch')) is int and cp['next_patch']>=threshold

def previous_binding(q,previous):
    """An already retired predecessor needs no repeated systemd stop."""
    if previous:
        states=[q.unit(previous[k]) for k in ('publisher','collector')]
        if all(s['ActiveState']=='inactive' and s['MainPID']=='0' for s in states):return None
    return previous

def adoption_matches(spec,c,live,owner):
    return (owner.get('ActiveState')=='active' and int(owner.get('MainPID','0'))>0 and
            live.get('run_id')==c['run_id'] and live.get('config_sha256')==spec['config_sha256'] and
            live.get('manifest_sha256')==c['manifest_sha256'] and
            live.get('phase')=='running' and live.get('alerts')==[])

def terminal_prefix_valid(owner,supervisor,native,cp,c,threshold):
    require(owner['ActiveState']=='inactive' and owner['MainPID']=='0','Tail compute owner has not exited')
    require(supervisor.get('error') is None and supervisor.get('worker_exit_code')==0 and supervisor.get('leases_released') is True,
            'Tail supervisor did not finish cleanly')
    require(native.get('status')=='stopped' and native.get('error') is None and
            native['journal_buffer']['pending_chunks']==native['journal_buffer']['pending_bytes']==0,'Tail has pending/failed records')
    require(c['initial_patch']<threshold<=cp['next_patch']<=c['range_end'] and
            cp['patches']==cp['next_patch']-c['initial_patch'],'Tail prefix skipped or overcounted cells')

def startup_readback(q,c):
    until=time.monotonic()+120
    while time.monotonic()<until:
        p=STATUS/'ada-publisher-readiness.json'
        if p.exists():
            d=read(p);push=d.get('latest_push',{});check=d.get('latest_readback',{})
            if push.get('run_id')==c['run_id'] and push.get('phase')=='running' and check.get('status')=='passed' and check.get('commit')==push.get('commit'):
                return dict(commit=push['commit'],readback=check)
        require(q.unit(c['service_name'])['ActiveState']=='active','New worker stopped before verified startup publication')
        time.sleep(1)
    raise TimeoutError('New runtime lacks exact startup GitHub readback')

def main(pin):
    require(os.uname().nodename.split('.')[0]=='ada','Controller belongs on physical Ada')
    lock=(ROOT/'controller.lock').open('a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    require(not(ROOT/'STATE-v2.json').exists(),'Existing controller state requires explicit reconciliation')
    a=read(ROOT/'ADMISSION-v2.json');proof=verify(a,pin);q=load_helpers(a)
    state=dict(status='starting',generation='ada-memory-r2-20261111',stop_epoch=a['stop_epoch'],
        admission_sha256=pin,active=None,completed=[],sealed_recovery_prefix=a['sealed_recovery_prefix'],
        analytic_tail_status='armed_not_yet_reached',error=None)
    def save():
        state['updated_epoch']=time.time();atomic(ROOT/'STATE-v2.json',state);atomic(SHARE/'STATE.json',state)
        atomic(Path(a['r3_directory'])/'ADA_QUEUE_STATUS.json',state)
    previous=a['previous'];save()
    try:
        for index,spec in enumerate(a['stages']):
            verify(a,pin);c=verify_stage(spec)
            if STOP.exists() or time.time()>=a['stop_epoch']-120:
                state['status']='stopped_at_original_deadline_or_request';save();return
            adopting=index==0 and a.get('adopt_first_running_stage') is True
            if adopting:
                live=read(STATUS/'status.json')
                require(adoption_matches(spec,c,live,q.unit(c['service_name'])),
                        'Live worker differs from the byte-exact admitted adoption')
                state.update(status='adopting_verified_running_stage',active=spec);save()
            else:
                require(not Path(c['output']).exists() and not Path(c['replica_output']).exists(),'Existing output cannot be resumed automatically')
                state.update(status='launching',active=spec);save()
                require(q.launch(spec,c,previous_binding(q,previous)),'Explicit stop prevented launch')
            state.update(status='running',startup_publication=startup_readback(q,c));save()
            analytic_stop=False
            while q.unit(c['service_name'])['ActiveState'] in ('active','activating','deactivating'):
                cp_path=Path(c['output'])/'checkpoint.json'
                cp=read(cp_path) if cp_path.exists() else None
                if c['initial_patch']<proof['native_stop_threshold']<c['range_end'] and tail_trigger(cp,proof['native_stop_threshold']):
                    verify(a,pin);analytic_stop=True
                    state['analytic_tail_status']='stopping_at_verified_crossing_window';save()
                    q.command(['systemctl','--user','stop',c['service_name']],timeout=20)
                elif STOP.exists() or time.time()>=a['stop_epoch']-10:
                    q.command(['systemctl','--user','stop',c['service_name']],timeout=20)
                save();time.sleep(.25)
            cp=q.wait_replica(spec,c,final=True)
            sup=read(Path(spec['worker'])/'supervisor-report.json');native=read(Path(c['output'])/'status.json')
            if STOP.exists() or time.time()>=a['stop_epoch']-10:
                state['status']='stopped_at_original_deadline_or_request';save();return
            if analytic_stop:terminal_prefix_valid(q.unit(c['service_name']),sup,native,cp,c,proof['native_stop_threshold'])
            else:q.terminal_is_clean(q.unit(c['service_name']),sup,native,cp,c)
            q.settle_publication(spec,c,cp)
            archive=q.archive(spec,c,cp);state['completed'].append(archive);previous=spec;state['active']=None;save()
            if analytic_stop:
                receipt=dict(schema='fifth42-ada-native-and-analytic-tail-completion-v1',status='verified',
                    completed_epoch=time.time(),native_run=c['run_id'],native_checkpoint_sha256=q.sha(Path(c['output'])/'checkpoint.json'),
                    native_interval=[c['initial_patch'],cp['next_patch']],native_archive=archive,
                    analytic_interval=proof['analytic_interval'],analytic_proof_sha256=proof['source_certificate_sha256'],
                    overlapping_native_and_analytic_cells=cp['next_patch']-proof['analytic_interval'][0],
                    skipped_native_cells=proof['analytic_interval'][1]-cp['next_patch'],analytic_native_visits=0,
                    grant_and_claims_unchanged=True,whole_shell_cap100_claim=False)
                atomic(ROOT/'TAIL-COMPLETION.json',receipt);atomic(SHARE/'TAIL-COMPLETION.json',receipt)
                state.update(status='native_work_complete_with_verified_analytic_tail',analytic_tail_status='integrated_verified',tail_completion=receipt)
                save();return
        raise RuntimeError('Queue ended before recording its analytic tail stop')
    except BaseException as error:
        state.update(status='attention_required',error=repr(error));save();raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--admission-sha256',required=True);main(p.parse_args().admission_sha256)
