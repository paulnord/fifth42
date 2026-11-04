#!/usr/bin/env python3
"""Execute the audited four-million stage with benchmark-selected concurrency."""
import datetime,json,resource,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bench=json.loads((ROOT/'benchmark/results.json').read_text());workers=bench['selected_workers'];assert workers==9
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');log=ROOT/f'execution_{stamp}.log';report=ROOT/f'execution_{stamp}.json'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def descendants(root):
    parent={}
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():continue
        try:
            row=(p/'stat').read_text();rest=row[row.rfind(')')+2:].split();parent[int(p.name)]=int(rest[1])
        except (FileNotFoundError,ProcessLookupError,PermissionError):pass
    seen={root};changed=True
    while changed:
        changed=False
        for pid,ppid in parent.items():
            if ppid in seen and pid not in seen:seen.add(pid);changed=True
    return seen
def rss(pid):
    try:
        for line in Path(f'/proc/{pid}/status').read_text().splitlines():
            if line.startswith('VmRSS:'):return int(line.split()[1])
    except (FileNotFoundError,ProcessLookupError):pass
    return 0
started=utc();t=time.monotonic();peak=0;max_descendants=0;samples=0
with log.open('w') as out:
    p=subprocess.Popen(['python',str(ROOT/'run_parallel.py'),'--workers',str(workers)],stdout=out,stderr=subprocess.STDOUT)
    print('PARALLEL_PRODUCTION_STARTED',p.pid,'workers',workers,'at',started,'log',log,flush=True)
    while p.poll() is None:
        ids=descendants(p.pid);peak=max(peak,sum(rss(i) for i in ids));max_descendants=max(max_descendants,len(ids));samples+=1;time.sleep(.2)
    code=p.wait()
ru=resource.getrusage(resource.RUSAGE_CHILDREN);files=[f for f in ROOT.rglob('*') if f.is_file()]
obj=dict(started_utc=started,ended_utc=utc(),elapsed_seconds=time.monotonic()-t,return_code=code,workers=workers,sampled_coordinator_plus_descendants_peak_rss_kib=peak,maximum_observed_process_count=max_descendants,sample_period_seconds=.2,samples=samples,maximum_child_rss_kib=ru.ru_maxrss,child_user_cpu_seconds=ru.ru_utime,child_system_cpu_seconds=ru.ru_stime,directory_logical_bytes=sum(f.stat().st_size for f in files),directory_allocated_bytes=sum(f.stat().st_blocks*512 for f in files),execution_log=log.name)
report.write_text(json.dumps(obj,indent=2)+'\n');print('PARALLEL_PRODUCTION_ENDED',json.dumps(obj),flush=True)
raise SystemExit(code)
