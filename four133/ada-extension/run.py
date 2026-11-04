#!/usr/bin/env python3
"""Frozen-source, independently reconciled, resumable CPU shell with a hard budget."""
import argparse,ctypes,fcntl,hashlib,json,os,resource,signal,subprocess,sys,time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import shutil
from math133 import Case,MODULI,cases,total_counts
from audit import digest,validate

ROOT=Path(__file__).resolve().parent
CODE=('run.py','math133.py','audit.py','src/search.cpp','PROOF.md','search')
def fingerprint(root=ROOT):return {f:digest(root/f) for f in CODE}
def utc():return datetime.now(timezone.utc).isoformat()
def atomic(path,value):
    temp=path.with_name(path.name+'.tmp')
    with temp.open('w') as f:
        json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def config_hash(c):return hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()
def syncdir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def tasks(config):
    out=[]
    for row in config['cases']:
        c=Case(**row)
        for lo in range(1,c.H+1,config['chunk_size']):
            hi=min(c.H,lo+config['chunk_size']-1)
            # Adjacent moduli keep partial coverage easy to interpret.
            for m in config['moduli']:out.append((f'{c.name}_m{m}_h{lo:07d}_{hi:07d}',c,m,lo,hi))
    return out
def lock(path):
    f=path.open('a+')
    try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:f.close();raise RuntimeError(f'Another coordinator holds {path}')
    return f
def parent_death(parent):
    # Linux guarantees workers die if their coordinator is killed.
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(1,signal.SIGTERM,0,0,0)!=0 or os.getppid()!=parent:os._exit(126)

