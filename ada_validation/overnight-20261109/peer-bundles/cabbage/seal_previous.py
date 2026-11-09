"""Verify and retain a stopped local journal and its final replica."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,fcntl,hashlib,json,os,shutil,subprocess,sys,time,tarfile,tempfile
import parallel_audit
R=Path(__file__).resolve().parent;E=R/'evidence'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024**2),b''):h.update(b)
 return h.hexdigest()
def save(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def seal(config,evidence):
 c=json.loads(Path(config).read_bytes());run=Path(c['output']);rep=Path(c['replica_output']);cp_raw=(run/'checkpoint.json').read_bytes();cp=json.loads(cp_raw)
 sup=json.loads((run.parent/'supervisor.json').read_bytes());status=json.loads((run/'status.json').read_bytes())
 assert sup['worker_exit_code']==0 and sup['leases_released'] and sup['error'] is None
 assert status['status']=='stopped' and status['error'] is None and status['journal_buffer']['pending_chunks']==0
 assert (rep/'checkpoint.json').read_bytes()==cp_raw
 final=json.loads((run/'final-replica.json').read_bytes());assert final['status']=='verified' and final['receipt']['checkpoint_sha256']==hashlib.sha256(cp_raw).hexdigest()
 assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
 locks=[]
 try:
  for p in [Path(c['ledger_root'])/'jobs'/c['ledger_job']/'journal.jsonl',Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock')]:
   fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW);fcntl.lockf(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);locks.append(fd)
  print('Auditing complete stopped parent',cp['chunks'],'chunks',flush=True);checked=parallel_audit.audit(run,c)
  raw_sha=sha(run/'coverage.jsonl');assert raw_sha==final['receipt']['raw_sha256']==sha(rep/'coverage.jsonl')
  q=dict(original_owner_lock_acquired=True,gpu_lease_acquired=True,gpu_compute_processes=[],worker_exit_code=0,worker_leases_released=True)
  audit=dict(checked,captured_checkpoint_sha256=hashlib.sha256(cp_raw).hexdigest(),committed_chain_sha256=cp['journal_sha256'],committed_raw_sha256=raw_sha,selected_interval=[c['initial_patch'],cp['next_patch']],uncommitted_trailing_bytes=0,quiescence=q,source_closed=True)
  archive=Path('/mnt/fifth42-storage/archives')/('CABBAGE-EXTENDED-PARENT-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()));archive.mkdir(mode=0o700)
  names={'checkpoint.json':run/'checkpoint.json','status.json':run/'status.json','supervisor.json':run.parent/'supervisor.json','configuration.json':Path(config),'source-manifest.json':Path(c['manifest']),'final-replica.json':run/'final-replica.json','prior-parent-archive-receipt.json':Path(c['parent_archive_receipt'])}
  for name,p in names.items():shutil.copy2(p,archive/name);assert sha(archive/name)==sha(p)
  save(archive/'parent-audit.json',audit);os.link(rep/'coverage.jsonl',archive/'coverage.jsonl')
  # Pack local immutable receipts once; avoid thousands of serialized NFS
  # metadata operations on already verified individual replica files.
  with tempfile.TemporaryFile(dir=R) as tmp:
   with tarfile.open(fileobj=tmp,mode='w') as tar:
    for p in sorted((run/'independent-audits').glob('*.json')):tar.add(p,arcname=p.name)
   tmp.seek(0)
   with (archive/'independent-audits.tar').open('xb') as dest:shutil.copyfileobj(tmp,dest,8*1024**2);dest.flush();os.fsync(dest.fileno())
  receipt=dict(status='verified',source=str(run),source_closed=True,source_retained=True,captured_next_patch=cp['next_patch'],committed_bytes=cp['journal_offset'],captured_checkpoint_sha256=audit['captured_checkpoint_sha256'],raw_sha256=raw_sha,journal_chain_sha256=cp['journal_sha256'],metadata_sha256={name:sha(archive/name) for name in names},archive_method='Retained read-only verified replica inode; separate local journal retained')
  save(archive/'ARCHIVE_RECEIPT.json',receipt)
  for p in archive.rglob('*'):
   if p.is_file():p.chmod(0o400)
  fd=os.open(archive,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd);archive.chmod(0o500)
  evidence.mkdir(parents=True,exist_ok=True);save(evidence/'parent-audit.json',audit);save(evidence/'parent-archive-receipt.json',receipt)
  result=dict(archive=str(archive),checkpoint=cp,audit=audit,receipt=receipt,config_sha256=sha(config),manifest_sha256=c['manifest_sha256'],parent_selected_patches=cp['next_patch']-c['reservation_initial_patch'])
  save(evidence/'parent-seal.json',result);print('SEALED',archive,cp['next_patch'],flush=True);return result
 finally:
  for fd in locks:os.close(fd)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args();os.sched_setaffinity(0,set(range(16)));seal(a.config,a.evidence)
