"""Bounded paired end-to-end and reduction-only benchmarks; never a production run."""
import argparse, json, platform, statistics, time
from pathlib import Path
from fractions import Fraction as Q
import lattice5 as l
from reproduce import PUBLISHED
OUT=Path(__file__).parent/'results'
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume',action='store_true',help='reuse completed paired rows after an interrupted run')
    args=parser.parse_args()
    report={'platform':platform.platform(),'python':platform.python_version(),'timing_note':'Three warm end-to-end trials; setup/import excluded. Reduction microbenchmark includes denominator clearing and exact transform validation. Exact enumeration remains unchanged.','runs':[],'large_controls':[],'reduction':[]}
    if args.resume and (OUT/'backend-benchmark.json').exists():
        report=json.loads((OUT/'backend-benchmark.json').read_text())
    backends=['reference','sympy','fpylll']
    for backend in backends:
        l.reduce_basis([[1,0,0],[0,1,0],[0,0,1]],backend)
    for bound in [100,1000]:
        for mode in ['healy','signed42']:
            expected=(l.direct_positive(1,bound,lambda c:5*c*c,lambda r,c:abs(r)<=5*c*c) if mode=='healy' else l.signed_reference(bound,42))
            for backend in backends:
                if any(r['bound']==bound and r['mode']==mode and r['backend']==backend for r in report['runs']):
                    continue
                times=[]
                for trial in range(3):
                    result=l.search_positive(bound,mode='healy',backend=backend) if mode=='healy' else l.signed42(bound,backend=backend)
                    hits=set(map(tuple,result['hits' if mode=='healy' else 'signed_hits']))
                    assert hits==expected
                    times.append(result['stats']['seconds'])
                row={'bound':bound,'mode':mode,'backend':backend,'seconds':times,'median_seconds':statistics.median(times),'exact_oracle_match':True,'hits':sorted(expected),'stats_last':result['stats']}
                report['runs'].append(row);print(json.dumps(row),flush=True)
                (OUT/'backend-benchmark.json').write_text(json.dumps(report,indent=2))
    report["large_controls"]=[]
    report["reduction"]=[]
    patches=[]
    for a,b,c in [(13852184,27401825,27580409),(21137517920,21483066250,24482314857)]:
        C=1<<(c.bit_length()-1);D=2*C-1;count=l.ceil(Q(9*C,20));i=l.floor(Q(a,c)*10*count/9)
        patch=l.make_patch(C,D,Q(9*i,10*count),Q(9*(i+1),10*count),5*D*D,bits=160)
        patches.append(patch)
        for backend in backends:
            stats=l.Stats();t=time.perf_counter();hits=l.patch_search(patch,lambda r,c:abs(r)<=5*c*c,stats,backend=backend)
            assert (a,b,c,a**5+b**5-c**5) in hits
            report['large_controls'].append({'triple':[a,b,c],'backend':backend,'seconds':time.perf_counter()-t,'hit_found':True,'coverage':'one fixture-selected patch only, NOT complete shell'})
    patches += [l.make_patch(512,1000,Q(i,10),Q(i+1,10),42) for i in range(9)]
    for backend in backends:
        times=[]
        for repeat in range(3):
            t=time.perf_counter()
            for p in patches:l.reduce_basis(p.basis(),backend)
            times.append(time.perf_counter()-t)
        report['reduction'].append({'backend':backend,'patches':len(patches),'seconds':times,'median_seconds':statistics.median(times)})
    (OUT/'backend-benchmark.json').write_text(json.dumps(report,indent=2))
    print('PASS: exact bounded controls and selected large patches',flush=True)
if __name__=='__main__':main()
