from pathlib import Path
import sys,types,json,hashlib,statistics,time,math,itertools,random
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent/'fifth42-coordinator-20261105';SOURCE=REPO/'lattice_prototype';sys.path[:0]=[str(ROOT.parent/'fifth42-coordinator-deps'),str(SOURCE/'compiled_experiment'),str(SOURCE)]
import benchmark_mpq
l,f=benchmark_mpq.engine('mpq')

def scale_allowed(g,targets):
    return any(t==0 for t in targets) if g==0 else any(t % (g**5) == 0 for t in targets)

source=(SOURCE/'compiled_experiment/modular_filters_snapshot.py').read_text()
source=source.replace('    integer_intervals: int = 0','    integer_intervals: int = 0\n    primitive_rejects: int = 0\n    gcd_calls: int = 0')
source=source.replace('        for n in candidates:', '        suffix_gcd = math.gcd(ns[1],ns[2]) if k == 0 else 1\n        primitive_only = filt.targets <= {-42,42}\n        for n in candidates:')
source=source.replace('            if k == 0 and not skipping:', '''            if k == 0 and suffix_gcd != 1:
                fs.gcd_calls += 1
                g = math.gcd(n,suffix_gcd)
                if (g != 1 if primitive_only else not scale_allowed(g,filt.targets)):
                    fs.primitive_rejects += 1
                    continue
            if k == 0 and not skipping:''')
p=types.ModuleType('_private_primitive_sphere');sys.modules[p.__name__]=p
exec(compile(source,str(ROOT/'private_primitive_sphere.py'),'exec'),p.__dict__);p.l=l;p.Q=l.Q;p.math=math;p.scale_allowed=scale_allowed
(ROOT/'private_primitive_sphere.py').write_text('# Derived isolated test only. Requires injected l, Q, math, scale_allowed.\n'+source)

def oracle(bound,targets):
    powers=[a**5 for a in range(bound+1)]; roots={value:a for a,value in enumerate(powers)}
    hits=set()
    for c in range(1,bound+1):
        for b in range(1,c):
            for target in targets:
                a=roots.get(target+powers[c]-powers[b])
                if a is not None and 1<=a<=b: hits.add((a,b,c,target))
    return hits

rows=[]
for bound,targets in [(100,[-42,42]),(100,[12,384,2951,-960]),(100,[0]),(1000,[-42,42])]:
    expected=oracle(bound,targets)
    for mode in ('prune','interval'):
        vals={};results={}
        for repeat in range(5):
            for name,module in ([('baseline',f),('suffix_gcd',p)] if repeat%2 else [('suffix_gcd',p),('baseline',f)]):
                st=time.perf_counter();result=module.search_targets_positive(bound,targets,mode=mode,backend='fpylll',width=2,max_seconds=60,max_nodes=10_000_000)
                vals.setdefault(name,[]).append(time.perf_counter()-st);results[name]=result
                assert set(map(tuple,result['hits']))==expected,(bound,targets,mode,name,result['hits'],expected)
        row=dict(bound=bound,targets=targets,mode=mode,hits=sorted(expected),all_hit_sets_equal=True,baseline_stats=results['baseline']['stats'],baseline_filter_stats=results['baseline']['filter_stats'],candidate_stats=results['suffix_gcd']['stats'],candidate_filter_stats=results['suffix_gcd']['filter_stats'],timings={k:dict(samples=v,median=statistics.median(v)) for k,v in vals.items()})
        rows.append(row);print(json.dumps(dict(bound=bound,targets=targets,mode=mode,hit_count=len(expected),times={k:round(v['median'],4) for k,v in row['timings'].items()},rejects=row['candidate_filter_stats']['primitive_rejects'],gcd_calls=row['candidate_filter_stats']['gcd_calls'])),flush=True)
# Direct transformation invariance checks, negative/zero coefficients, both determinant signs.
rng=random.Random(4242);mapping=0
for sign in (-1,1):
 for trial in range(20):
  u=[[1,0,0],[0,1,0],[0,0,sign]]
  for k in range(10):
   i,j=rng.sample(range(3),2);v=rng.randint(-7,7);u[i]=[a+v*b for a,b in zip(u[i],u[j])]
  assert abs(l.det3(u))==1
  for n in itertools.product(range(-3,4),repeat=3):
   v=[sum(n[k]*u[k][j] for k in range(3)) for j in range(3)]
   assert math.gcd(*n)==math.gcd(*v);mapping+=1
assert scale_allowed(2,[384]) and not scale_allowed(2,[-42,42]) and scale_allowed(0,[0]) and not scale_allowed(0,[42])
# Known nonprimitive exact control must survive its target-aware filter.
assert 26**5+32**5-34**5==384 and math.gcd(26,32,34)==2
out=dict(status='passed',scope='Bounded exact positive-domain controls, including independent pair-power hash oracle through B1000',unimodular_mapping_cases=mapping,control_nonprimitive=[26,32,34,384],rows=rows)
(ROOT/'sphere-results.json').write_text(json.dumps(out,indent=2,default=int)+'\n')
