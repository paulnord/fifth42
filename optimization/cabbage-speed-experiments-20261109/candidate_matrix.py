"""Holdout test of the reusable initializer on the actual 16-core allocation."""
import json,statistics,subprocess,sys,time
from fractions import Fraction
from pathlib import Path
r=Path(__file__).resolve().parent;out=r/'results/candidate-matrix';out.mkdir(exist_ok=True)
selection=json.loads((r/'results/width-matrix/frozen-selection.json').read_text())['selection']
rows=[];hits={};signatures={}
for window,num,den in [('low',6,25),('middle',7,20),('high',17,20)]:
    left=Fraction(num,den)+Fraction(2,100000)
    cases=[('reference',8),('recommended',8)]
    if selection[window]!=8:cases.append(('recommended',selection[window]))
    for repeat in range(5):
        order=cases[repeat%len(cases):]+cases[:repeat%len(cases)]
        if repeat%2:order=list(reversed(order))
        for variant,width in order:
            dest=out/f'{window}-{repeat}-{variant}-w{width}'
            matches=sorted(out.glob(dest.name+'-retry-*/result.json'))
            if matches and not (dest/'result.json').exists():dest=matches[-1].parent
            if not (dest/'result.json').exists():
                if dest.exists():dest=out/(dest.name+'-retry-'+str(time.time_ns()))
                command=[sys.executable,str(r/'candidate_probe.py'),'--variant',variant,'--width',str(width),'--workers','16',
                    '--ratio-num',str(left.numerator),'--ratio-den',str(left.denominator),'--output',str(dest)]
                began=time.time();p=subprocess.run(command,capture_output=True,text=True,timeout=180)
                log=dict(command=command,started_epoch=began,finished_epoch=time.time(),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
                (out/(dest.name+'.log.json')).write_text(json.dumps(log,indent=2)+'\n')
                if p.returncode:raise RuntimeError(log)
            x=json.loads((dest/'result.json').read_text());x.update(window_name=window,repeat=repeat)
            if window not in hits:hits[window]=x['hits']
            assert x['hits']==hits[window],(window,variant,width,'different exact hit sets')
            if width==8:
                if window not in signatures:signatures[window]=x['signatures_sha256']
                assert x['signatures_sha256']==signatures[window],'Changed baseline geometry/certificates/packets'
            rows.append({k:v for k,v in x.items() if k not in ['stages','records']})
            (out/'progress.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(window,repeat,variant,width,round(x['steady_seconds'],6),flush=True)
summary={}
for window in ['low','middle','high']:
    group=[x for x in rows if x['window_name']==window]
    baseline=statistics.median(x['steady_seconds'] for x in group if x['variant']=='reference')
    med={}
    for variant,width in sorted(set((x['variant'],x['width']) for x in group)):
        samples=[x['steady_seconds'] for x in group if x['variant']==variant and x['width']==width]
        value=statistics.median(samples);med[f'{variant}-w{width}']=dict(median_seconds=value,throughput_ratio=baseline/value,samples=samples)
    summary[window]=med
(out/'summary.json').write_text(json.dumps(dict(status='passed',workers=16,summary=summary,rows=rows,selection=selection,
    timing='Fresh adaptive saved-root preparation and exact certification; bounded prefetch; original CUDA engine; exact checks; first-chunk full GMP audit; local durable commits. Startup/recovery separate.',
    geometry='Original width-8 geometry/certificate/packet identities preserved by reusable initializer. Width choices frozen on training region, tested on a second disjoint holdout with identical exact region per case.'),indent=2)+'\n')
