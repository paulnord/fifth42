#!/usr/bin/env python3
"""Same bounded workload at different worker counts; never adopted as coverage."""
import concurrent.futures,json,os,resource,subprocess,threading,time
from pathlib import Path
import run_parallel as runner
ROOT=Path(__file__).resolve().parent
prior=json.loads((ROOT.parent/'four133_3000000/audit_production_report.json').read_text())
assert prior['complete'] and prior['checked_chunks']==180 and prior['exact_solutions']==[]
sha,binary_sha=runner.build();B=4000000;old=3000000;m=2305843009213693921;S=4206972;H=runner.max_gap('31pos',B,S)
config=dict(bound=B,previous_bound=old,test_mode=False,source_sha=sha)
work=[dict(branch='31pos',modulus=m,normalized_sum=S,max_gap=H,start=1+i*256,end=(i+1)*256) for i in range(9)]
root=ROOT/'benchmark';root.mkdir(exist_ok=True)
def rss(pid):
    try:
        for s in Path(f'/proc/{pid}/status').read_text().splitlines():
            if s.startswith('VmRSS:'):return int(s.split()[1])
    except (FileNotFoundError,ProcessLookupError):pass
    return 0
results=[]
for workers in [1,2,4,9]:
    directory=root/f'workers_{workers}';directory.mkdir(exist_ok=True);active=set();lock=threading.Lock();stop=threading.Event();peak=[0,0]
    def monitor():
        while not stop.wait(.05):
            with lock:pids=list(active)
            peak[0]=max(peak[0],sum(rss(pid) for pid in pids));peak[1]=max(peak[1],len(pids))
    def run(spec):
        p=directory/f"h{spec['start']:05d}_{spec['end']:05d}.log"
        cmd=[str(ROOT/'search133_incremental'),'31pos',str(B),str(old),str(m),str(spec['start']),str(spec['end']),sha]
        with p.open('w') as f:
            child=subprocess.Popen(cmd,stdout=f)
            with lock:active.add(child.pid)
            try:code=child.wait()
            finally:
                with lock:active.discard(child.pid)
        if code:raise RuntimeError(f'Benchmark child returned {code}')
        return runner.validate_chunk(p,spec,config)
    print('BENCHMARK_START workers=',workers,flush=True);before=resource.getrusage(resource.RUSAGE_CHILDREN);t=time.monotonic();thread=threading.Thread(target=monitor);thread.start()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:records=list(pool.map(run,work))
    finally:stop.set();thread.join()
    elapsed=time.monotonic()-t;after=resource.getrusage(resource.RUSAGE_CHILDREN);cpu=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime)
    result=dict(workers=workers,chunks=len(records),gap_checkpoints=sum(x['checkpoints'] for x in records),left=sum(x['left'] for x in records),right=sum(x['right'] for x in records),raw=sum(x['raw'] for x in records),elapsed_seconds=elapsed,child_cpu_seconds=cpu,average_used_cpu_cores=cpu/elapsed,sampled_children_peak_rss_kib=peak[0],observed_max_concurrent_children=peak[1],maximum_search_process_rss_kib=max(x['rss_kib'] for x in records),entries_per_second=sum(x['left']+x['right'] for x in records)/elapsed)
    results.append(result);print('BENCHMARK_DONE',json.dumps(result),flush=True)
    runner.atomic_json(root/'results.json',dict(coverage_claim=False,production_adoption=False,source_sha=sha,binary_sha=binary_sha,cpu_count=os.cpu_count(),affinity=sorted(os.sched_getaffinity(0)),cases=results))
assert len({(x['left'],x['right'],x['raw'],x['chunks'],x['gap_checkpoints']) for x in results})==1
fastest=max(x['entries_per_second'] for x in results);selected=min(x['workers'] for x in results if x['entries_per_second']>=.95*fastest)
summary=json.loads((root/'results.json').read_text());summary.update(selected_workers=selected,selection_rule='Fewest workers within 5 percent of measured maximum throughput',speedup_over_one=results[0]['elapsed_seconds']/next(x['elapsed_seconds'] for x in results if x['workers']==selected))
runner.atomic_json(root/'results.json',summary);print('SELECTED',json.dumps(summary),flush=True)
