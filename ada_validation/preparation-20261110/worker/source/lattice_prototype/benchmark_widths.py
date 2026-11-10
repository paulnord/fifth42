"""Uniform certified patch-width experiment, complete bounded domain only."""
import json, statistics
from pathlib import Path
import lattice5 as l
import modular_filters as f

def main():
 rows=[]
 oracle=l.signed_reference(1000,42)
 for width in [1,2,4,8]:
  runs=[]
  try:
   for _ in range(3):
    r=f.signed42_filtered(1000,mode='interval',backend='fpylll',width=width)
    assert set(map(tuple,r['signed_hits']))==oracle
    runs.append(r['stats']['seconds'])
   rows.append(dict(width=width,seconds=runs,median_seconds=statistics.median(runs),stats=r['stats'],complete=True,oracle_equal=True))
  except l.BudgetExceeded as e:
   rows.append(dict(width=width,complete=False,error=str(e)))
  Path('results/width-benchmark.json').write_text(json.dumps(rows,indent=2))
  print(rows[-1],flush=True)
 # Nonempty exact target2951 checks wider covering as well as empty target42.
 for width in [1,2,4,8]:
  r=f.search_targets_positive(100,[2951],mode='interval',backend='fpylll',width=width)
  assert set(map(tuple,r['hits']))=={(42,71,72,2951)}
 rows.append(dict(nonempty_all_widths=True,hit=[42,71,72,2951]))
 Path('results/width-benchmark.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
