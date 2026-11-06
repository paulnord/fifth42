#!/usr/bin/env python3
"""Bounded persistent-engine parity controls. No search or coverage publication."""
import argparse, hashlib, itertools, json, math, os, statistics, sys, time
from pathlib import Path

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def parse_packet(text):
    lines=text.splitlines(); magic,mode,cap,n=lines[0].split()
    assert magic=='LATTICE_GPU_V1' and len(lines)==int(n)+1
    tasks=[]
    for i,line in enumerate(lines[1:]):
        row=list(map(int,line.split()));assert len(row)==15 and row[0]==i
        _,lo,hi,*tail=row; j=tail[:3];u=tail[3:]
        tasks.append(dict(lo=lo,hi=hi,j=j,u=u,points=math.prod(2*x+1 for x in j)))
    return int(mode),int(cap),tasks

def validate(packet,response,backend):
    mode,cap,tasks=parse_packet(packet)
    assert response.get('backend')==backend and response.get('box_complete') is True
    assert type(response['points_visited']) is int
    assert response['points_visited']==sum(t['points'] for t in tasks)
    expected=[dict(id=i,expected=t['points'],visited=t['points']) for i,t in enumerate(tasks)]
    assert response['counts']==expected
    for c in response['counts']:
        assert all(type(v) is int for v in c.values())
    records=[]
    for h in response['hits']:
        assert set(h)=={'task','linear','a','b','c'} and all(type(v) is int for v in h.values())
        t=tasks[h['task']];idx=h['linear'];assert 0<=h['task']<len(tasks) and 0<=idx<t['points']
        ns=[]
        for j in t['j']:ns.append(idx%(2*j+1)-j);idx//=2*j+1
        c,a,b=(sum(ns[i]*t['u'][3*i+k] for i in range(3)) for k in range(3))
        assert (a,b,c)==(h['a'],h['b'],h['c']) and t['lo']<=c<=t['hi'] and 1<=a<=b<c
        r=a**5+b**5-c**5;assert abs(r)<=(5*c*c if mode else cap)
        records.append((h['task'],h['linear'],a,b,c))
    assert len(records)==len(set(records))
    for key in ['engine_seconds','kernel_seconds']:
        assert type(response[key]) in (int,float) and math.isfinite(response[key]) and response[key]>=0
    return sorted(records)

def oracle(packet):
    mode,cap,tasks=parse_packet(packet);result=[]
    for tid,t in enumerate(tasks):
        assert t['points']<=100000
        for n2,n1,n0 in itertools.product(*(range(-j,j+1) for j in reversed(t['j']))):
            ns=(n0,n1,n2);c,a,b=(sum(ns[i]*t['u'][3*i+k] for i in range(3)) for k in range(3))
            if t['lo']<=c<=t['hi'] and 1<=a<=b<c and abs(a**5+b**5-c**5)<=(5*c*c if mode else cap):
                linear=(n0+t['j'][0])+(2*t['j'][0]+1)*((n1+t['j'][1])+(2*t['j'][1]+1)*(n2+t['j'][2]))
                result.append((tid,linear,a,b,c))
    return sorted(result)

