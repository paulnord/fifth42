import json,os,statistics,subprocess,sys,time
from pathlib import Path
r=Path(__file__).resolve().parent;out=r/'results/host-matrix';out.mkdir(exist_ok=True)
variants=['reference','roots','inverse','combined','serializer','warm']
windows=[('low',6,25),('middle',7,20),('high',17,20)]
rows=[];signatures={};hits={};start=time.monotonic()
for window,num,den in windows:
    for repeat in range(5):
        order=variants[repeat%len(variants):]+variants[:repeat%len(variants)]
        if repeat%2:order=list(reversed(order))
        for variant in order:
            dest=out/f'{window}-{repeat}-{variant}'
            command=[sys.executable,str(r/'host_probe.py'),'--variant',variant,'--patches','2048','--ratio-num',str(num),'--ratio-den',str(den),'--output',str(dest)]
            if not (dest/'result.json').exists():
                # Preserve interrupted attempts and use a fresh directory.
                if dest.exists():dest=out/f'{window}-{repeat}-{variant}-retry-{time.time_ns()}';command[-1]=str(dest)
                began=time.time();p=subprocess.run(command,capture_output=True,text=True,timeout=180)
                log=dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,started_epoch=began,finished_epoch=time.time())
                (out/f'{window}-{repeat}-{variant}-{time.time_ns()}.log.json').write_text(json.dumps(log,indent=2)+'\n')
                if p.returncode:raise RuntimeError(log)
            x=json.loads((dest/'result.json').read_text());x.update(window_name=window,repeat=repeat)
            if variant!='warm':
                if window not in signatures:signatures[window]=x['signatures_sha256']
                assert x['signatures_sha256']==signatures[window],(window,variant,'changed geometry')
            if window not in hits:hits[window]=x['hits']
            assert x['hits']==hits[window],(window,variant,'changed exact hits')
            rows.append({k:v for k,v in x.items() if k not in ['stages','records']})
            (out/'progress.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(window,repeat,variant,round(x['steady_seconds'],6),x['points'],flush=True)
summary={}
for window,_,_ in windows:
    med={v:statistics.median(x['steady_seconds'] for x in rows if x['window_name']==window and x['variant']==v) for v in variants}
    summary[window]={v:dict(median_seconds=med[v],throughput_ratio=med['reference']/med[v],samples=[x['steady_seconds'] for x in rows if x['window_name']==window and x['variant']==v]) for v in variants}
(out/'summary.json').write_text(json.dumps(dict(status='passed',summary=summary,rows=rows,seconds=time.monotonic()-start,
    timing='Fresh preparation/certification, bounded prefetch, GPU execution, full response checks, first-chunk GMP audit, durable local journal commits. Startup/recovery excluded.',
    controls='Identical geometry/packets for arithmetic/serializer variants; warm basis independently certified and compared to GMP plus nonempty full-domain oracles.',workers=4),indent=2)+'\n')
print(json.dumps(summary,indent=2),flush=True)
