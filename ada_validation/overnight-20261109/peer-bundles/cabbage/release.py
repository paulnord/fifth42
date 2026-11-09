"""Freeze a fresh continuation; each journal has its own immutable identity."""
from pathlib import Path
import hashlib,json,os,re,shutil
ROOT=Path(__file__).resolve().parent;DEADLINE=1794351600
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 p=Path(p)
 if p.exists():p.unlink()
 p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def freeze(root,previous,seal,claim=None,coverage=None):
 root=Path(root);w=root/'worker';old=json.loads(Path(previous).read_bytes());cp=seal['checkpoint'];archive=Path(seal['archive'])
 if not w.exists():shutil.copytree(ROOT/'worker',w,ignore=shutil.ignore_patterns('__pycache__','base-config.json','release-manifest.json'))
 original=claim or json.loads(Path(old['origin_claim_file']).read_bytes());fresh=claim is not None
 first,last=original['first'],original['last'];initial=first if fresh else cp['next_patch']
 assert first<=initial<last
 for p,v in [(w/'origin-claim.json',original),(w/'parent-audit.json',seal['audit']),(w/'parent-archive-receipt.json',seal['receipt']),(w/'origin-config.json',old),(w/'reservation-metadata.json',coverage if fresh else json.loads(Path(old['coverage_file']).read_bytes()))]:write(p,v)
 # Preserve the precise original proof bytes when inheriting the old claim.
 if not fresh:
  for name,key in [('origin-claim.json','origin_claim_file'),('reservation-metadata.json','coverage_file')]:
   (w/name).unlink();shutil.copy2(old[key],w/name)
 else:
  assert sha(w/'reservation-metadata.json')==original['coverage']['sha256']
 policy=w/'cabbage_policy.py';s=policy.read_text()
 s=re.sub(r"JOB='[^']+'",f"JOB={original['job']!r}",s);s=re.sub(r"CLAIM='[^']+'",f"CLAIM={original['sha256']!r}",s);s=re.sub(r"RESERVATION='[^']+'",f"RESERVATION={original['identity']!r}",s)
 s=re.sub(r'FIRST=\d+;LAST=\d+;DEADLINE=\d+',f'FIRST={first};LAST={last};DEADLINE={DEADLINE}',s);policy.write_text(s)
 run=root.name;local=Path('/home/pnord/fifth42-local-runs')/original['job']/run/'run';replica=Path('/mnt/fifth42-storage/runs')/original['job']/run/'run'
 for p in [local.parent,replica.parent]:p.mkdir(mode=0o700,parents=True,exist_ok=False)
 files={str(p.relative_to(w)):sha(p) for p in sorted(w.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ['base-config.json','release-manifest.json'] and not p.name.endswith(('.log','.lock'))}
 m=json.loads(Path(old['manifest']).read_bytes());m.update(status='frozen_cabbage_extended',files=files,predecessor_manifest_sha256=old['manifest_sha256'],authorized_deadline='2026-11-10T17:00:00-06:00');write(w/'release-manifest.json',m)
 c=dict(old,run_id=run,initial_patch=initial,range_end=last,parent_run=str(archive),parent_selected_patches=0 if fresh else initial-first,parent_final_cursor=cp['next_patch'],fresh_reservation=fresh,
  output=str(local),replica_output=str(replica),manifest=str(w/'release-manifest.json'),manifest_sha256=sha(w/'release-manifest.json'),
  ledger_job=original['job'],ledger_claim_sha256=original['sha256'],reservation_manifest_sha256=original['identity'],reservation_initial_patch=first,
  origin_claim_file=str(w/'origin-claim.json'),origin_claim_file_sha256=sha(w/'origin-claim.json'),coverage_file=str(w/'reservation-metadata.json'),coverage_sha256=sha(w/'reservation-metadata.json'),
  parent_checkpoint_sha256=sha(archive/'checkpoint.json'),parent_status_sha256=sha(archive/'status.json'),parent_journal_sha256=cp['journal_sha256'],parent_journal_offset=cp['journal_offset'],parent_journal_raw_sha256=seal['audit']['committed_raw_sha256'],parent_identity=cp['identity'],
  parent_audit_file=str(w/'parent-audit.json'),parent_audit_sha256=sha(w/'parent-audit.json'),parent_archive_receipt=str(archive/'ARCHIVE_RECEIPT.json'),parent_archive_receipt_sha256=sha(archive/'ARCHIVE_RECEIPT.json'),
  stop_epoch=DEADLINE,stop_local='2026-11-10T17:00:00-06:00',service_name='fifth-'+run+'.service',deadline_service_name='fifth-'+run+'-deadline.service',cleanup_service_name='fifth-'+run+'-final-copy.service')
 st=(archive/'coverage.jsonl').stat();c['parent_journal_identity']=[st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
 write(root/'production-config.json',c);write(w/'base-config.json',c)
 for p in [w/'release-manifest.json',w/'base-config.json',root/'production-config.json']:p.chmod(0o400)
 return root/'production-config.json'
if __name__=='__main__':
 seal=json.loads((ROOT/'evidence/parent-seal.json').read_bytes());print(freeze(ROOT,Path('/home/pnord/scratch/cabbage-buffered-20261109/production-config.json'),seal))
