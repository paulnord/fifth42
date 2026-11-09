"""Use the unchanged grouped auditor on independent byte spans; join every seam."""
from pathlib import Path
import concurrent.futures,hashlib,json,os,sys,multiprocessing as mp
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'worker'))
import audit_grouped
def part(args):
 run,c,cp,start,end=args;run=Path(run);first=last=None;points=patches=chunks=0;hits=set()
 with (run/'coverage.jsonl').open('rb') as f:
  f.seek(start)
  while f.tell()<end:
   raw=f.readline(end-f.tell());assert raw.endswith(b'\n');row=json.loads(raw)
   if first is None:first=row
   last=row;points+=row['points'];patches+=row['window']['last']-row['window']['first'];chunks+=1;hits.update(map(tuple,row['hits']))
  assert f.tell()==end and first is not None
 parent=dict(next_patch=first['window']['first'],chunks=first['sequence']-1,points=0,patches=0,hits=[],journal_sha256=first['previous_sha256'],journal_offset=start)
 target=dict(cp,chunks=last['sequence'],points=points,patches=patches,hits=sorted(hits),next_patch=last['window']['last'],journal_sha256=last['sha256'],journal_offset=end)
 checked=audit_grouped.audit_suffix(run,dict(checkpoint=parent,config=c),target,'append',c['gmp_audit_period'])
 assert checked['new_chunks']==chunks
 return dict(start=start,end=end,first_sequence=first['sequence'],last_sequence=last['sequence'],first_patch=first['window']['first'],last_patch=last['window']['last'],previous=first['previous_sha256'],chain=last['sha256'],points=points,patches=patches,chunks=chunks,hits=sorted(hits),audits=checked['new_gmp_audited_chunks'])
def audit(run,c,workers=16):
 run=Path(run);raw=(run/'checkpoint.json').read_bytes();cp=json.loads(raw);limit=cp['journal_offset']
 assert (run/'coverage.jsonl').stat().st_size==limit
 offsets=[0]
 with (run/'coverage.jsonl').open('rb') as f:
  for i in range(1,workers):
   f.seek(limit*i//workers);f.readline();off=f.tell()
   if offsets[-1]<off<limit:offsets.append(off)
 offsets.append(limit)
 with concurrent.futures.ProcessPoolExecutor(max_workers=workers,mp_context=mp.get_context('fork')) as pool:
  rows=list(pool.map(part,[(str(run),c,cp,a,b) for a,b in zip(offsets,offsets[1:])]))
 cursor=c['initial_patch'];sequence=points=patches=audits=0;chain='0'*64;hits=set();offset=0
 for row in rows:
  assert (row['start'],row['first_sequence'],row['first_patch'],row['previous'])==(offset,sequence+1,cursor,chain),'Segment seam mismatch'
  offset=row['end'];sequence=row['last_sequence'];cursor=row['last_patch'];chain=row['chain'];points+=row['points'];patches+=row['patches'];audits+=row['audits'];hits.update(map(tuple,row['hits']))
 assert (offset,sequence,cursor,chain,points,patches,sorted(hits))==(cp['journal_offset'],cp['chunks'],cp['next_patch'],cp['journal_sha256'],cp['points'],cp['patches'],cp['hits'])
 assert (run/'checkpoint.json').read_bytes()==raw
 return dict(status='passed',final_checkpoint=True,committed_bytes=limit,next_patch=cursor,new_chunks=sequence,new_patches=patches,new_gmp_audited_chunks=audits,segments=len(rows),unchanged_auditor_sha256=hashlib.sha256(Path(audit_grouped.__file__).read_bytes()).hexdigest())
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--workers',type=int,default=16);a=p.parse_args()
 os.sched_setaffinity(0,set(range(a.workers)));print(json.dumps(audit(a.run,json.loads(a.config.read_bytes()),a.workers),indent=2))
