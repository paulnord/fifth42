import errno,json,os,signal,subprocess,sys,time,unittest,uuid
from pathlib import Path
from unittest.mock import patch
import range_worker as w
B=Path(__file__).resolve().parent
TEST=Path('/mnt/diskBox/pnord/fifth42/tests-20261107')
IDENT=(B/'runtime-identity.txt').read_text().strip()
FIRST=3750000000

def evaluate(first,last):
    request=dict(first=first,last=last,grid=w.GRID,identity=IDENT)
    result=subprocess.check_output([sys.executable,str(B/'chunk_evaluator.py'),'--manifest',str(B/'runtime-manifest.json')],input=json.dumps(request),text=True,timeout=60)
    return json.loads(result)

class WorkerTests(unittest.TestCase):
 def setUp(self):
    self.root=TEST/(self._testMethodName+'-'+uuid.uuid4().hex[:8]);self.s=w.Store(self.root)
 def claim(self,n=256):return self.s.reserve('job',FIRST,FIRST+n,IDENT)
 def checkpoint(self):return json.loads((self.root/'jobs/job/checkpoint.json').read_text())
 def test_large_adjacent_and_overlapping_claims(self):
    a=self.s.reserve('large-a',FIRST,FIRST+100000000,IDENT)
    self.assertEqual(a,self.s.reserve('large-a',FIRST,FIRST+100000000,IDENT))
    self.s.reserve('large-b',FIRST+100000000,FIRST+200000000,IDENT)
    for start,end in [(FIRST-1,FIRST+1),(FIRST+1,FIRST+2),(FIRST+99999999,FIRST+100000001)]:
      with self.assertRaises(w.Conflict):self.s.reserve('overlap',start,end,IDENT)
    for start,end in [(0,0),(-1,1),(0,w.GRID['count']+1)]:
      with self.assertRaises(ValueError):self.s.reserve('invalid',start,end,IDENT)
    with self.assertRaises(w.Conflict):self.s.reserve('large-a',FIRST,FIRST+1,IDENT)
 def test_concurrent_reservation(self):
    code='''import sys,time\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1]);import range_worker as w\ns=w.Store(sys.argv[2])\nfor i in range(100):\n try:s.reserve(sys.argv[3],3750000000,3750000256,sys.argv[4]);print('accepted');break\n except w.Busy:time.sleep(.01)\n except w.Conflict:print('conflict');break\nelse:raise RuntimeError('lock timeout')'''
    ps=[subprocess.Popen([sys.executable,'-c',code,str(B),str(self.root),name,IDENT],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for name in ['a','b']]
    outputs=[]
    for p in ps:
      out,err=p.communicate(timeout=20);self.assertEqual(p.returncode,0,err);outputs.append(out.strip())
    self.assertEqual(sorted(outputs),['accepted','conflict'])
 def driver(self,phase):
    marker=self.root/'barrier'
    code='''import sys,time,signal\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1]);import range_worker as w\nfrom test_range_worker import evaluate,IDENT\nroot=Path(sys.argv[2]);phase=sys.argv[3];stop=[False]\nsignal.signal(signal.SIGTERM,lambda a,b:stop.__setitem__(0,True))\ndef inject(event):\n if event==phase:\n  (root/'barrier').write_text(event)\n  if phase=='before_evaluate':time.sleep(1)\n  else:time.sleep(600)\ns=w.Store(root,inject);s.run('job',IDENT,evaluate,lambda:stop[0])'''
    p=subprocess.Popen([sys.executable,'-c',code,str(B),str(self.root),phase],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    end=time.monotonic()+30
    while not marker.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.02)
    self.assertTrue(marker.exists(),p.communicate(timeout=1) if p.poll() is not None else 'barrier timeout')
    return p
 def test_kill_restart_and_duplicate_worker(self):
    self.claim(512);p=self.driver('after_checkpoint')
    try:
      self.assertEqual(self.checkpoint()['next_patch'],FIRST+256)
      with self.assertRaises(w.Busy):self.s.run('job',IDENT,evaluate)
    finally:p.kill();p.communicate(timeout=10)
    state=self.s.run('job',IDENT,evaluate);self.assertTrue(state['complete']);self.assertEqual(state['chunks'],2)
    self.assertEqual(state['next_patch'],FIRST+512)
    records=[json.loads(x) for x in (self.root/'jobs/job/journal.jsonl').read_text().splitlines()]
    self.assertEqual([(r['first'],r['last']) for r in records],[(FIRST,FIRST+256),(FIRST+256,FIRST+512)])
    self.assertEqual(self.s.run('job',IDENT,lambda a,b:self.fail('completed chunk rerun')),state)
 def test_sigterm_finishes_chunk_then_resume(self):
    self.claim(512);p=self.driver('before_evaluate');p.send_signal(signal.SIGTERM);out,err=p.communicate(timeout=30);self.assertEqual(p.returncode,0,err)
    self.assertEqual(self.checkpoint()['chunks'],1);self.assertFalse(self.checkpoint()['complete'])
    self.assertTrue(self.s.run('job',IDENT,evaluate)['complete'])
 def test_partial_write_enospc_preserved_and_recomputed(self):
    self.claim();original=w.write_all;failed=[False]
    def diskfull(fd,data):
      target=os.readlink('/proc/self/fd/'+str(fd))
      if target.endswith('/journal.jsonl') and not failed[0]:
       failed[0]=True;original(fd,data[:31]);raise OSError(errno.ENOSPC,'injected partial journal write')
      original(fd,data)
    with patch.object(w,'write_all',diskfull):
      with self.assertRaises(OSError):self.s.run('job',IDENT,evaluate)
    self.assertEqual(self.checkpoint()['next_patch'],FIRST)
    state=self.s.run('job',IDENT,evaluate);self.assertTrue(state['complete']);self.assertEqual(state['chunks'],1)
    self.assertEqual(len(list((self.root/'jobs/job').glob('uncommitted-tail.*.bin'))),1)
 def test_checkpoint_io_failure_rolls_forward_durable_chunk(self):
    self.claim();calls=[0]
    def ioerror(event):
      if event=='fsync_checkpoint':
       calls[0]+=1
       if calls[0]==2:raise OSError(errno.EIO,'injected checkpoint fsync failure')
    self.s.inject=ioerror
    with self.assertRaises(OSError):self.s.run('job',IDENT,evaluate)
    self.assertEqual(self.checkpoint()['chunks'],0)
    self.s.inject=lambda event:None
    state=self.s.run('job',IDENT,lambda a,b:self.fail('durable completed chunk rerun'))
    self.assertTrue(state['complete']);self.assertEqual(state['chunks'],1)
 def test_changed_identity_and_journal_tampering_fail_closed(self):
    self.claim();state=self.s.run('job',IDENT,evaluate)
    with self.assertRaises(w.Integrity):self.s.run('job','0'*64,evaluate)
    journal=self.root/'jobs/job/journal.jsonl';data=journal.read_bytes();journal.write_bytes(data.replace(b'"complete":true',b'"complete":false'))
    with self.assertRaises(w.Integrity):self.s.run('job',IDENT,evaluate)
    self.assertEqual(self.checkpoint(),json.loads(w.canonical(state)))
 def test_missing_mount_no_local_fallback(self):
    missing=self.root/'must-not-exist'
    with patch.object(w,'verify_share',side_effect=w.Integrity('injected missing NFS mount')):
      with self.assertRaises(w.Integrity):w.Store(missing)
    self.assertFalse(missing.exists())
    local=Path('/tmp/fifth42-no-local-'+uuid.uuid4().hex)
    with self.assertRaises(w.Integrity):w.Store(local)
    self.assertFalse(local.exists())
 def test_partial_reservation_log_rejects_new_claims(self):
    self.claim();p=self.root/'reservations.jsonl'
    with p.open('ab') as f:f.write(b'{"partial":');f.flush();os.fsync(f.fileno())
    with self.assertRaises(w.Integrity):self.s.reserve('next',FIRST+256,FIRST+512,IDENT)
 def test_incomplete_evaluator_cannot_advance(self):
    self.claim()
    with self.assertRaises(w.Integrity):self.s.run('job',IDENT,lambda first,last:dict(first=first,last=last,identity=IDENT,complete=False,hits=[]))
    self.assertEqual(self.checkpoint()['next_patch'],FIRST)
    self.assertEqual((self.root/'jobs/job/journal.jsonl').stat().st_size,0)
 def test_malformed_complete_result_cannot_commit(self):
    self.claim();good=evaluate(FIRST,FIRST+256)
    for key,value in [('points',good['points']+1),('certificate_sha256','bad'),('tasks',255)]:
      bad=dict(good,**{key:value})
      with self.assertRaises(w.Integrity):self.s.run('job',IDENT,lambda a,b:bad)
      self.assertEqual(self.checkpoint()['next_patch'],FIRST)
      self.assertEqual((self.root/'jobs/job/journal.jsonl').stat().st_size,0)
 def test_coverage_metadata_is_linked_without_old_journal_resume(self):
    coverage=dict(checkpoint_sha256='1'*64,journal_sha256='2'*64,verified_gaps=[[FIRST,FIRST+256]],fixture_only=True)
    claim=self.s.reserve('job',FIRST,FIRST+256,IDENT,coverage)
    self.assertEqual(claim['coverage'],coverage)
    state=self.s.run('job',IDENT,evaluate)
    self.assertEqual(state['claim_sha256'],claim['sha256']);self.assertEqual(state['chunks'],1)
 def test_cli_and_optimized_python_rejection(self):
    root=self.root/'cli';prefix=[sys.executable,str(B/'range_worker.py'),'--root',str(root)]
    subprocess.run(prefix+['reserve','--job','cli','--first',str(FIRST),'--last',str(FIRST+256),'--identity',IDENT],check=True,capture_output=True,text=True,timeout=20)
    p=subprocess.run(prefix+['run','--job','cli','--identity',IDENT,'--max-chunks','1','--',sys.executable,str(B/'chunk_evaluator.py'),'--manifest',str(B/'runtime-manifest.json')],check=True,capture_output=True,text=True,timeout=30)
    self.assertTrue(json.loads(p.stdout)['complete'])
    missing=self.root/'forbidden-optimized'
    p=subprocess.run([sys.executable,'-O',str(B/'range_worker.py'),'--root',str(missing),'reserve','--job','bad','--first','0','--last','1','--identity',IDENT],capture_output=True,text=True,timeout=20)
    self.assertNotEqual(p.returncode,0);self.assertIn('Ordinary Python required',p.stderr);self.assertFalse(missing.exists())
if __name__=='__main__':unittest.main(verbosity=2)
