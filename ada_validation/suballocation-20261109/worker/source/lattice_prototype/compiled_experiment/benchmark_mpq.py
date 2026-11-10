"""Opt-in isolated GMP experiment. Never mutates production module globals.

Frozen source snapshots are loaded under private names. Only those private
module instances receive the exact mpq constructor. No floating point is used
for geometry, enumeration, exclusion, or residual tests.
"""
import cProfile
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT.parent/'fifth_lattice_compiled_deps'), str(ROOT.parent/'fifth_lattice_deps'), str(ROOT)]
from fractions import Fraction
import gmpy2
if gmpy2.version() != '2.2.2':
    raise RuntimeError('validated compiled experiment requires gmpy2 2.2.2')


def private_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE/filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # required by dataclass introspection, private name only
    spec.loader.exec_module(mod)
    return mod


def engine(kind):
    l = private_module('_experiment_lattice_'+kind, 'lattice5_snapshot.py')
    f = private_module('_experiment_filter_'+kind, 'modular_filters_snapshot.py')
    f.l = l
    if kind == 'mpq':
        l.Q = f.Q = gmpy2.mpq
    return l, f


def geometry(l, f, bound, targets):
    """Exact normalized transcript of every planned patch and reduced geometry."""
    records = []
    cap = max(map(abs, targets))
    cmin = 1
    while cmin <= bound:
        cmax = min(2*cmin-1, bound)
        if l.Q(cap, cmin**5) <= l.Q(9049,50000):
            count = max(1,l.ceil(l.Q(9*cmin,20)))
            for i in range(count):
                p = l.make_patch(cmin,cmax,l.Q(9*i,10*count),l.Q(9*(i+1),10*count),cap)
                basis = p.basis()
                reduced,u = l.reduce_basis(basis,'fpylll')
                mu,norms = l.gram_schmidt(reduced)
                records.append(normalize([vars(p),basis,reduced,u,mu,norms]))
        cmin *= 2
    return records


def normalize(x):
    if isinstance(x, (Fraction, gmpy2.mpq)):
        return [int(x.numerator),int(x.denominator)]
    if isinstance(x, gmpy2.mpz):
        return int(x)
    if isinstance(x, dict):
        return {k:normalize(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)):
        return [normalize(v) for v in x]
    return x


def comparable(result):
    result = normalize(result)
    result['stats'].pop('seconds')
    return result


def main():
    engines = {kind:engine(kind) for kind in ('fraction','mpq')}
    # Warm the published LLL backend before timings.
    import fpylll
    rows = []
    for bound,targets,signed in [(100,[-42,42],True),(1000,[-42,42],True),(34,[12,384],False),(100,[2951],False)]:
        l0,f0 = engines['fraction']
        oracle = (l0.signed_reference(bound,42) if signed else l0.direct_positive(1,bound,lambda c:max(map(abs,targets)),lambda r,c:r in targets))
        geometries = [geometry(l,f,bound,targets) for l,f in engines.values()]
        assert geometries[0] == geometries[1]
        geometry_hash = hashlib.sha256(json.dumps(geometries[0],sort_keys=True).encode()).hexdigest()
        for mode in ('prune','interval'):
            results,times = {},{k:[] for k in engines}
            # Alternate paired order to reduce drift.
            for repeat in range(5):
                for kind in (('fraction','mpq') if repeat%2 == 0 else ('mpq','fraction')):
                    l,f = engines[kind]
                    result = (f.signed42_filtered(bound,mode=mode,backend='fpylll') if signed else f.search_targets_positive(bound,targets,mode=mode,backend='fpylll'))
                    assert result['complete']
                    assert set(map(tuple,result['signed_hits'] if signed else result['hits'])) == oracle
                    if not signed:
                        assert oracle
                    times[kind].append(result['stats']['seconds'])
                    results[kind] = comparable(result)
            assert results['fraction'] == results['mpq']
            row = dict(bound=bound,targets=targets,signed=signed,mode=mode,times=times,medians={k:statistics.median(v) for k,v in times.items()},exact_geometry_equal=True,geometry_sha256=geometry_hash,geometry_patches=len(geometries[0]),all_results_and_counters_equal=True,oracle_equal=True,result=results['mpq'])
            row['speedup']=row['medians']['fraction']/row['medians']['mpq']
            rows.append(row)
            (ROOT/'results/compiled-mpq-benchmark.json').write_text(json.dumps(rows,indent=2))
            print(bound,targets,mode,row['medians'],'speedup',row['speedup'],flush=True)
    for kind,(l,f) in engines.items():
        profiler=cProfile.Profile()
        profiler.runcall(f.signed42_filtered,1000,mode='interval',backend='fpylll')
        profiler.dump_stats(str(ROOT/f'results/profile-{kind}-interval-1000.prof'))
        import pstats
        with (ROOT/f'results/profile-{kind}-interval-1000.txt').open('w') as out:
            pstats.Stats(profiler,stream=out).sort_stats('cumulative').print_stats(35)
    print('All geometry, counter, oracle, and nonempty-control checks passed.',flush=True)

if __name__ == '__main__':
    main()
