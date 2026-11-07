"""Exercise real new chunks, signal stop and deadline stop in separate fresh outputs."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'config.json').read_text())


def require(value,message):
    if not value:raise RuntimeError(message)


def audit(output):
    state=json.loads((output/'checkpoint.json').read_text());raw=(output/'coverage.jsonl').read_bytes()
    require(len(raw)==state['journal_offset'],'Validation run has trailing or missing journal bytes')
    previous='0'*64;sequence=points=patches=0;cursor=BASE['initial_patch']
    for line in raw.splitlines(keepends=True):
        require(line.endswith(b'\n'),'Partial committed record')
        row=json.loads(line);digest=row.pop('sha256')
        require(row['previous_sha256']==previous and row['sequence']==sequence+1,'Invalid chain order')
        require(hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()==digest,'Invalid record digest')
        require(row['window']['first']==cursor and row['window']['last']==cursor+256,'Noncontiguous forward commit')
        require([p[0] for p in row['patches']]==list(range(cursor,cursor+256)),'Wrong patch manifest')
        require(row['independent_gmp_audited'] is True,'Bounded validation omitted independent audit')
        for index,batch in enumerate(row['batches']):
            reference=json.loads((output/'independent-audits'/f'{sequence+1:08d}-{index}.json').read_text())
            ids=batch['patch_ids']
            counts=sorted([ids[c['id']],c['expected'],c['visited']] for c in reference['counts'])
            records=sorted([ids[h['task']],h['linear'],h['a'],h['b'],h['c']] for h in reference['hits'])
            require(counts==batch['native_counts'] and records==batch['native_hit_records'],'GMP/native record mismatch')
        sequence+=1;points+=row['points'];patches+=256;cursor+=256;previous=digest
    require((sequence,points,patches,cursor,previous)==(state['chunks'],state['points'],state['patches'],state['next_patch'],state['journal_sha256']),
            'Checkpoint differs from exact committed prefix')
    require(state['completed_bound'] is None,'Selected continuation claimed a full bound')
    return dict(chunks=sequence,patches=patches,next_patch=cursor,points=points,journal_sha256=previous)


def case(name,mode):
    output=ROOT/'validation'/name
    config=dict(BASE,output=str(output),run_id=BASE['run_id']+'-'+name,gmp_audit_period=1,
                test_chunk_limit=8 if mode=='chunks' else None)
    config['stop_epoch']=min(BASE['stop_epoch'],time.time()+(16 if mode=='deadline' else 90))
    config['stop_local']=datetime.fromtimestamp(config['stop_epoch'],ZoneInfo('America/Chicago')).isoformat()
    path=ROOT/(name+'-config.json');path.write_text(json.dumps(config,indent=2)+'\n')
    with (ROOT/(name+'.stdout.txt')).open('x') as stdout,(ROOT/(name+'.stderr.txt')).open('x') as stderr:
        process=subprocess.Popen([sys.executable,'-B',str(ROOT/'packed_worker.py'),'--config',str(path)],stdout=stdout,stderr=stderr)
        try:
            if mode=='signal':
                until=time.monotonic()+25
                while not (output/'checkpoint.json').exists():
                    require(process.poll() is None,'Signal validation worker exited before committing')
                    require(time.monotonic()<until,'No checkpoint appeared before signal test deadline')
                    time.sleep(.05)
                process.send_signal(signal.SIGTERM)
            code=process.wait(timeout=30)
            require(code==0,'Integration worker failed: '+name)
        finally:
            if process.poll() is None:process.kill();process.wait()
    status=json.loads((output/'status.json').read_text());result=audit(output)
    require(status['error'] is None,'Validation status reports failure')
    if mode=='chunks':require(result['chunks']==8 and status['status']=='completed_test','Bounded chunks not completed')
    elif mode=='signal':require(status['status']=='stopped' and 'Stop requested' in status['reason'],'Signal was not handled gracefully')
    else:
        require(status['status']=='stopped' and 'Absolute deadline' in status['reason'],'Absolute deadline did not stop run')
        require(time.time()<config['stop_epoch']+1,'Run exceeded its absolute deadline')
    require(result['chunks']>0,'Integration case did not commit new chunks')
    return dict(name=name,status='passed',reason=status['reason'],**result)


if __name__=='__main__':
    results=[]
    for name,mode in (('smoke-next-chunks','chunks'),('signal-stop','signal'),('deadline-stop','deadline')):
        result=case(name,mode);results.append(result);print(json.dumps(result),flush=True)
    (ROOT/'integration-report.json').write_text(json.dumps(dict(status='passed',cases=results),indent=2)+'\n')
