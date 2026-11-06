from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent/'fifth42-coordinator-20261105'
sys.path[:0]=[str(ROOT.parent/'fifth42-coordinator-deps'),str(REPO/'lattice_gpu')]
import scaling_core as c, overnight_search as n, wider_patch_experiment as w
c.initialize(REPO/'lattice_prototype');c.MAX_BOUND=n.MAX_BASE
sets={
 'small1000':c.specs(1000,42,8),
 'controls100':c.specs(100,2951,8),
 'high8':(w.shared_specs(8),[]),
 'high32':(w.shared_specs(32),[]),
}
rows={}
for name,(specs,direct) in sets.items():
 start=time.perf_counter();tasks=[];tokens=[]
 for spec in specs:
  task=c.prepare_task(spec);tokens.append(c.certify_task(task));tasks.append(task)
 batch=c.encode_batch(tasks,specs[0][-2]);packet=batch.packet
 (ROOT/(name+'.packet')).write_text(packet)
 (ROOT/(name+'.tasks.json')).write_text(json.dumps([__import__('dataclasses').asdict(t) for t in tasks]))
 rows[name]=dict(patches=len(tasks),points=sum(t.points for t in tasks),direct=direct,sha256=hashlib.sha256(packet.encode()).hexdigest(),certificate_sha256=hashlib.sha256('\n'.join(tokens).encode()).hexdigest(),preparation_seconds=time.perf_counter()-start)
 print(name,rows[name],flush=True)
(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
