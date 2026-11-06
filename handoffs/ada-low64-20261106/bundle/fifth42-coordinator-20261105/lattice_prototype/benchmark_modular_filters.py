"""Small reproducible patch comparison, not a production/global search."""
import argparse
import json
import statistics
from fractions import Fraction as Q
from itertools import product
import lattice5 as l
import modular_filters as f


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("reference","sympy","fpylll"), default="reference")
    backend = parser.parse_args().backend
    cases = [
        ('nonempty_boundary', l.make_patch(17,34,Q(13,17),Q(4,5),384),[12,384]),
        ('target42_medium_patch', l.make_patch(64,127,Q(7,10),Q(4,5),42),[-42,42]),
        ('target42_narrow_patch', l.make_patch(64,127,Q(3,4),Q(31,40),42),[-42,42]),
    ]
    rows = []
    for name,p,targets in cases:
        oracle = l.patch_search(p,lambda r,c:r in targets)
        for mode,mods in [('none',()),('post',(25,)),('post',(31,)),('post',(61,)),
                          ('post',(25,31,61)),('prune',(25,)),('prune',(31,)),
                          ('prune',(61,)),('prune',(25,31,61))]:
            samples = [f.search_patch(p,targets,mode,mods,backend=backend) for _ in range(5)]
            assert all(set(map(tuple,s['hits']))==oracle for s in samples)
            row = samples[-1]
            row.update(case=name,repetitions=5,median_seconds=statistics.median(s['stats']['seconds'] for s in samples))
            rows.append(row)
    density=[]
    for targets in ([42],[-42,42],[12,384]):
        for m in (25,31,61):
            powers=[pow(i,5,m) for i in range(m)]
            want={t%m for t in targets}
            count=sum((powers[a]+powers[b]-powers[c])%m in want for c,a,b in product(range(m),repeat=3))
            density.append(dict(targets=targets,modulus=m,allowed_classes=count,total_classes=m**3,density=count/m**3))
    print(json.dumps(dict(scope='Three bounded positive-domain patches; no global exclusion or asymptotic claim',rows=rows,residue_densities=density),indent=2))

if __name__=='__main__':
    main()
