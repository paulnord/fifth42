"""Paired exact enumeration optimizations; bounded nonempty and signed controls."""
import json,time,statistics
from pathlib import Path
import lattice5 as l
import modular_filters as f

def main():
 rows=[]
 for bound,repeats in [(100,3),(1000,3)]:
  expected=l.signed_reference(bound,42)
  for mode,mods in [('prune',(25,31,61)),('progression',(25,31,61)),('interval',(25,31,61)),('interval',())]:
   times=[]
   for _ in range(repeats):
    r=f.signed42_filtered(bound,mode=mode,moduli=mods,backend='fpylll')
    assert set(map(tuple,r['signed_hits']))==expected
    times.append(r['stats']['seconds'])
   r.update(times=times,median_seconds=statistics.median(times),oracle_equal=True)
   rows.append(r);Path('results/enumeration-benchmark.json').write_text(json.dumps(rows,indent=2))
   print(bound,mode,mods,r['median_seconds'],flush=True)
 for mode in ['prune','progression','interval']:
  for targets,bound in [([12,384],34),([2951],100)]:
   r=f.search_targets_positive(bound,targets,mode=mode,backend='fpylll')
   expected=l.direct_positive(1,bound,lambda c:max(map(abs,targets)),lambda r,c:r in targets)
   assert set(map(tuple,r['hits']))==expected and expected
   rows.append(dict(nonempty_control=True,mode=mode,targets=targets,bound=bound,hits=r['hits'],oracle_equal=True))
 Path('results/enumeration-benchmark.json').write_text(json.dumps(rows,indent=2))
def large_controls():
 from fractions import Fraction as Q
 out=[]
 for a,b,c in [(13852184,27401825,27580409),(21137517920,21483066250,24482314857)]:
  C=1<<(c.bit_length()-1);D=2*C-1;count=l.ceil(Q(9*C,20));i=l.floor(Q(a,c)*10*count/9)
  p=l.make_patch(C,D,Q(9*i,10*count),Q(9*(i+1),10*count),5*D*D,bits=160);r=a**5+b**5-c**5
  for mode in ['prune','progression','interval']:
   v=f.search_patch(p,[r],mode=mode,backend='fpylll')
   assert (a,b,c,r) in set(map(tuple,v['hits']))
   out.append(dict(triple=[a,b,c],residual=r,mode=mode,seconds=v['stats']['seconds'],hit_found=True,coverage='fixture-selected single patch only, NOT full shell'))
 Path('results/enumeration-large-controls.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':
 main()
 large_controls()
