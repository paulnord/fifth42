"""Finite actual-GPU, exact-GMP and NFS Store/TrialJournal acceptance."""
import copy,errno,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
review=root/'review-bundle'
variant=sys.argv[1]
assert variant in ('baseline','candidate')
sys.path.insert(0,str(review));import cabbage_export_store as store
source=review/variant/'source/lattice_prototype'
sys.path.insert(0,str(review/variant/'source/lattice_gpu'))
import overnight_search as night,scaling_core as core,packing_opt,adapter_runtime as adapter,coordinator_pipeline as pipeline
from engine_session import EngineSession
night.initialize(source)
share=Path((root/'nfs-root.txt').read_text().strip())
assert share.name.startswith('TEST_ONLY_cabbage_saved_root_')
identity=hashlib.sha256((review/'STAGED-MANIFEST.json').read_bytes()).hexdigest()
local=root/'nfs-local-evidence'/variant;local.mkdir(parents=True,exist_ok=False)
class Serial:
 def map(self,f,items,chunksize):return list(map(f,items))
def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(stable(x)).hexdigest()
def oracle(bound,cap):
 p=[n**5 for n in range(bound+1)]
 return {(a,b,c,p[a]+p[b]-p[c]) for c in range(1,bound+1) for b in range(1,c) for a in range(1,b+1) if abs(p[a]+p[b]-p[c])<=cap}
