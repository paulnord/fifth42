#!/usr/bin/env python3
"""Finite calibration only; never a production launcher."""
import argparse,json,os,resource,subprocess,time
from pathlib import Path
from math133 import MODULI,cases,total_counts
from audit import digest,validate

ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--bound',type=int,required=True);p.add_argument('--seconds',type=int,default=180);a=p.parse_args()
    assert 4000000<a.bound<=20000000 and 1<=a.seconds<=240
    validation=json.loads((ROOT/'validation.json').read_text());sha=digest(ROOT/'src/search.cpp')
    assert validation['passed'] and validation['source_sha256']==sha and validation['binary_sha256']==digest(ROOT/'search')
    out=ROOT/'calibration'/f'B{a.bound}';out.mkdir(exist_ok=False)
    tasks=[]
    for c in cases(a.bound):
        for m in MODULI:
            for index,fraction in enumerate((.05,.5,.95)):
                lo=max(1,min(c.H-63,round(c.H*fraction)));hi=min(c.H,lo+63)
                tasks.append((c,m,lo,hi,index))
    start=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN);active={};records=[];pending=iter(tasks);done=False;peak=0
    try:
        while active or not done:
            if time.monotonic()-start>a.seconds:raise TimeoutError('finite calibration budget reached')
            while len(active)<16 and not done:
                task=next(pending,None)
                if task is None:done=True;break
                c,m,lo,hi,index=task;path=out/f'{c.name}_m{m}_sample{index}.log';stream=path.open('x')
                cmd=[str(ROOT/'search'),c.pattern,str(a.bound),'4000000',str(m),str(c.S),str(c.sign),str(lo),str(hi),sha,'production','100000']
                child=subprocess.Popen(cmd,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
                active[child.pid]=(child,stream,path,task)
            rss=0
            for pid,(child,stream,path,task) in list(active.items()):
                try:
                    line=next(x for x in Path(f'/proc/{pid}/status').read_text().splitlines() if x.startswith('VmRSS:'))
                    rss+=int(line.split()[1])
                except (FileNotFoundError,StopIteration,ProcessLookupError):pass
                if child.poll() is None:continue
                stream.close();del active[pid];assert child.returncode==0,path
                c,m,lo,hi,index=task
                r=validate(path,a.bound,4000000,c,m,lo,hi,sha);r.pop('checkpoints')
                assert not r['exact'],'exact candidate: stop and inspect'
                records.append(dict(case=c.name,modulus=m,start=lo,end=hi,path=str(path.relative_to(ROOT)),**r))
            peak=max(peak,rss);time.sleep(.02)
    finally:
        for child,stream,path,task in active.values():
            child.terminate();child.wait(timeout=10);stream.close()
    elapsed=time.monotonic()-start;after=resource.getrusage(resource.RUSAGE_CHILDREN);predictions=[]
    for c in cases(a.bound):
        rs=[r for r in records if r['case']==c.name]
        sample_entries=sum(r['totals']['left']+r['totals']['right'] for r in rs)
        sample_compute=sum(r['wall_seconds']-r['setup_seconds'] for r in rs)
        expected=total_counts(a.bound,4000000,c)
        all_entries=sum(expected)*2
        compute_seconds=sample_compute/sample_entries*all_entries if sample_entries else 0
        setups=2*((c.H+1023)//1024)*sum(r['setup_seconds'] for r in rs)/len(rs)
        predictions.append(dict(case=c.name,H=c.H,expected_left_per_modulus=expected[0],expected_right_per_modulus=expected[1],sample_entries=sample_entries,sample_compute_seconds=sample_compute,predicted_child_wall_seconds=compute_seconds+setups))
    result=dict(bound=a.bound,previous_bound=4000000,workers=16,complete=True,unique_gap_cases=sum(r['end']-r['start']+1 for r in records),wall_seconds=elapsed,child_cpu_seconds=(after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime),peak_combined_rss_mib=peak/1024,predicted_production_seconds=sum(x['predicted_child_wall_seconds'] for x in predictions)/16,source_sha256=sha,binary_sha256=digest(ROOT/'search'),predictions=predictions,chunks=records)
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('chunks','predictions')},indent=2))

if __name__=='__main__':main()
