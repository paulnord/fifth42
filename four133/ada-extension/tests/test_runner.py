#!/usr/bin/env python3
import json,os,signal,subprocess,sys,tempfile,time
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from math133 import Case,max_gap,counts
from run import CODE,fingerprint,atomic,tasks
from audit import digest

def make_job(parent,name,workers=8,budget=20,B=1000,chunk=3):
    job=parent/name;job.mkdir();(job/'code/src').mkdir(parents=True);(job/'logs').mkdir();(job/'receipts').mkdir()
    for f in CODE:shutil.copy2(ROOT/f,job/'code'/f)
    cs=[Case(p,S,s,max_gap(B,S,s,p)) for p,S,s in (('22',42,1),('22',100,-1),('31',600,1),('31',600,-1))]
    expected=[sum(counts(B,B//2,c,h)[i] for c in cs for h in range(1,c.H+1)) for i in (0,1)]
    config=dict(bound=B,previous_bound=B//2,workers=workers,budget_seconds=budget,chunk_size=chunk,moduli=[43],cases=[c.__dict__ for c in cs],code=fingerprint(),test_mode=True,expected_totals=dict(zip(('left','right'),expected)))
    atomic(job/'config.json',config);return job
def command(job):return [sys.executable,str(job/'code/run.py'),'coordinate','--job',str(job)]
def invoke(job,ok=True):
    p=subprocess.run(command(job),capture_output=True,text=True,timeout=30)
    assert (p.returncode==0)==ok,(p.stdout,p.stderr)
    return json.loads((job/'progress.json').read_text())

def main():
    start=time.monotonic();checks=[]
    with tempfile.TemporaryDirectory() as temp:
        parent=Path(temp)
        reference=None
        for workers in (1,8,16):
            job=make_job(parent,f'w{workers}',workers)
            state=invoke(job);assert state['status']=='complete' and state['full_box_complete']
            signature={p.name:json.loads(p.read_text())['totals'] for p in (job/'receipts').glob('*.json')}
            if reference is None:reference=signature
            else:assert signature==reference
            assert state['totals']['canonical']>0
            # Resume a completed job and preserve every completed byte.
            before={str(p):digest(p) for p in (job/'logs').glob('*.log')}
            assert invoke(job)['status']=='complete'
            assert before=={str(p):digest(p) for p in (job/'logs').glob('*.log')}
            checks.append(f'complete and resume at {workers} workers')
        job=make_job(parent,'stop');(job/'STOP').touch();s=invoke(job)
        assert s['status']=='stopped' and s['completed_chunks']==0
        (job/'STOP').unlink();assert invoke(job)['status']=='complete';checks.append('STOP and resume')
        # A crash between log rename and receipt commit is recoverable.
        receipt=next((job/'receipts').glob('*.json'));receipt.unlink();assert invoke(job)['status']=='complete';checks.append('adopt validated log after commit interruption')
        log=next((job/'logs').glob('*.log'));log.write_text(log.read_text().replace('CHECKPOINT h=1 ','CHECKPOINT h=999999 ',1))
        # Select a known change even if this particular chunk starts later than h=1.
        log.write_text(log.read_text()+'TAMPER\n')
        assert invoke(job,False)['status']=='failed';checks.append('reject changed completed log')
        job=make_job(parent,'missing-log');assert invoke(job)['status']=='complete'
        next((job/'logs').glob('*.log')).unlink();assert invoke(job,False)['status']=='failed';checks.append('reject missing completed log')
        job=make_job(parent,'bad-source');(job/'code/src/search.cpp').write_text('changed')
        p=subprocess.run(command(job),capture_output=True);assert p.returncode!=0;checks.append('reject changed source')
        job=make_job(parent,'budget',budget=.01);s=invoke(job)
        assert s['status']=='time_limit' and not s['full_box_complete'];checks.append('hard budget is partial coverage')
        # Kill an active coordinator and ensure its workers cannot remain orphaned.
        job=make_job(parent,'killed',workers=1,B=1000000,chunk=1000,budget=20)
        stream=(job/'coordinator.log').open('w');p=subprocess.Popen(command(job),stdout=stream,stderr=subprocess.STDOUT)
        until=time.monotonic()+10
        child=None
        while time.monotonic()<until:
            try:
                children=Path(f'/proc/{p.pid}/task/{p.pid}/children').read_text().split()
                if children:child=int(children[0]);break
            except FileNotFoundError:break
            time.sleep(.02)
        assert child is not None,'no worker started'
        # A second coordinator cannot acquire the held lock.
        second=subprocess.run(command(job),capture_output=True,timeout=10);assert second.returncode!=0
        p.kill();p.wait();stream.close();time.sleep(.2)
        status=Path(f'/proc/{child}/status')
        assert not status.exists() or '\nState:\tZ' in status.read_text(),'worker survived coordinator SIGKILL'
        assert list((job/'logs').glob('*.partial')),'interrupted evidence missing'
        checks += ['exclusive coordinator lock','worker dies with coordinator','preserve interrupted partial log']
    result=dict(passed=True,code=fingerprint(),checks=checks,seconds=time.monotonic()-start)
    (ROOT/'runner-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
