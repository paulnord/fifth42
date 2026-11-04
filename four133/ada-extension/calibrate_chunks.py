#!/usr/bin/env python3
"""One finite 16-worker calibration at production chunk size; no continuation."""
import concurrent.futures,json,resource,subprocess,time
from pathlib import Path
from math133 import MODULI,cases
from audit import digest,validate
ROOT=Path(__file__).resolve().parent
def main():
    B=10800000;out=ROOT/'calibration'/'B10800000-long-chunks';out.mkdir(exist_ok=False)
    sha=digest(ROOT/'src/search.cpp');validation=json.loads((ROOT/'validation.json').read_text())
    assert validation['passed'] and validation['source_sha256']==sha
    tasklist=[]
    for c in cases(B):
        if c.pattern=='22' and 4000000<c.S<5000000:
            for m in MODULI:
                for index,fraction in enumerate((.1,.35,.6,.85)):
                    lo=round(c.H*fraction);tasklist.append((c,m,lo,lo+1023,index))
    assert len(tasklist)==16
    def execute(t):
        c,m,lo,hi,index=t;path=out/f'{c.name}_m{m}_sample{index}.log'
        cmd=[str(ROOT/'search'),c.pattern,str(B),'4000000',str(m),str(c.S),str(c.sign),str(lo),str(hi),sha,'production','100000']
        with path.open('x') as stream:subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=150)
        return t,path
    start=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN)
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:finished=list(pool.map(execute,tasklist))
    search_wall=time.monotonic()-start;after=resource.getrusage(resource.RUSAGE_CHILDREN);records=[]
    # Keep independent Python reconciliation outside the timed search interval.
    for (c,m,lo,hi,index),path in finished:
        r=validate(path,B,4000000,c,m,lo,hi,sha);r.pop('checkpoints');assert not r['exact']
        records.append(dict(case=c.name,modulus=m,start=lo,end=hi,**r))
    entries=sum(r['totals']['left']+r['totals']['right'] for r in records)
    result=dict(complete=True,bound=B,workers=16,chunk_size=1024,chunks=16,unique_gap_cases=16384,wall_seconds=search_wall,child_cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,pair_entries=entries,raw_matches=sum(r['totals']['raw'] for r in records),canonical_matches=sum(r['totals']['canonical'] for r in records),source_sha256=sha,binary_sha256=digest(ROOT/'search'),chunks_detail=records)
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='chunks_detail'},indent=2))
if __name__=='__main__':main()
