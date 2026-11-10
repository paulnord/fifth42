"""Existing Cabbage GPU lease plus the unchanged NFS owner/allocator guards."""
from pathlib import Path
import fcntl,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'worker'))
import ada_export_store
JOB='cabbage-saved-root-20261108T222040Z';SHARED=Path('/mnt/nfs_share/fifth42-shared-20261107')
class Guard:
 def resources(self):return None
 def hardware_blockers(self):
  reasons=[]
  if os.uname().nodename.split('.')[0]!='cabbage':reasons.append('Wrong host')
  if subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():reasons.append('GPU occupied')
  if os.getloadavg()[0]>=17:reasons.append('Load ceiling')
  return reasons
 def acquire_leases(self,resources,wait):
  assert not wait and not self.hardware_blockers()
  s=ada_export_store.Store(SHARED)
  with s.locked(SHARED/'reservations.jsonl') as fd:claims=s.claims(fd)
  original=next(x for x in claims if x['job']==JOB)
  assert original['sha256']=='364221db0023ea69fa18b47eb512e9e83362f6d598fc19c101e74b72f4f3d1c8'
  for i,a in enumerate(claims):
   for b in claims[i+1:]:assert not(a['first']<b['last'] and b['first']<a['last']),('Reservation overlap',a['job'],b['job'])
  (ROOT/'evidence/reservations-verified.json').write_text(json.dumps(dict(status='passed',claims=[{k:x[k] for k in ['job','first','last','sha256']} for x in claims]),indent=2)+'\n')
  handles=[]
  try:
   for p in [Path('/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-runtime/gpu-owner.lock'),SHARED/'jobs'/JOB/'journal.jsonl']:
    h=p.open('r+');fcntl.lockf(h,fcntl.LOCK_EX|fcntl.LOCK_NB);handles.append(h)
   return handles,[]
  except BaseException:
   for h in handles:h.close()
   raise
def helper():return Guard()