def gmp(batch):
 p=subprocess.run([str(review/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=15)
 return json.loads(p.stdout)
records={};executions=[]
with EngineSession([str(review/'bin/scaling_gpu')],'gpu',time.monotonic()+150) as session:
 def exact(batch):
  got,wall=session.run(batch.packet,timeout=20);pipeline.validate_response_types(got)
  ref=gmp(batch)
  assert adapter.normalized_counts(batch,got)==adapter.normalized_counts(batch,ref),'GMP counts'
  assert adapter.normalized_hits(batch,got)==adapter.normalized_hits(batch,ref),'GMP native records'
  hits=core.decode_batch(batch,got,'gpu')
  assert hits==core.decode_batch(batch,ref,'emulated'),'GMP decoded hits'
  return got,hits
 controls=[]
 for bound,cap in ((34,42),(100,2951)):
  specs,direct=core.specs(bound,cap,8);prep=[pipeline.prepare_certified(s) for s in specs]
  plan=packing_opt.assemble(bound,cap,specs,direct,[r[0] for r in prep],[r[1] for r in prep])
  found=set(plan.direct_hits);counts=[];native=[]
  for b in plan.batches:
   got,h=exact(b);found|=h;counts.extend(adapter.normalized_counts(b,got));native.extend(adapter.normalized_hits(b,got))
  expected=oracle(bound,cap);assert found==expected and found
  controls.append(dict(bound=bound,cap=cap,hits=sorted(found),counts=counts,native_hits=native))
 FIRST=3000000000
 def evaluate(first,last):
  window=pipeline.Window(100000000001,200000000000,first,last,8,222,42,'adaptive')
  chunk=pipeline.prepare_chunk(Serial(),window,'packed')
  record=pipeline.execute_chunk(chunk,pipeline.OwnedEngine(session),trial='nfs-'+variant,coordinator=0,timeout=20)
  for b,receipt in zip(chunk.plan.batches,record['batches']):
   ref=gmp(b)
   assert list(map(tuple,receipt['native_counts']))==adapter.normalized_counts(b,ref),'High GMP counts'
   assert list(map(tuple,receipt['native_hit_records']))==adapter.normalized_hits(b,ref),'High GMP records'
  records[(first,last)]=(window,record)
  executions.append((first,last))
  result=dict(complete=True,first=first,last=last,identity=identity,tasks=last-first,points=chunk.plan.points,certificate_sha256=chunk.plan.certificate_sha256,exact_checks=True,hits=record['hits'],packets=[dict(points=r['points'],visited=sum(n[2] for n in r['native_counts']),counts_sha256=digest(r['native_counts']),packet_sha256=r['identity']['packet_sha256'],response_sha256=r['response_sha256']) for r in record['batches']])
  (local/f'{first}-{last}.json').write_text(json.dumps(dict(prepared_window=window.identity(),record=record,store_result=result),indent=2)+'\n')
  return result
 # Real fsync failure after the first durable chunk: recovery must roll forward
 # without enumerating that chunk a second time.
 s=store.Store(share/('gpu-'+variant));claim=s.reserve('recover',FIRST,FIRST+512,identity)
 calls=[0]
 def fail_checkpoint(event):
  if event=='fsync_checkpoint':
   calls[0]+=1
   if calls[0]==2:raise OSError(errno.EIO,'TEST_ONLY injected checkpoint fsync failure')
 s.inject=fail_checkpoint
 try:s.run('recover',identity,evaluate);raise AssertionError('Expected injected checkpoint error')
 except OSError as e:assert e.errno==errno.EIO
 s.inject=lambda e:None
 before=list(executions);state=s.run('recover',identity,evaluate)
 assert state['complete'] and state['chunks']==2
 assert executions.count((FIRST,FIRST+256))==1,'Durable chunk rerun'
 assert executions.count((FIRST+256,FIRST+512))==1
 again=s.run('recover',identity,lambda *_:(_ for _ in ()).throw(AssertionError('Completed range rerun')))
 assert again==state
 # The actual production pipeline journal also commits and recovers on NFS.
 window,record=records[(FIRST,FIRST+256)]
 jdir=share/('pipeline-'+variant)
 with pipeline.TrialJournal(jdir,dict(trial=variant,source_identity=identity),window) as journal:
  journal.commit(record);checkpoint=dict(journal.state)
 with pipeline.TrialJournal(jdir,dict(trial=variant,source_identity=identity),window) as recovered:assert recovered.state==checkpoint
 try:
  with pipeline.TrialJournal(jdir,dict(trial=variant,source_identity='0'*64),window):pass
  raise AssertionError('Changed TrialJournal identity accepted')
 except ValueError:pass
 # New isolated cases use actual audited GPU receipts, with intentional errors
 # injected only at this test's NFS file descriptors.
 s.reserve('partial',FIRST+512,FIRST+768,identity)
 original=store.write_all;failed=[False]
 def diskfull(fd,data):
  target=os.readlink('/proc/self/fd/'+str(fd))
  if target.endswith('/jobs/partial/journal.jsonl') and not failed[0]:
   failed[0]=True;original(fd,data[:31]);raise OSError(errno.ENOSPC,'TEST_ONLY injected partial append')
  original(fd,data)
 store.write_all=diskfull
 try:
  try:s.run('partial',identity,evaluate);raise AssertionError('Expected partial-write failure')
  except OSError as e:assert e.errno==errno.ENOSPC
 finally:store.write_all=original
 partial=s.run('partial',identity,evaluate)
 assert partial['complete'] and partial['chunks']==1
 assert len(list((s.root/'jobs/partial').glob('uncommitted-tail.*.bin')))==1
 # Reject changed runtime identities before any new evaluation.
 try:s.run('partial','0'*64,evaluate);raise AssertionError('Changed identity accepted')
 except store.Integrity:pass
 # Deliberate incomplete count cannot advance a fresh claim.
 s.reserve('incomplete',FIRST+768,FIRST+1024,identity)
 template=copy.deepcopy(evaluate(FIRST+768,FIRST+1024));template['packets'][0]['visited']-=1
 try:s.run('incomplete',identity,lambda *_:template);raise AssertionError('Bad count accepted')
 except store.Integrity:pass
 cp=json.loads((s.root/'jobs/incomplete/checkpoint.json').read_text());assert cp['next_patch']==FIRST+768 and cp['chunks']==0
 assert (s.root/'jobs/incomplete/journal.jsonl').stat().st_size==0
 # Tamper only with a completed TEST_ONLY journal; it must fail closed.
 checkpoint_path=s.root/'jobs/partial/checkpoint.json';saved=checkpoint_path.read_bytes()
 jp=s.root/'jobs/partial/journal.jsonl';data=jp.read_bytes();assert b'"complete":true' in data
 jp.write_bytes(data.replace(b'"complete":true',b'"complete":false',1))
 try:s.run('partial',identity,evaluate);raise AssertionError('Tampered journal accepted')
 except store.Integrity:pass
 assert checkpoint_path.read_bytes()==saved
 signatures=[]
 for key,(w,r) in sorted(records.items()):
  signatures.append(dict(window=w.identity(),patches=r['patches'],points=r['points'],geometry=r['geometry_sha256'],certificates=r['certificate_sha256'],counts=[b['native_counts'] for b in r['batches']],native_hits=[b['native_hit_records'] for b in r['batches']],packet_hashes=[b['identity']['packet_sha256'] for b in r['batches']],hits=r['hits']))
 report=dict(status='passed',TEST_ONLY=True,production_coverage=False,variant=variant,manifest_sha256=identity,controls=controls,signatures=signatures,executions=executions,durable_chunk_not_repeated=True,store_checkpoint_recovery=True,pipeline_journal_recovery=True,changed_identity_rejected=True,partial_append_recovered=True,incomplete_count_rejected=True,tampering_rejected=True,ledger=str(s.root),limitations=['Single Cabbage NFS client; no Ada/Boole process or live-ledger access.','Staged storage adapter adds Cabbage host and fresh test-root verification; no production worker launch.'])
 (root/f'nfs-{variant}-results.json').write_text(json.dumps(report,indent=2)+'\n')
 print(variant,'passed actual GPU/GMP and NFS recovery acceptance',flush=True)
