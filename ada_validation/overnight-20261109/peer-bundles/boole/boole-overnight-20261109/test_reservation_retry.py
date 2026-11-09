"""Exercise transient contention, timeout, and integrity rejection on isolated NFS ledgers."""
import hashlib,json,subprocess,sys,time,unittest,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'worker'),str(ROOT/'worker/source/lattice_gpu')]
import ada_export_store as store_module
import policy

class ReservationRetryTests(unittest.TestCase):
 def setUp(self):
  self.cfg=json.loads(Path('/home/pnord/boole-buffered-20261109/worker/production-config.json').read_bytes())
  self.store=store_module.Store(policy.TEST_LEDGER/('lock-'+uuid.uuid4().hex))
  self.claim=self.store.reserve('test',self.cfg['initial_patch'],self.cfg['range_end'],self.cfg['manifest_sha256'])
  self.cfg.update(TEST_ONLY=True,ledger_root=str(self.store.root),ledger_job='test',ledger_device=self.store.device,ledger_claim_sha256=self.claim['sha256'])
 def holder(self,duration):
  code="import fcntl,sys,time; f=open(sys.argv[1],'r+'); fcntl.lockf(f,fcntl.LOCK_EX); print('locked',flush=True); time.sleep(float(sys.argv[2]))"
  process=subprocess.Popen([sys.executable,'-B','-u','-c',code,str(self.store.root/'reservations.jsonl'),str(duration)],stdout=subprocess.PIPE,text=True)
  self.addCleanup(process.wait)
  self.assertEqual(process.stdout.readline().strip(),'locked')
  self.addCleanup(process.stdout.close)
  return process
 def test_brief_contention_retries(self):
  self.holder(.4);start=time.monotonic()
  _,claim=policy.validate_ledger(self.cfg)
  self.assertEqual(claim,self.claim)
  self.assertGreaterEqual(time.monotonic()-start,.30)
  self.assertLess(time.monotonic()-start,2)
 def test_sustained_contention_fails_closed(self):
  self.holder(2.5);start=time.monotonic()
  with self.assertRaises(store_module.Busy):policy.validate_ledger(self.cfg)
  self.assertGreaterEqual(time.monotonic()-start,1.9)
  self.assertLess(time.monotonic()-start,2.4)
 def test_validly_signed_overlap_rejected(self):
  row=dict(self.claim,job='other')
  row['sha256']=store_module.digest({k:v for k,v in row.items() if k!='sha256'})
  with self.store.locked(self.store.root/'reservations.jsonl') as fd:
   self.store.append(fd,store_module.canonical(row)+b'\n','test-overlap')
  with self.assertRaisesRegex(RuntimeError,'overlaps another owner'):policy.validate_ledger(self.cfg)
 def test_bad_digest_rejected(self):
  with self.store.locked(self.store.root/'reservations.jsonl') as fd:
   self.store.append(fd,b'{"sha256":"bad"}\n','test-invalid')
  with self.assertRaisesRegex(store_module.Integrity,'digest/grid'):policy.validate_ledger(self.cfg)
if __name__=='__main__':unittest.main(verbosity=2)
