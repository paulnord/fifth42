import argparse,bisect,hashlib,json,random,subprocess,sys,time
from pathlib import Path
from dataclasses import replace
import host_probe as h
ROOT=h.ROOT;core=h.core;pipeline=h.pipeline
def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def oracle(bound,cap):
    powers=[i**5 for i in range(bound+1)];out=set()
    for c in range(1,bound+1):
        for b in range(1,c):
            target=powers[c]-powers[b]
            for a in range(bisect.bisect_left(powers,target-cap,1,b+1),bisect.bisect_right(powers,target+cap,1,b+1)):
                out.add((a,b,c,powers[a]+powers[b]-powers[c]))
    return out
def full_plan(bound,cap):
    specs,direct=core.specs(bound,cap,8);rows=[pipeline.prepare_certified(s) for s in specs]
    return h.packing_opt.assemble(bound,cap,specs,direct,[r[0] for r in rows],[r[1] for r in rows])
def response(session,packet):
    r,_=session.run(packet,timeout=30);pipeline.validate_response_types(r)
    if r.get('box_complete') is not True:raise ValueError(r)
    return r
def norm(r):return dict(counts=[dict(id=x['id'],expected=x['expected'],visited=x.get('accounted',x['visited'])) for x in r['counts']],hits=sorted(r['hits'],key=lambda x:(x['task'],x['linear'])))
def reference(packet):
    p=subprocess.run([str(ROOT/'bin/gmp_reference')],input=packet,text=True,capture_output=True,check=True,timeout=60)
    return json.loads(p.stdout)
def packet(j,u,cmin,cmax,cap=42,mode=0):
    return f'LATTICE_GPU_V1 {mode} {cap} 1\n0 {cmin} {cmax} '+ ' '.join(map(str,j))+'\n'+' '.join(str(x) for row in u for x in row)+'\n'
def run(variant):
    h.initialize(h.SOURCE,(),variant);packets=[];cases=[]
    with h.open_session(ROOT/'bin/scaling_gpu','gpu',time.monotonic()+240) as baseline:
        for bound,cap in [(34,384),(100,2951),(1000,42)]:
            plan=full_plan(bound,cap);hits=set(plan.direct_hits);expected=oracle(bound,cap)
            for batch in plan.batches:
                r=response(baseline,batch.packet);g=reference(batch.packet)
                assert norm(r)==norm(g),'Independent GMP small-domain records'
                hits|=core.decode_batch(batch,r,'gpu');packets.append(dict(label=f'full-{bound}-{cap}',packet=batch.packet,expected=norm(g)))
            assert hits==expected and hits,'Independent nonempty full-domain oracle'
            cases.append(dict(bound=bound,cap=cap,hits=sorted(hits),points=plan.points,certificate=plan.certificate_sha256))
        class Serial:
            def map(self,f,items,chunksize):return list(map(f,items))
        for first in [3000000000,3917103232,6250000000,10625000000,11249999996]:
            chunk=pipeline.prepare_chunk(Serial(),pipeline.Window(100000000001,200000000000,first,first+4,8,222,42,'adaptive'),'packed')
            for batch in chunk.plan.batches:
                r=response(baseline,batch.packet);g=reference(batch.packet);assert norm(r)==norm(g),'High-shell GMP'
                core.decode_batch(batch,r,'gpu');packets.append(dict(label=f'high-{first}',packet=batch.packet,expected=norm(g)))
            cases.append(dict(first=first,points=chunk.plan.points,geometry=chunk.geometry_sha256))
        # Certification must still reject altered points, transform and bounds.
        task=core.prepare_task(chunk.window.specifications()[0])
        for bad in [replace(task,points=task.points+1),replace(task,J=(task.J[0]+1,*task.J[1:])),replace(task,U=((0,0,0),*task.U[1:]))]:
            try:core.certify_task(bad)
            except ValueError:pass
            else:raise AssertionError('Tampered certificate accepted')
    if variant=='reference':
        identity=[[1,0,0],[0,1,0],[0,0,1]]
        synthetic=[]
        for cap in [0,1,42,125,384,2**63-1]:synthetic.append((f'cap-{cap}',packet([10,10,10],identity,1,10,cap)))
        synthetic.append(('variable-cap',packet([20,20,20],identity,1,20,0,1)))
        for axis in range(3):
            u=[[0,0,0] for _ in range(3)];u[axis][0]=1;u[(axis+1)%3][1]=1;u[(axis+2)%3][2]=1
            j=[7,7,7];j[axis]=10000
            synthetic.append((f'long-row-axis-{axis}',packet(j,u,1,10000)))
        synthetic.append(('signed-extreme',packet([1,0,0],[[2**63-2,0,0],[0,1,0],[0,0,1]],1,200000000000)))
        rng=random.Random(20261109)
        for i in range(32):
            u=[row[:] for row in identity]
            for _ in range(4):
                a,b=rng.sample(range(3),2);q=rng.choice([-2,-1,1,2]);u[a]=[x+q*y for x,y in zip(u[a],u[b])]
            synthetic.append((f'signed-unimodular-{i}',packet([rng.randrange(1,8) for _ in range(3)],u,1,200,rng.choice([0,12,42,384]))))
        for label,p in synthetic:packets.append(dict(label=label,packet=p,expected=norm(reference(p))))
        (ROOT/'validation-packets.json').write_text(json.dumps(packets,indent=2)+'\n')
    result=dict(status='passed',variant=variant,cases=cases,packets=len(packets),independent_gmp=True,tamper_rejections=3)
    (ROOT/'results'/f'host-validation-{variant}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(variant,'host validation passed',len(cases),flush=True)
def native():
    packets=json.loads((ROOT/'validation-packets.json').read_text());results=[]
    for binary in ['baseline','low64','rows','wheel','differences','wheel_differences']:
        with h.open_session(ROOT/'bin'/binary,'gpu',time.monotonic()+240) as session:
            counts=[]
            for item in packets:
                r=response(session,item['packet']);assert norm(r)==item['expected'],(binary,item['label'],'exact GMP record mismatch')
                assert r['points_explicitly_evaluated']+r['points_exactly_excluded']==r['points_accounted']
                assert sum(x['visited'] for x in r['counts'])==r['points_visited']==r['points_explicitly_evaluated']
                assert all(x['visited']+x['exactly_excluded']==x['accounted']==x['expected'] for x in r['counts'])
                counts.append(dict(label=item['label'],points=r['points_accounted'],evaluated=r['points_explicitly_evaluated'],excluded=r['points_exactly_excluded'],hits=len(r['hits'])))
            for p in ['LATTICE_GPU_V1 0 42 1\n0 1 200000000001 1 1 1\n1 0 0 0 1 0 0 0 1\n',
                      'LATTICE_GPU_V1 0 42 1\n0 1 10 10000000 10000000 10000000\n1 0 0 0 1 0 0 0 1\n',
                      'LATTICE_GPU_V1 0 42 1\n0 1 10 2 1 1\n9223372036854775807 0 0 0 1 0 0 0 1\n']:
                r,_=session.run(p,timeout=10);assert r.get('box_complete') is False,'Invalid packet accepted'
            response(session,packets[0]['packet']) # Framed error recovery.
        results.append(dict(binary=binary,status='passed',cases=counts,invalid_packets_rejected=3,error_recovery=True))
        (ROOT/'results/native-validation.json').write_text(json.dumps(results,indent=2)+'\n')
        print(binary,'GPU validation passed',len(counts),'packets',flush=True)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('variant');args=a.parse_args()
    native() if args.variant=='native' else run(args.variant)
