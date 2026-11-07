#!/usr/bin/env python3
"""TEST ONLY. Exact Store methods; synthetic evaluator; separate Ada-export verifier."""
import argparse, datetime, fcntl, hashlib, importlib.util, json, os, signal, socket, subprocess, sys, time
from pathlib import Path
BASE=Path('/mnt/nfs_share')
ROOT=BASE/'TEST_ONLY_boole_ada_protocol_20261107_v1'
HERE=Path(__file__).resolve().parent
IDENT=hashlib.sha256(b'TEST_ONLY synthetic evaluator, no mathematical coverage v1').hexdigest()
DEADLINE=time.monotonic()+600
role=None

def wait(path):
 while not path.exists():
  if time.monotonic()>DEADLINE: raise TimeoutError(str(path))
  time.sleep(.1)
 return json.loads(path.read_text())

def emit(name,obj):
 p=ROOT/name; temp=p.with_name(p.name+'.'+str(os.getpid())+'.tmp')
 with temp.open('x') as f:
  json.dump(obj,f,sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
 os.replace(temp,p)
 fd=os.open(ROOT,os.O_DIRECTORY); os.fsync(fd); os.close(fd)

def verify(path):
 path=Path(path).resolve()
 if not path.is_relative_to(ROOT): raise RuntimeError('Outside isolated TEST_ONLY directory')
 host=socket.gethostname().split('.')[0]
 if host!=role: raise RuntimeError('Role must match actual hostname')
 fs=json.loads(subprocess.check_output(['findmnt','--json','-T',str(BASE),'-o','TARGET,SOURCE,FSTYPE,OPTIONS'],text=True,timeout=5))['filesystems'][0]
 if role=='boole':
  if fs['target']!=str(BASE) or fs['source']!='ada:/mnt/nfs_share' or fs['fstype'] not in ('nfs','nfs4'):raise RuntimeError('Wrong Ada client export')
  if any(x in fs['options'].split(',') for x in ['nolock','local_lock=all','local_lock=posix']):raise RuntimeError('Local POSIX locks forbidden')
 elif role=='ada':
  if fs['fstype'] not in ('ext4','xfs','btrfs') or fs['fstype'] in ('nfs','nfs4'):raise RuntimeError('Expected local server filesystem')
  exports=subprocess.check_output(['showmount','-e','localhost'],text=True,timeout=5)
  if not any(line.split() and line.split()[0]==str(BASE) for line in exports.splitlines()):raise RuntimeError('Ada export missing')
 ancestor=path
 while not ancestor.exists():ancestor=ancestor.parent
 return ancestor.stat().st_dev

def load():
 spec=importlib.util.spec_from_file_location('probe_exact_worker',HERE/'range_worker.py'); w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
 # Only verifier substituted, in memory for this test. Store and validation unchanged.
 w.verify_share=verify
 return w

def evaluate(first,last):
 h=hashlib.sha256(('SYNTHETIC '+str(first)+' '+str(last)).encode()).hexdigest()
 return dict(complete=True,first=first,last=last,identity=IDENT,tasks=last-first,points=0,certificate_sha256=h,exact_checks=True,packets=[dict(points=0,visited=0,counts_sha256=h,packet_sha256=h,response_sha256=h)],hits=[])

def retry(fn,w):
 while True:
  try:return fn()
  except w.Busy:
   if time.monotonic()>DEADLINE:raise
   time.sleep(.05)

def main():
 global role
 ap=argparse.ArgumentParser();ap.add_argument('role',choices=['ada','boole']);ap.add_argument('--holder',action='store_true');a=ap.parse_args();role=a.role
 verify(ROOT);ROOT.mkdir(mode=0o700,exist_ok=True)
 w=load();s=w.Store(ROOT/'ledger')
 if a.holder:
  def inject(event):
   if event=='before_evaluate' and not (ROOT/'initial-checkpoint.json').exists():emit('initial-checkpoint.json',json.loads((s.root/'jobs/recovery/checkpoint.json').read_text()))
   if event=='after_checkpoint':
    emit('ada-holder-ready.json',{'journal_inode':(s.root/'jobs/recovery/journal.jsonl').stat().st_ino})
    time.sleep(180)
  s.inject=inject;s.run('recovery',IDENT,evaluate,max_chunks=1);return
 if (ROOT/(role+'-result.json')).exists():raise RuntimeError('Do not reuse a completed probe directory')
 emit(role+'-ready.json',{'host':socket.gethostname(),'pid':os.getpid(),'synthetic':True})
 wait(ROOT/(('boole' if role=='ada' else 'ada')+'-ready.json'))
 try:
  retry(lambda:s.reserve(role+'-overlap',1000,1512,IDENT,{'TEST_ONLY':True}),w);outcome='accepted'
 except w.Conflict:outcome='conflict'
 emit(role+'-claim.json',{'outcome':outcome})
 other=wait(ROOT/(('boole' if role=='ada' else 'ada')+'-claim.json'))
 assert sorted([outcome,other['outcome']])==['accepted','conflict']
 start=2000 if role=='ada' else 2256
 retry(lambda:s.reserve(role+'-adjacent',start,start+256,IDENT,{'TEST_ONLY':True}),w)
 emit(role+'-adjacent.json',{'accepted':True})
 wait(ROOT/(('boole' if role=='ada' else 'ada')+'-adjacent.json'))
 def read_claims():
  with s.locked(s.root/'reservations.jsonl') as fd:
   return s.claims(fd),os.fstat(fd).st_ino
 rows,reservation_inode=retry(read_claims,w)
 assert len(rows) in (3,4)
 if role=='ada':
  s.reserve('recovery',4000,4768,IDENT,{'TEST_ONLY':True})
  child=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'ada','--holder'])
  try:
   held=wait(ROOT/'ada-holder-ready.json');wait(ROOT/'boole-busy-confirmed.json')
  finally:
   child.kill();child.wait(timeout=10)
  journal=s.root/'jobs/recovery/journal.jsonl'
  with s.locked(journal) as fd:
   assert os.fstat(fd).st_ino==held['journal_inode']
   s.append(fd,b'{"TEST_ONLY_partial_tail":','journal')
  s.checkpoint('recovery',wait(ROOT/'initial-checkpoint.json'))
  emit('ada-recovery-ready.json',held)
  peer=wait(ROOT/'boole-recovery-complete.json')
  state=s.run('recovery',IDENT,lambda x,y:(_ for _ in ()).throw(AssertionError('Completed journal reevaluated')))
  assert state['complete'] and state['chunks']==3 and state['next_patch']==4768
  assert state==peer['state']
 else:
  held=wait(ROOT/'ada-holder-ready.json')
  try:s.run('recovery',IDENT,evaluate)
  except w.Busy:pass
  else:raise AssertionError('Same job was not excluded')
  emit('boole-busy-confirmed.json',{'excluded':True})
  wait(ROOT/'ada-recovery-ready.json');calls=[]
  def ev(x,y):calls.append([x,y]);return evaluate(x,y)
  state=s.run('recovery',IDENT,ev)
  assert calls==[[4256,4512],[4512,4768]],calls
  journal=s.root/'jobs/recovery/journal.jsonl'
  assert journal.stat().st_ino==held['journal_inode']
  tails=list(journal.parent.glob('uncommitted-tail.*.bin'))
  assert len(tails)==1 and tails[0].read_bytes()==b'{"TEST_ONLY_partial_tail":'
  records=[json.loads(x) for x in journal.read_text().splitlines()]
  assert [[x['first'],x['last']] for x in records]==[[4000,4256],[4256,4512],[4512,4768]]
  emit('boole-recovery-complete.json',{'state':state,'evaluated_synthetic_ranges':calls})
 assert (s.root/'reservations.jsonl').stat().st_ino==reservation_inode
 result={'status':'PASS','host':socket.gethostname(),'role':role,'TEST_ONLY':True,'mathematical_coverage':False,'exact_store_source_sha256':hashlib.sha256((HERE/'range_worker.py').read_bytes()).hexdigest(),'limitations':'Exact Store methods with separate in-memory Ada-export verifier and synthetic evaluation; not production runtime or NAS validation.','reservation_inode':reservation_inode,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 emit(role+'-result.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as e:
  if role and ROOT.exists():emit(role+'-failure-'+str(os.getpid())+'.json',{'error':repr(e),'TEST_ONLY':True})
  raise