def main():
    if sys.flags.optimize:raise SystemExit('Do not use Python -O; exact checks must stay enabled')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--backend',choices=['emulated','gpu'],required=True)
    p.add_argument('--ubsan',action='store_true')
    p.add_argument('--repeats',type=int,default=2)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if not 1<=a.repeats<=6 or (a.ubsan and a.backend!='emulated'):p.error('Unsupported finite probe options')
    work=a.work.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((work/'source-manifest.json').read_text())
    for name,sha in manifest['files'].items():
        if digest(work/name)!=sha:raise RuntimeError('Frozen source changed: '+name)
    sys.path.insert(0,str(work));from engine_session import EngineSession
    suffix='scaling_gpu' if a.backend=='gpu' else ('scaling_cpu_ubsan' if a.ubsan else 'scaling_cpu')
    binaries={v:work/v/'bin'/suffix for v in ['baseline','low64']}
    report=dict(status='running',backend=a.backend,ubsan=a.ubsan,repeats=a.repeats,
        cuda_executed=False,no_new_coverage_claim=True,raw_timings=[],checks=[],
        binary_sha256={v:digest(path) for v,path in binaries.items()},source_manifest_sha256=digest(work/'source-manifest.json'))
    began=time.monotonic();deadline=began+120;sessions={}
    def session(binary,capacity=65536):
        return EngineSession([str(binary),'--capacity',str(capacity)],a.backend,deadline,
            environment=dict(os.environ,CUDA_VISIBLE_DEVICES='0'))
    def run(s,packet):
        result,wall=s.run(packet,timeout=min(10,max(.001,deadline-time.monotonic())))
        if a.backend=='gpu':report['cuda_executed']=True
        return result,wall
    try:
        evidence=work/'packet-evidence';certificates=json.loads((evidence/'manifest.json').read_text());cases=[]
        for name in ['small1000','controls100','high8','high32']:
            path=evidence/(name+'.packet');assert digest(path)==certificates[name]['sha256']
            packet=path.read_text();expected=json.loads((evidence/(name+'.interval.json')).read_text())
            assert expected['equal_hit_sets'] is True
            cases.append((name,packet,sorted(map(tuple,expected['hits']))))
        # Synthetic controls are point tests, not certified region coverage.
        triples=[(1,1,2),(13,16,17),(2,2,4),(8192,8192,16384),
                 (1,1,200000000000),(199999999998,199999999999,200000000000)]
        caps=[0,1,12,42,960,2951,(1<<63)-1]
        for mode,cap in [(0,c) for c in caps]+[(1,0)]:
            rows=['LATTICE_GPU_V1 %d %d %d'%(mode,cap,len(triples))]
            rows += [f'{i} {c} {c} 1 0 0 {c} {x} {y} 0 0 0 0 0 0' for i,(x,y,c) in enumerate(triples)]
            packet='\n'.join(rows)+'\n';cases.append((f'triple-mode{mode}-cap{cap}',packet,oracle(packet)))
        identity='LATTICE_GPU_V1 0 18098 1\n0 1 10 10 10 10 1 0 0 0 1 0 0 0 1\n'
        cases.append(('nonempty-identity',identity,oracle(identity)))
        assert any(row[2:]==(1,1,2) for name,_,hits in cases if name=='triple-mode0-cap42' for row in hits)
        assert all(row[2:]!=(8192,8192,16384) for _,_,hits in cases for row in hits)
        for v,binary in binaries.items():
            sessions[v]=session(binary)
            for name,packet,expected in cases:
                response,wall=run(sessions[v],packet)
                assert validate(packet,response,a.backend)==expected,(v,name)
                report['checks'].append(dict(variant=v,case=name,points=response['points_visited'],hit_records=len(expected),passed=True))
            # Failed request must not poison the next complete request.
            with session(binary,1) as limited:
                bad,_=run(limited,identity);assert bad.get('box_complete') is False
                empty='LATTICE_GPU_V1 0 42 0\n';ok,_=run(limited,empty);assert validate(empty,ok,a.backend)==[]
                one='LATTICE_GPU_V1 0 42 1\n0 2 2 1 0 0 2 1 1 0 0 0 0 0 0\n'
                ok,_=run(limited,one);assert validate(one,ok,a.backend)==[(0,2,1,1,2)]
                for invalid in ['LATTICE_GPU_V1 0 42 4097\n','LATTICE_GPU_V1 0 9223372036854775808 0\n']:
                    bad,_=run(limited,invalid);assert bad.get('box_complete') is False
                ok,_=run(limited,one);assert validate(one,ok,a.backend)==[(0,2,1,1,2)]
            report['checks'].append(dict(variant=v,case='capacity-and-invalid-request-recovery',passed=True))
        # Alternating AB/BA repetitions, warmed sessions; raw values retained.
        for repeat in range(a.repeats):
            for v in (['baseline','low64'] if repeat%2==0 else ['low64','baseline']):
                for name,packet,expected in cases[:4]:
                    response,wall=run(sessions[v],packet)
                    checked=time.perf_counter();assert validate(packet,response,a.backend)==expected
                    report['raw_timings'].append(dict(repeat=repeat,variant=v,packet=name,
                        request_wall_seconds=wall,engine_seconds=response['engine_seconds'],
                        kernel_seconds=response['kernel_seconds'],decode_seconds=time.perf_counter()-checked,
                        packet_sha256=hashlib.sha256(packet.encode()).hexdigest()))
        report['status']='passed'
    except BaseException as error:
        report['status']='failed_or_incomplete';report['error']=f'{type(error).__name__}: {error}';raise
    finally:
        for s in sessions.values():s.close()
        report['wall_seconds']=time.monotonic()-began
        report['timing_scope']='Warmed fixed-packet calibration only; excludes preparation, certification and durable commits. No full end-to-end speedup.'
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','backend','cuda_executed','wall_seconds']}))

if __name__=='__main__':main()