def coordinate(job):
    job=job.resolve();config=json.loads((job/'config.json').read_text());identity=config_hash(config)
    assert config['code']==fingerprint(job/'code'),'frozen source or binary changed'
    assert 1<=config['workers']<=16 and 0<config['budget_seconds']<=28800
    if not config['test_mode']:
        assert config['workers']==16 and config['previous_bound']==4000000 and config['moduli']==list(MODULI)
        assert config['cases']==[c.__dict__ for c in cases(config['bound'])]
        assert config['prior_verification_sha256']==digest(job/'prior-verification.json')
        prior=json.loads((job/'prior-verification.json').read_text())
        assert prior['verified_bound']==4000000 and prior['frozen_evidence_preserved']
    resource_lock=lock(job.parent/'.resource.lock');job_lock=lock(job/'coordinator.lock')
    all_tasks=tasks(config);done={};totals=Counter();active={};status='starting';failure=None;peak=0;started=time.time();stop_signal=[]
    old_state=json.loads((job/'progress.json').read_text()) if (job/'progress.json').exists() else {}
    cpu_before=resource.getrusage(resource.RUSAGE_CHILDREN)
    started=old_state.get('started_unix',started)
    remaining=max(0,started+config['budget_seconds']-time.time());deadline=time.monotonic()+remaining
    def save():
        usage=resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu=old_state.get('child_cpu_seconds',0)+usage.ru_utime+usage.ru_stime-cpu_before.ru_utime-cpu_before.ru_stime
        coverage={}
        for r in done.values():
            key=f'{r["case"]}_m{r["modulus"]}'
            coverage[key]=coverage.get(key,0)+r['end']-r['start']+1
        atomic(job/'progress.json',dict(status=status,started_at=datetime.fromtimestamp(started,timezone.utc).isoformat(),started_unix=started,updated_at=utc(),budget_seconds=config['budget_seconds'],elapsed_seconds=time.time()-started,child_cpu_seconds=cpu,bound=config['bound'],previous_bound=config['previous_bound'],workers=config['workers'],active_workers=len(active),active_pids=list(active),coordinator_pid=os.getpid(),completed_chunks=len(done),expected_chunks=len(all_tasks),completed_gap_cases=sum(r['end']-r['start']+1 for r in done.values()),expected_gap_cases=sum(hi-lo+1 for _,_,_,lo,hi in all_tasks),coverage_by_case_and_modulus=coverage,totals=dict(totals),peak_combined_rss_mib=max(old_state.get('peak_combined_rss_mib',0),peak/1024),config_sha256=identity,error=failure,full_box_complete=status=='complete',old_box_verified=not config['test_mode']))
    def interrupted(signum,frame):stop_signal.append(signum)
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,interrupted)
    try:
        # Reconcile completed chunks again on every resume; never trust a checkpoint alone.
        for name,c,m,lo,hi in all_tasks:
            receipt=job/'receipts'/f'{name}.json';log=job/'logs'/f'{name}.log'
            if not receipt.exists():
                if not log.exists():continue
                r=validate(log,config['bound'],config['previous_bound'],c,m,lo,hi,config['code']['src/search.cpp'],config['test_mode']);r.pop('checkpoints')
                r.update(config_sha256=identity,start=lo,end=hi,case=c.name,modulus=m)
                atomic(receipt,r)
            r=json.loads(receipt.read_text());assert r['config_sha256']==identity and r['sha256']==digest(log),'changed completed log'
            fresh=validate(log,config['bound'],config['previous_bound'],c,m,lo,hi,config['code']['src/search.cpp'],config['test_mode'])
            assert r['totals']==fresh['totals'] and r['candidates']==fresh['candidates']
            done[name]=r;totals.update(r['totals'])
        pending=iter(t for t in all_tasks if t[0] not in done);exhausted=len(done)==len(all_tasks);status='running';save();last_save=time.monotonic()
        while active or not exhausted:
            if time.monotonic()>=deadline-min(20,config['budget_seconds']/10):status='time_limit';break
            if stop_signal or (job/'STOP').exists():status='stopped';break
            while len(active)<config['workers'] and not exhausted:
                task=next(pending,None)
                if task is None:exhausted=True;break
                name,c,m,lo,hi=task;attempt=0
                while (job/'logs'/f'{name}.attempt{attempt}.partial').exists():attempt+=1
                path=job/'logs'/f'{name}.attempt{attempt}.partial';stream=path.open('x');parent=os.getpid()
                cmd=[str(job/'code/search'),c.pattern,str(config['bound']),str(config['previous_bound']),str(m),str(c.S),str(c.sign),str(lo),str(hi),config['code']['src/search.cpp'],'synthetic' if config['test_mode'] else 'production','100000']
                child=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=lambda:parent_death(parent))
                active[child.pid]=(child,stream,path,task)
            rss=0
            for pid,(child,stream,path,task) in list(active.items()):
                try:rss+=int(next(x for x in Path(f'/proc/{pid}/status').read_text().splitlines() if x.startswith('VmRSS:')).split()[1])
                except (FileNotFoundError,StopIteration,ProcessLookupError):pass
                if child.poll() is None:continue
                stream.flush();os.fsync(stream.fileno());stream.close();del active[pid]
                assert child.returncode==0,f'Worker failed ({child.returncode}): {path}'
                name,c,m,lo,hi=task;r=validate(path,config['bound'],config['previous_bound'],c,m,lo,hi,config['code']['src/search.cpp'],config['test_mode']);r.pop('checkpoints')
                r.update(config_sha256=identity,start=lo,end=hi,case=c.name,modulus=m)
                final=job/'logs'/f'{name}.log';assert not final.exists();os.rename(path,final);syncdir(final.parent)
                atomic(job/'receipts'/f'{name}.json',r);done[name]=r;totals.update(r['totals'])
                if r['exact']:status='exact_candidate';break
            peak=max(peak,rss)
            if status=='exact_candidate':break
            if time.monotonic()-last_save>=5:save();last_save=time.monotonic()
            time.sleep(.05)
        else:status='complete'
        if status=='complete':
            assert len(done)==len(all_tasks)
            for name,c,m,lo,hi in all_tasks:
                assert done[name]['sha256']==digest(job/'logs'/f'{name}.log')
            expected=config['expected_totals']
            assert totals['left']==expected['left'] and totals['right']==expected['right']
    except BaseException as error:
        status='failed';failure=f'{type(error).__name__}: {error}'
    finally:
        for child,stream,path,task in active.values():
            try:os.killpg(child.pid,signal.SIGTERM)
            except ProcessLookupError:pass
        until=time.monotonic()+5
        for child,stream,path,task in active.values():
            try:child.wait(timeout=max(.01,until-time.monotonic()))
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGKILL);child.wait()
            stream.close()
        active.clear();save();resource_lock.close();job_lock.close()
    print(json.dumps(dict(status=status,job=str(job),completed_chunks=len(done),expected_chunks=len(all_tasks),error=failure)),flush=True)
    return 1 if status=='failed' else 0

