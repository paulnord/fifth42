"""Export bounded exact-certified replay packets; no coverage claim."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; W=ROOT/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import runtime_initialize,buffered_pipeline as b,coordinator_pipeline as p
runtime_initialize.initialize(W/'source/lattice_prototype')
class Serial:
 def map(self,f,args,chunksize):return list(map(f,args))
out=Path(sys.argv[1]);out.mkdir(exist_ok=False);rows=[]
for label,first in [('ada',4564955776),('cabbage',2572492928),('dense',9562500096)]:
 for group in (4,8,16):
  c=b.prepare_cached(Serial(),p.Window(100000000001,200000000000,first,first+256,8,222,42,'adaptive'),group);b.validate_cached(c)
  for i,batch in enumerate(c.plan.batches):
   name=f'{label}-g{group}-{i}.packet';(out/name).write_text(batch.packet)
   rows.append(dict(file=name,first=first,last=first+256,group=group,points=batch.points))
(out/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
