#!/usr/bin/env python3
"""Run the authorized production stage and retain measured resource information."""
import datetime,json,os,resource,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
log=ROOT/f'execution_{stamp}.log';report=ROOT/f'execution_{stamp}.json'
def rss(pid):
    try:
        for row in Path(f'/proc/{pid}/status').read_text().splitlines():
            if row.startswith('VmRSS:'):return int(row.split()[1])
    except FileNotFoundError:pass
    return 0
def children(pid):
    try:return list(map(int,Path(f'/proc/{pid}/task/{pid}/children').read_text().split()))
    except FileNotFoundError:return []
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
started=utc();t=time.monotonic();peak=0;samples=0
with log.open('w') as out:
    proc=subprocess.Popen(['python',str(ROOT/'run_incremental.py')],stdout=out,stderr=subprocess.STDOUT)
    print('PRODUCTION_PROCESS_STARTED',proc.pid,'at',started,'log',log,flush=True)
    while proc.poll() is None:
        pids=[proc.pid]+children(proc.pid)
        peak=max(peak,sum(rss(p) for p in pids));samples+=1;time.sleep(1)
    code=proc.wait()
ru=resource.getrusage(resource.RUSAGE_CHILDREN)
files=[p for p in ROOT.rglob('*') if p.is_file()]
obj=dict(started_utc=started,ended_utc=utc(),elapsed_seconds=time.monotonic()-t,return_code=code,sampled_driver_plus_child_peak_rss_kib=peak,sample_period_seconds=1,samples=samples,maximum_child_rss_kib=ru.ru_maxrss,child_user_cpu_seconds=ru.ru_utime,child_system_cpu_seconds=ru.ru_stime,directory_logical_bytes=sum(p.stat().st_size for p in files),directory_allocated_bytes=sum(p.stat().st_blocks*512 for p in files),execution_log=log.name)
report.write_text(json.dumps(obj,indent=2)+'\n');print('PRODUCTION_PROCESS_ENDED',json.dumps(obj),flush=True)
raise SystemExit(code)
