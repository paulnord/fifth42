import json,statistics,subprocess,sys,time
from fractions import Fraction
from pathlib import Path
r=Path(__file__).resolve().parent;out=r/'results/width-matrix';out.mkdir(exist_ok=True)
widths=[8,16,32,64,128];windows=[('low',6,25),('middle',7,20),('high',17,20)]
rows=[];guards=[];hits={};unions={};blocked=set()
def call(window,num,den,width,repeat,variant='combined',label='train'):
    dest=out/f'{label}-{window}-{repeat}-{variant}-w{width}'
    command=[sys.executable,str(r/'host_probe.py'),'--variant',variant,'--width',str(width),'--patches','2048',
             '--ratio-num',str(num),'--ratio-den',str(den),'--output',str(dest)]
    existing=out/(dest.name+'.log.json')
    if existing.exists():
        old=json.loads(existing.read_text())
        if old['exit_code'] and any(x in old['stderr'] for x in ['Patch point allowance mismatch','Full-domain coefficient allowance exhausted','Integer transform can overflow','needs the original sphere fallback']):
            guards.append(dict(window=window,width=width,error=old['stderr'],complete=False));blocked.add((window,width));return None
    if not (dest/'result.json').exists():
        if dest.exists():dest=out/(dest.name+'-retry-'+str(time.time_ns()));command[-1]=str(dest)
        began=time.time();p=subprocess.run(command,capture_output=True,text=True,timeout=180)
        log=dict(command=command,started_epoch=began,finished_epoch=time.time(),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
        existing.write_text(json.dumps(log,indent=2)+'\n')
        if p.returncode:
            if any(x in p.stderr for x in ['Patch point allowance mismatch','Full-domain coefficient allowance exhausted','Integer transform can overflow','needs the original sphere fallback']):
                guards.append(dict(window=window,width=width,error=p.stderr,complete=False));blocked.add((window,width));return None
            raise RuntimeError(log)
    x=json.loads((dest/'result.json').read_text());x.update(window_name=window,repeat=repeat,label=label)
    key=(label,window)
    if key not in hits:hits[key]=x['hits'];unions[key]=(x['ratio_left'],x['ratio_right'])
    assert x['hits']==hits[key] and (x['ratio_left'],x['ratio_right'])==unions[key],'Changed target hit set or exact region'
    rows.append({k:v for k,v in x.items() if k not in ['stages','records']});(out/'progress.json').write_text(json.dumps(dict(rows=rows,guards=guards),indent=2)+'\n')
    print(label,window,repeat,width,variant,round(x['steady_seconds'],6),x['points'],flush=True)
    return x
for window,num,den in windows:
    for repeat in range(5):
        order=widths[repeat%len(widths):]+widths[:repeat%len(widths)]
        if repeat%2:order=list(reversed(order))
        for width in order:
            if (window,width) not in blocked:call(window,num,den,width,repeat)
selection={}
for window,_,_ in windows:
    med={w:statistics.median(x['steady_seconds'] for x in rows if x['window_name']==window and x['width']==w) for w in widths if (window,w) not in blocked}
    selection[window]=min(med,key=med.get)
(out/'frozen-selection.json').write_text(json.dumps(dict(selection=selection,holdout_offset=[1,100000],selection_metric='Measured full steady seconds including audit and durable commits'),indent=2)+'\n')
for window,num,den in windows:
    left=Fraction(num,den)+Fraction(1,100000)
    for repeat in range(5):
        order=[('reference',8),('combined',selection[window])]
        if repeat%2:order.reverse()
        for variant,width in order:call(window,left.numerator,left.denominator,width,repeat,variant,'holdout')
summary={}
for window,_,_ in windows:
    group=[x for x in rows if x['window_name']==window and x['label']=='holdout']
    med={v:statistics.median(x['steady_seconds'] for x in group if x['variant']==v) for v in ['reference','combined']}
    summary[window]=dict(selected_width=selection[window],medians=med,combined_throughput_ratio=med['reference']/med['combined'],samples=group)
(out/'summary.json').write_text(json.dumps(dict(status='passed',summary=summary,training=rows,guards=guards,
    timing='Fresh preparation, independent certificates, bounded prefetch, GPU, response checks, first-chunk full GMP audit and local durable journal commits. Fixed exact-region span and commit cadence for all widths.',
    holds='Winner selected from training windows before disjoint holdout runs; 4 physical cores; no full-domain or production speedup claim.'),indent=2)+'\n')
