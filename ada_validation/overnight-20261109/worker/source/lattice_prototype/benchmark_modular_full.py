"""Bounded full-domain signed42 comparisons, including independent signed oracle."""
import json
import statistics
import argparse
import lattice5 as l
import modular_filters as f

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backend',default='fpylll',choices=['reference','sympy','fpylll'])
    args=parser.parse_args()
    rows=[]
    for bound,repeats in ((100,3),(1000,1)):
        oracle=l.signed_reference(bound,42)
        for mode in ('none','post','prune'):
            samples=[f.signed42_filtered(bound,mode=mode,backend=args.backend,max_seconds=180) for _ in range(repeats)]
            assert all(set(map(tuple,s['signed_hits']))==oracle for s in samples)
            r=samples[-1]
            r.update(repetitions=repeats,median_seconds=statistics.median(s['stats']['seconds'] for s in samples),signed_dictionary_oracle_equal=True)
            rows.append(r)
            print(json.dumps(dict(bound=bound,mode=mode,seconds=r['median_seconds'])),file=__import__('sys').stderr,flush=True)
    print(json.dumps(dict(scope='Full signed boxes only through recorded bounds; target42 only',rows=rows),indent=2))
if __name__=='__main__':
    main()
