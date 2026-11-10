"""Lifecycle decisions fail closed and cannot race deactivation or manual stop."""
import copy,unittest
from rotation_controller import decision
class RotationTests(unittest.TestCase):
 def setUp(self):
  self.service=dict(ActiveState='inactive',MainPID='0');self.sup=dict(worker_exit_code=0,leases_released=True,error=None)
  self.status=dict(status='stopped',error=None,reason='Bulk journal byte budget reached',journal_buffer=dict(pending_chunks=0,pending_bytes=0));self.cp=dict(next_patch=500);self.config=dict(range_end=1000,stop_epoch=2000)
 def choose(self,**kw):
  d=dict(service=self.service,supervisor=self.sup,status=self.status,checkpoint=self.cp,config=self.config,stopping=False,now=1000);d.update(kw);return decision(**d)
 def test_only_clean_cap_stop_rotates(self):self.assertEqual(self.choose(),'rotate')
 def test_deactivating_report_is_never_read(self):self.assertEqual(self.choose(service=dict(ActiveState='deactivating',MainPID='12'),supervisor=None,status=None,checkpoint=None),'wait')
 def test_nonzero_main_pid_is_not_quiescent(self):self.assertEqual(self.choose(service=dict(ActiveState='inactive',MainPID='12')),'wait')
 def test_manual_stop_prevents_rollover(self):self.assertEqual(self.choose(stopping=True,supervisor=None,status=None,checkpoint=None),'stop')
 def test_bad_or_missing_supervisor_fails_closed(self):
  for s in (None,dict(self.sup,worker_exit_code=1),dict(self.sup,leases_released=False),dict(self.sup,error='failure')):
   with self.subTest(s=s),self.assertRaises(RuntimeError):self.choose(supervisor=s)
 def test_failed_service_cannot_restart(self):
  with self.assertRaises(RuntimeError):self.choose(service=dict(ActiveState='failed',MainPID='0'))
 def test_pending_commit_or_replica_lag_cannot_restart(self):
  for s in (dict(self.status,journal_buffer=dict(pending_chunks=1,pending_bytes=0)),dict(self.status,reason='Verified replica has fallen behind its time budget')):
   with self.subTest(s=s),self.assertRaises(RuntimeError):self.choose(status=s)
 def test_endpoint_and_deadline_finish(self):
  self.assertEqual(self.choose(checkpoint=dict(next_patch=1000)),'complete');self.assertEqual(self.choose(now=1990),'complete')
if __name__=='__main__':unittest.main(verbosity=2)