def launch():
    launch_lock=lock(ROOT/'jobs'/'.launch.lock')
    if (ROOT/'jobs/latest.json').exists():
        raise RuntimeError('A job has already been launched. Use run.py status; resume that job rather than launching a duplicate.')
    plan=json.loads((ROOT/'plan.json').read_text());assert plan['budget_seconds']==28800 and plan['workers']==16
    validation=json.loads((ROOT/'validation.json').read_text());driver=json.loads((ROOT/'runner-validation.json').read_text())
    baseline=json.loads((ROOT/'baseline-validation.json').read_text())
    code=fingerprint();assert driver['passed'] and driver['code']==code
    assert validation['passed'] and validation['source_sha256']==code['src/search.cpp'] and validation['binary_sha256']==code['search']
    assert baseline['passed'] and baseline['source_sha256']==code['src/search.cpp'] and baseline['reference_source_sha256']=='30365331b8f9e0cde8471b843c3ca38b695417d8dfc8c4c9df25cd0fee968f24'
    assert plan['code']==code and plan['calibration_sha256']==digest(ROOT/plan['calibration'])
    # Recheck preserved evidence immediately before making a launchable snapshot.
    subprocess.run([sys.executable,str(ROOT/'verify_prior.py')],check=True)
    # A second invocation reports an active job instead of launching duplicate work.
    existing=lock(ROOT/'jobs'/'.resource.lock')
    existing.close()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');job=ROOT/'jobs'/f'B{plan["bound"]}-{stamp}'
    job.mkdir();(job/'code/src').mkdir(parents=True);(job/'logs').mkdir();(job/'receipts').mkdir()
    for name in CODE:shutil.copy2(ROOT/name,job/'code'/name)
    for name in ('prior-verification.json','validation.json','baseline-validation.json','runner-validation.json','plan.json'):shutil.copy2(ROOT/name,job/name)
    config=dict(bound=plan['bound'],previous_bound=4000000,workers=16,budget_seconds=28800,chunk_size=1024,moduli=list(MODULI),cases=[c.__dict__ for c in cases(plan['bound'])],code=code,test_mode=False,prior_verification_sha256=digest(job/'prior-verification.json'),expected_totals=plan['expected_totals'],created_at=utc())
    atomic(job/'config.json',config)
    with (job/'coordinator.log').open('xb') as stream:
        child=subprocess.Popen([sys.executable,str(job/'code/run.py'),'coordinate','--job',str(job)],stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
    atomic(ROOT/'jobs/latest.json',dict(job=str(job),coordinator_pid=child.pid,launched_at=utc()))
    time.sleep(1)
    assert child.poll() is None,f'Coordinator exited; inspect {job}/coordinator.log'
    print(f'Launched {job}\nCoordinator PID: {child.pid}\n16 CPU workers; eight-hour hard cap.\nStatus: python3 {ROOT}/run.py status')
    launch_lock.close()

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('launch','coordinate','status'));p.add_argument('--job',type=Path);a=p.parse_args()
    if a.action=='launch':launch();return 0
    job=a.job
    if job is None:job=Path(json.loads((ROOT/'jobs/latest.json').read_text())['job'])
    if a.action=='status':print((job/'progress.json').read_text());return 0
    return coordinate(job)

if __name__=='__main__':sys.exit(main())
