"""Real POSIX-lock contention and corruption checks in an isolated test ledger."""
import multiprocessing as mp,sys,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'worker'),str(ROOT/'worker/source/lattice_gpu')]
import ada_export_store as store_module
import policy

def hold_lock(path,ready,seconds):
    import fcntl
    with open(path,'r+b') as stream:
        fcntl.lockf(stream,fcntl.LOCK_EX);ready.set();time.sleep(seconds)

class ClaimRetryTests(unittest.TestCase):
    def setUp(self):
        self.store=store_module.Store(policy.TEST_LEDGER/'claim-retry'/str(time.time_ns()))
        self.claim=self.store.reserve('retry-test',4564955776,4564956032,'d'*64,dict(TEST_ONLY=True))
    def holder(self,seconds):
        context=mp.get_context('spawn');ready=context.Event()
        child=context.Process(target=hold_lock,args=(str(self.store.root/'reservations.jsonl'),ready,seconds));child.start()
        self.addCleanup(lambda:child.join(2))
        self.assertTrue(ready.wait(5));return child
    def test_transient_real_lock_is_retried(self):
        self.holder(.2);self.assertEqual(policy.claim_with_retry(self.store,'retry-test',timeout=1),self.claim)
    def test_persistent_lock_has_a_finite_timeout(self):
        self.holder(.5);start=time.monotonic()
        with self.assertRaises(store_module.Busy):policy.claim_with_retry(self.store,'retry-test',timeout=.1)
        self.assertLess(time.monotonic()-start,.4)
    def test_bad_digest_is_not_retried_or_accepted(self):
        import os,json
        with self.store.locked(self.store.root/'reservations.jsonl') as fd:
            row=dict(self.claim,sha256='0'*64);raw=store_module.canonical(row)+b'\n'
            os.ftruncate(fd,0);os.write(fd,raw);os.fsync(fd)
        with self.assertRaises(store_module.Integrity):policy.claim_with_retry(self.store,'retry-test',timeout=.1)
    def test_unknown_job_remains_an_integrity_failure(self):
        with self.assertRaises(store_module.Integrity):policy.claim_with_retry(self.store,'missing-job',timeout=.1)

if __name__=='__main__':unittest.main(verbosity=2)
