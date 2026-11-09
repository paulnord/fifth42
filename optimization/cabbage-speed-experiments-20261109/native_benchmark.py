import json,os,random,statistics,sys,time
from fractions import Fraction
from pathlib import Path
from validate import packet,norm,response
import host_probe as h
r=h.ROOT;core=h.core;out=r/'results/native-benchmark';out.mkdir(exist_ok=True)
h.initialize(h.SOURCE,(),'reference');cases=[];guards=[]
for name,num,den in [('low',6,25),('middle',7,20),('high',17,20)]:
    left=Fraction(num,den);lo=100000000001;hi=200000000000;span=Fraction(2048,lo)
    for width in [8,32,64,128]:
        specs=[];tasks=[];tokens=[];count=2048//width
        try:
            for i in range(count):
                a,b=left+span*Fraction(i,count),left+span*Fraction(i+1,count)
                bits=h.precision_policy.geometry_bits(core.lattice(),lo,hi,core.lattice().Q(*a.as_integer_ratio()),core.lattice().Q(*b.as_integer_ratio()),42)
                s=(i,lo,hi,a.as_integer_ratio(),b.as_integer_ratio(),42,bits);t=core.prepare_task(s);token=core.certify_task(t)
                specs.append(s);tasks.append(t);tokens.append(token)
            plan=h.packing_opt.assemble(hi,42,specs,(),tasks,tokens)
            cases.append(dict(name=f'{name}-w{width}',packets=[b.packet for b in plan.batches],points=plan.points,width=width,ratio=[num,den]))
        except ValueError as e:guards.append(dict(name=f'{name}-w{width}',error=str(e),completed=False))
for axis in range(3):
    u=[[0,0,0] for _ in range(3)];u[axis][0]=1;u[(axis+1)%3][1]=1;u[(axis+2)%3][2]=1;j=[7,7,7];j[axis]=10000
    cases.append(dict(name=f'long-row-axis-{axis}',packets=[packet(j,u,1,10000)],points=(20001*15*15),synthetic=True))
(out/'cases.json').write_text(json.dumps(dict(cases=cases,guards=guards),indent=2)+'\n')
bins=['scaling_gpu','baseline','low64','rows','wheel','differences','wheel_differences'];rows=[];expected={}
for case in cases:
    with h.open_session(r/'bin/scaling_gpu','gpu',time.monotonic()+180) as engine:
        expected[case['name']]=[norm(response(engine,p)) for p in case['packets']]
    for repeat in range(5):
        order=bins[repeat%len(bins):]+bins[:repeat%len(bins)]
        if repeat%2:order=list(reversed(order))
        for binary in order:
            saved=out/f"{case['name']}-{repeat}-{binary}.json"
            if saved.exists():rows.append(json.loads(saved.read_text()));continue
            with h.open_session(r/'bin'/binary,'gpu',time.monotonic()+120) as engine:
                for p in case['packets']:response(engine,p) # Untimed warmup.
                kernel=rpc=seconds=0.;evaluated=excluded=0;began=time.perf_counter()
                for inner in range(10):
                    for i,p in enumerate(case['packets']):
                        x,wall=engine.run(p,timeout=30);assert norm(x)==expected[case['name']][i],(case['name'],binary,'record mismatch')
                        kernel+=x['kernel_seconds'];rpc+=wall;seconds+=x['engine_seconds']
                        evaluated+=x.get('points_explicitly_evaluated',x['points_visited']);excluded+=x.get('points_exactly_excluded',0)
                elapsed=time.perf_counter()-began
            row=dict(case=case['name'],binary=binary,repeat=repeat,requests=10*len(case['packets']),kernel_seconds=kernel/10,
                     rpc_seconds=rpc/10,engine_seconds=seconds/10,wall_seconds=elapsed/10,points=case['points'],
                     explicitly_evaluated=evaluated//10,exactly_excluded=excluded//10,full_records_match=True)
            saved.write_text(json.dumps(row,indent=2)+'\n')
            rows.append(row);(out/'progress.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(case['name'],repeat,'complete',flush=True)
summary={}
for case in cases:
    group={b:[x for x in rows if x['case']==case['name'] and x['binary']==b] for b in bins}
    med={b:statistics.median(x['kernel_seconds'] for x in group[b]) for b in bins}
    summary[case['name']]={b:dict(kernel_median_seconds=med[b],kernel_speedup_vs_original=med['scaling_gpu']/med[b],
        rpc_median_seconds=statistics.median(x['rpc_seconds'] for x in group[b]),
        samples=group[b]) for b in bins}
(out/'summary.json').write_text(json.dumps(dict(status='passed',summary=summary,guards=guards,rows=rows,
    timing='Prepared packets only; kernel CUDA events and native RPC separately. Not full-pipeline speedups.',
    accounting='Box coverage = explicitly evaluated + exactly excluded; no skipped point is labelled explicitly visited.'),indent=2)+'\n')
