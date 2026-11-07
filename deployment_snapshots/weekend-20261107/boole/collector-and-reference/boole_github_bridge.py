"""Run on Ada: publish read-only Boole snapshots using Ada's existing Git credential."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,fcntl,hashlib,json,os,subprocess,tempfile,time
SHARE=Path('/mnt/nfs_share/boole-publishing-20261107')
ROOT=Path('/home/pnord/boole-reporting-bridge-20261107')
PUBLIC='boole_validation/precision-weekend-20261107'
BRANCH='handoff/fifth-lattice-optimizations-20261105'
REMOTE='git@github.com:paulnord/fifth42.git'
def utc():return datetime.now(timezone.utc).isoformat()
def atomic(path,obj):
 temp=path.with_name(path.name+'.'+str(os.getpid())+'.tmp')
 with temp.open('w') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(temp,path)
def render(row):
 cp=row['checkpoint'];m=row['worker_metrics']
 return f"""# Boole adaptive-precision search

Updated: {row['snapshot_utc']}

State: **{row['phase']}**. GPU with {row['workers']} preparation workers.
Committed patches: **{cp['patches']:,}** in {cp['chunks']:,} chunks.
Current cursor: **{cp['next_patch']}**. Reserved interval: {row['reserved_interval']}.
Observed worker rate: **{m['patches_per_second']:.0f} patches/s**; independent GMP audits: {m['gmp_audited_chunks']}.
Deadline: **{row['stop_local']}**. Console-independent worker and deadline timer on Boole; reporter on Ada.
Alerts: {row['alerts'] or 'None reported'}.

Source manifest: `{row['manifest_sha256']}`.
Selected early-interval coverage only. Ada's coverage is separate. No completed full-box bound.
Journal budget: {row['journal_limit_bytes']//1024**3} GiB; storage limits may stop the run before Monday.

[Ada's separate search](../../ada_validation/weekend-20261106/STATUS.md).
"""
def snapshot():
 spec=json.loads((SHARE/'publication-spec.json').read_text());row=json.loads((SHARE/'status.json').read_text())
 if row['host']!='boole' or row.get('TEST_ONLY') is not False or row['run_id']!=spec['run_id']:raise RuntimeError('Wrong Boole snapshot')
 for k in ['manifest_sha256','config_sha256','ledger_claim_sha256']:
  if row[k]!=spec[k]:raise RuntimeError('Boole immutable identity changed: '+k)
 if row['committed_interval']!=[row['reserved_interval'][0],row['checkpoint']['next_patch']]:raise RuntimeError('Coverage mismatch')
 age=time.time()-datetime.fromisoformat(row['snapshot_utc']).timestamp()
 if age>120 and row['phase']!='stopped':raise RuntimeError('Boole collector snapshot stale')
 return row
def git(*args,data=None,env=None,check=True):
 environment=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_AUTHOR_NAME='Boole lattice runner',GIT_COMMITTER_NAME='Boole lattice runner',GIT_AUTHOR_EMAIL='boole-lattice@users.noreply.github.com',GIT_COMMITTER_EMAIL='boole-lattice@users.noreply.github.com',GIT_SSH_COMMAND='ssh -i /home/pnord/.ssh/fifth42_status_20261105 -o IdentitiesOnly=yes -o IdentityAgent=none -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 -o UserKnownHostsFile=/home/pnord/fifth-lattice-gpu/github_known_hosts')
 environment.update(env or {})
 p=subprocess.run(['git','--git-dir',str(ROOT/'repository.git'),*args],input=data,capture_output=True,text=True,env=environment,timeout=45)
 if check and p.returncode:raise RuntimeError('git '+args[0]+': '+p.stderr.strip())
 return p
def publish(row):
 if not (ROOT/'repository.git/HEAD').exists():git('init','--bare',str(ROOT/'repository.git'))
 files={PUBLIC+'/STATUS.md':render(row),PUBLIC+'/status.json':json.dumps(row,indent=2)+'\n'}
 spec=json.loads((SHARE/'publication-spec.json').read_text())
 for name,expected in spec.get('evidence',{}).items():
  if Path(name).name!=name:raise RuntimeError('Invalid evidence filename')
  raw=(SHARE/'evidence'/name).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=expected:raise RuntimeError('Frozen evidence changed')
  files[PUBLIC+'/evidence/'+name]=raw.decode()
 for attempt in range(3):
  git('fetch','--depth=1',REMOTE,'refs/heads/'+BRANCH);parent=git('rev-parse','FETCH_HEAD').stdout.strip()
  with tempfile.TemporaryDirectory(dir=ROOT) as temp:
   env={'GIT_INDEX_FILE':str(Path(temp)/'index')};git('read-tree',parent,env=env)
   for name,contents in files.items():
    blob=git('hash-object','-w','--stdin',data=contents).stdout.strip();git('update-index','--add','--cacheinfo','100644',blob,name,env=env)
   tree=git('write-tree',env=env).stdout.strip();commit=git('commit-tree',tree,'-p',parent,data='Update Boole precision search: '+row['snapshot_utc']+'\n').stdout.strip()
  p=git('push','--porcelain',REMOTE,commit+':refs/heads/'+BRANCH,check=False)
  if p.returncode==0:
   receipt=dict(status='published',commit=commit,run_id=row['run_id'],snapshot_utc=row['snapshot_utc'],published_utc=utc(),phase=row['phase'],next_patch=row['checkpoint']['next_patch']);atomic(SHARE/'ada-publication-receipt.json',receipt);return receipt
  head=git('ls-remote',REMOTE,'refs/heads/'+BRANCH).stdout.split()
  if not head or head[0]==parent or attempt==2:raise RuntimeError('GitHub push failed: '+p.stderr.strip())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--once',action='store_true');a=ap.parse_args()
 if a.preview:print(render(snapshot()));return 0
 if os.uname().nodename.split('.')[0]!='ada':raise RuntimeError('Bridge credential stays on Ada')
 ROOT.mkdir(mode=0o700,exist_ok=True)
 with (ROOT/'publisher.lock').open('a+') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);next_push=0;terminal_since=None
  if (SHARE/'ada-publication-receipt.json').exists() and not a.once:
   old=json.loads((SHARE/'ada-publication-receipt.json').read_text());next_push=datetime.fromisoformat(old['published_utc']).timestamp()+900
  while time.time()<1794236400+1800:
   try:
    row=snapshot();terminal=row['phase']=='stopped';terminal_since=(terminal_since or time.monotonic()) if terminal else None
    final=terminal_since is not None and time.monotonic()-terminal_since>=15
    if a.once or final or (not terminal and time.time()>=next_push):
     receipt=publish(row);print(json.dumps(receipt),flush=True);next_push=time.time()+900
     if final or a.once:return 0
   except Exception as e:
    atomic(SHARE/'ada-bridge-health.json',dict(status='error',updated_utc=utc(),error=repr(e)))
    print(json.dumps({'error':repr(e),'updated_utc':utc()}),flush=True)
    if a.once:return 1
   time.sleep(15)
  return 2
if __name__=='__main__':raise SystemExit(main())
