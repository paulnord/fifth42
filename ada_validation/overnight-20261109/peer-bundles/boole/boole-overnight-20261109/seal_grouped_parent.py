"""Seal the stopped combined run and its already verified NFS replica in place."""
from datetime import datetime,timezone
import fcntl,hashlib,json,os,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OLD=Path('/home/pnord/boole-buffered-20261109');W=OLD/'worker'
sys.path[:0]=[str(W),str(W/'source/lattice_gpu')]
import policy
from audit_grouped import audit_suffix
from durable_mirror import atomic

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for data in iter(lambda:f.read(8*1024**2),b''):h.update(data)
 return h.hexdigest()
def identity(s):return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def main():
 os.umask(0o077);os.nice(19);os.sched_setaffinity(0,{0});start=time.monotonic()
 c=json.loads((W/'production-config.json').read_bytes());policy.verify_sources(c);policy.validate_parent(c);local=Path(c['output']);replica=Path(c['replica_output'])
 until=time.monotonic()+600
 while not (local/'final-replica.json').exists():
  assert time.monotonic()<until,'Final copy did not finish';time.sleep(2)
 final=json.loads((local/'final-replica.json').read_bytes());assert final['status']=='verified'
 cpraw=(local/'checkpoint.json').read_bytes();cp=json.loads(cpraw)
 assert cpraw==(replica/'checkpoint.json').read_bytes()
 st=json.loads((local/'status.json').read_bytes());sup=json.loads((local.parent/'supervisor.json').read_bytes())
 assert st['status']=='stopped' and st['error'] is None and sup['leases_released']
 assert sup['error']=="Busy('/mnt/nfs_share/fifth42-shared-20261107/reservations.jsonl')",'Unexpected old supervisor failure'
 assert st['journal_buffer']['pending_chunks']==st['journal_buffer']['pending_bytes']==0
 assert sup.get('all_owned_processes_exited_utc') and sup['status']=='failed'
 import subprocess
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
 assert subprocess.check_output(['systemctl','--user','show',c['service_name'],'-p','ActiveState','--value'],text=True).strip()=='inactive' 
 assert (replica/'coverage.jsonl').stat().st_size==cp['journal_offset']==(local/'coverage.jsonl').stat().st_size
 assert final['receipt']['next_patch']==cp['next_patch'] and final['receipt']['checkpoint_sha256']==hashlib.sha256(cpraw).hexdigest()
 import ada_export_store
 store=ada_export_store.Store(c['ledger_root']);until=time.monotonic()+2
 while True:
  try:claim=store.claim(c['ledger_job']);break
  except ada_export_store.Busy:
   assert time.monotonic()<until;time.sleep(.02)
 assert claim==json.loads((W/'origin-claim.json').read_bytes()) and claim['sha256']==c['ledger_claim_sha256']
 with store.locked(store.root/'jobs'/c['ledger_job']/'journal.jsonl'):
  baseline=dict(checkpoint=dict(next_patch=c['initial_patch']),config=c)
  print(json.dumps(dict(phase='auditing_local_grouped_parent',chunks=cp['chunks'],bytes=cp['journal_offset'])),flush=True)
  a=audit_suffix(local,baseline,cp,'fresh',c['gmp_audit_period'])
  print(json.dumps(dict(phase='auditing_replica_grouped_parent',local_audit=a)),flush=True)
  b=audit_suffix(replica,baseline,cp,'fresh',c['gmp_audit_period']);assert a==b
  localhash=sha(local/'coverage.jsonl')
  with (replica/'coverage.jsonl').open('rb') as f:
   fcntl.lockf(f,fcntl.LOCK_SH|fcntl.LOCK_NB)
   before=os.fstat(f.fileno());h=hashlib.sha256()
   for data in iter(lambda:f.read(8*1024**2),b''):h.update(data)
   after=os.fstat(f.fileno());assert identity(before)==identity(after)
  assert h.hexdigest()==localhash==final['receipt']['raw_sha256']
  assert (local/'checkpoint.json').read_bytes()==cpraw==(replica/'checkpoint.json').read_bytes()
  audit=dict(status='passed',final_checkpoint=True,read_only=True,parent_run=str(local),sealed_replica=str(replica),
   first=c['initial_patch'],next_patch=cp['next_patch'],selected_interval=[c['initial_patch'],cp['next_patch']],chunks=cp['chunks'],points=cp['points'],patches=cp['patches'],
   hits=cp['hits'],gmp_audited_chunks=a['new_gmp_audited_chunks'],captured_checkpoint_sha256=hashlib.sha256(cpraw).hexdigest(),checkpoint_sha256=hashlib.sha256(cpraw).hexdigest(),
   committed_chain_sha256=cp['journal_sha256'],committed_raw_sha256=localhash,committed_bytes=cp['journal_offset'],uncommitted_trailing_bytes=0,
   journal_sha256=cp['journal_sha256'],journal_raw_sha256=localhash,journal_offset=cp['journal_offset'],status_sha256=sha(local/'status.json'),claim_sha256=claim['sha256'],
   local_grouped_audit=a,replica_grouped_audit=b,verified_utc=policy.utc(),completed_bound=None,
   prior_supervisor_failure=sup['error'],prior_worker_status=st['status'],limitation='Complete committed receipt, native-count and recorded GMP audit plus full local/replica byte comparison; historical coefficients not recomputed.')
  atomic(ROOT/'parent-audit.json',audit)
  sources={'configuration.json':W/'production-config.json','source-manifest.json':W/'release-manifest.json',
   'supervisor.json':local.parent/'supervisor.json','parent-audit.json':ROOT/'parent-audit.json','lineage.json':W/'parent-lineage.json'}
  hashes={}
  for name,path in sources.items():
   assert not (replica/name).exists(),'Existing sealed metadata must be preserved: '+name
   shutil.copy2(path,replica/name)
   with (replica/name).open('rb') as f:os.fsync(f.fileno())
   hashes[name]=sha(path);assert sha(replica/name)==hashes[name]
  receipt=dict(status='verified',source=str(local),archive=str(replica),source_closed=True,source_retained=True,sealed_verified_replica=True,
   captured_checkpoint_sha256=hashlib.sha256(cpraw).hexdigest(),captured_next_patch=cp['next_patch'],captured_chunks=cp['chunks'],
   committed_bytes=cp['journal_offset'],raw_sha256=localhash,journal_chain_sha256=cp['journal_sha256'],metadata_sha256=hashes,
   final_copy_receipt=final['receipt'],verified_utc=policy.utc())
  assert not (replica/'ARCHIVE_RECEIPT.json').exists()
  atomic(replica/'ARCHIVE_RECEIPT.json',receipt);atomic(ROOT/'parent-archive-receipt.json',receipt)
  lineage=json.loads((W/'parent-lineage.json').read_bytes())
  lineage['segments'].append(dict(archive=str(replica),receipt_sha256=sha(replica/'ARCHIVE_RECEIPT.json'),checkpoint_sha256=sha(replica/'checkpoint.json'),
   first=c['initial_patch'],last=cp['next_patch'],journal_offset=cp['journal_offset'],journal_sha256=cp['journal_sha256'],raw_sha256=localhash))
  lineage['covered_interval']=[3000000000,cp['next_patch']];atomic(ROOT/'parent-lineage.json',lineage)
  atomic(ROOT/'sealed-parent.json',dict(status='verified',archive=str(replica),initial_patch=cp['next_patch'],parent_journal_identity=identity(after),audit=audit,receipt=receipt,wall_seconds=time.monotonic()-start))
  print(json.dumps(dict(status='sealed',cursor=cp['next_patch'],bytes=cp['journal_offset'],wall_seconds=time.monotonic()-start)),flush=True)
if __name__=='__main__':main()
