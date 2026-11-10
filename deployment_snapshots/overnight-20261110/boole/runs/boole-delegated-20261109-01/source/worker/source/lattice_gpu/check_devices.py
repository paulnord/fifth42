#!/usr/bin/env python3
"""Finite correctness comparisons; invoked only by the guarded validator."""
import argparse,copy,itertools,json,os,random,subprocess,time
from pathlib import Path
import model as m
ROOT=m.ROOT
def brute(bound,mode,cap):
    powers=[x**5 for x in range(bound+1)];hits=[]
    for c in range(2,bound+1):
        limit=cap if mode=='constant' else 5*c*c
        for b in range(1,c):
            for a in range(1,b+1):
                r=powers[a]+powers[b]-powers[c]
                if abs(r)<=limit:hits.append((a,b,c,r))
    return sorted(hits)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(exist_ok=False)
    started=time.monotonic();gpu_used=0.;records=[];cases=[];mask=(1<<192)-1
    def execute(name,packet,args=(),expected=0):
        nonlocal gpu_used
        t=time.monotonic();limit=min(20,120-gpu_used) if name=='cuda' else 60
        if limit<=0:raise TimeoutError('GPU subprocess wall budget exhausted')
        try:
            r=subprocess.run([str(ROOT/'bin'/name),*args],input=packet,text=True,capture_output=True,timeout=limit,env=dict(os.environ,CUDA_VISIBLE_DEVICES='0',ASAN_OPTIONS='detect_leaks=0'))
        except subprocess.TimeoutExpired:
            seconds=time.monotonic()-t
            if name=='cuda':gpu_used+=seconds
            records.append(dict(binary=name,args=list(args),exit_code=None,timed_out=True,wall_seconds=seconds,input_sha256=__import__('hashlib').sha256(packet.encode()).hexdigest()))
            raise
        seconds=time.monotonic()-t
        if name=='cuda':gpu_used+=seconds
        records.append(dict(binary=name,args=list(args),exit_code=r.returncode,wall_seconds=seconds,input_sha256=__import__('hashlib').sha256(packet.encode()).hexdigest()))
        if r.returncode!=expected:raise RuntimeError(f'{name}: exit {r.returncode}; {r.stderr}; {r.stdout[:500]}')
        return json.loads(r.stdout)
    backends=[('emulated','emulated'),('emulated-sanitized','emulated'),('cuda','gpu')]
    try:
        # Signed, zero, cross-limb and >128-bit fifth powers against Python integers.
        values=[0,1,-1,2,-2,2**32-1,2**32,2**32+1,10**8,-10**8,m.MAX_BASE,-m.MAX_BASE]
        rng=random.Random(194133);pairs=[(x,y) for x in values for y in values]+[(rng.randint(-m.MAX_BASE,m.MAX_BASE),rng.randint(-m.MAX_BASE,m.MAX_BASE)) for _ in range(128)]
        packet='ARITH_V1 '+str(len(pairs))+'\n'+'\n'.join(f'{x} {y}' for x,y in pairs)+'\n'
        def unpack(v):return sum(int(x)<<(64*i) for i,x in enumerate(v))
        for binary,backend in backends:
            result=execute(binary,packet,('--arithmetic',));assert result['backend']==backend and len(result['arithmetic'])==len(pairs)
            for (x,y),row in zip(pairs,result['arithmetic']):
                px,py=x**5,y**5
                for key,v in [('p',px),('q',py),('sum',px+py),('negative',-px-py),('square5',5*x*x)]:assert unpack(row[key])==(v&mask),(binary,x,y,key)
                assert row['lt']==(px<py) and row['eq']==(px==py)
        for bound,mode,cap in [(10,'constant',18098),(40,'constant',0),(40,'constant',42),(100,'constant',12),(100,'constant',2951),(100,'healy',42),(1000,'constant',42),(1000,'healy',42)]:
            t=time.monotonic();plan=m.make_plan(bound,mode,cap);packet=m.packet(plan);prep=time.monotonic()-t
            if bound<=100:expected=brute(bound,mode,cap)
            else:
                # These outputs were independently reproduced before this worker.
                receipt=json.loads((ROOT/'CPU_BASELINE.json').read_text());scratch=Path(receipt['scratch'])
                file='signed42-1000.json' if mode=='constant' else 'healy-1000.json'
                expected=sorted(map(tuple,json.loads((scratch/'results'/file).read_text())['hits']))
            matches=[]
            for binary,backend in backends:
                result=execute(binary,packet);process_seconds=records[-1]['wall_seconds'];t=time.monotonic();hits=m.decode(plan,result,backend);decode_seconds=time.monotonic()-t;assert hits==expected,(binary,bound,mode,cap,hits,expected)
                matches.append(dict(binary=binary,points_visited=result['points_visited'],raw_candidates=len(result['hits']),exact_patch_hits=len(hits),engine_seconds=result['engine_seconds'],kernel_seconds=result['kernel_seconds'],engine_process_seconds=process_seconds,host_verification_seconds=decode_seconds,end_to_end_seconds=prep+process_seconds+decode_seconds))
            if mode=='constant' and cap==42:
                signed=sorted({tuple(sorted((a,b,-c))) if r==42 else tuple(sorted((-a,-b,c))) for a,b,c,r in expected if abs(r)==42}|m.reference().signed_reference(min(bound,2),42))
                assert signed==sorted(m.reference().signed_reference(bound,42))
            if cap in (12,2951):assert any(r==cap for *_,r in expected)
            cases.append(dict(bound=bound,mode=mode,cap=cap,complete_positive_domain=True,patches=len(plan['tasks']),coefficient_points=plan['points'],cpu_preparation_seconds=prep,hits=expected,backends=matches))
        # Known large fixtures are selected patches, not full-shell searches.
        plan=m.make_plan(mode='healy',selected=True);packet=m.packet(plan);ref=m.reference();expected=set()
        for task in plan['tasks']:expected|=ref.patch_search(m.patch_for_task(task),lambda r,c:abs(r)<=5*c*c)
        for binary,backend in backends:assert m.decode(plan,execute(binary,packet),backend)==sorted(expected)
        for a0,b0,c0 in m.FIXTURES:assert (a0,b0,c0,a0**5+b0**5-c0**5) in expected
        # A tiny output buffer must fail the complete box, including on the GPU.
        identity='LATTICE_GPU_V1 0 18098 1\n0 1 10 10 10 10 1 0 0 0 1 0 0 0 1\n'
        for binary,backend in backends:
            boundary=execute(binary,identity)
            assert boundary['points_visited']==21**3 and boundary['counts']==[dict(id=0,expected=21**3,visited=21**3)]
            boundary_hits=sorted((h['a'],h['b'],h['c'],h['a']**5+h['b']**5-h['c']**5) for h in boundary['hits'])
            assert boundary_hits==brute(10,'constant',18098) and (9,9,10,18098) in boundary_hits
            assert execute(binary,identity,('--capacity','1'),2)['box_complete'] is False
            for bad in ['LATTICE_GPU_V1 0 42 4097\n','LATTICE_GPU_V1 0 42 1\n0 1 10 2 2 2 9223372036854775807 0 0 0 1 0 0 0 1\n']:
                assert execute(binary,bad,expected=2)['box_complete'] is False
        report=dict(status='passed',arithmetic_cases=len(pairs),full_domain_cases=cases,selected_large_fixture_patches=2,selected_large_fixtures_are_full_shell_coverage=False,gpu_subprocess_wall_seconds=gpu_used,total_wall_seconds=time.monotonic()-started,engine_calls=records,speedup_demonstrated=False)
    except BaseException as error:
        report=dict(status='failed_or_incomplete',error=f'{type(error).__name__}: {error}',gpu_subprocess_wall_seconds=gpu_used,total_wall_seconds=time.monotonic()-started,engine_calls=records,full_domain_cases=cases,speedup_demonstrated=False)
    (a.output/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('engine_calls','full_domain_cases')},indent=2))
    return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
