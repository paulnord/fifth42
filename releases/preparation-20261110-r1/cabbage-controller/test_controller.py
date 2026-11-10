import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,Mock
import controller
import install_controller
import stop_controller
class ControlTests(unittest.TestCase):
 def test_allocations_stay_in_unreserved_cells(self):
  claims=[dict(first=500000000,last=11250000001)]
  self.assertEqual(controller.available_interval(claims),(1,500000000))
  self.assertIsNone(controller.available_interval([dict(first=1,last=11250000001)]))
  self.assertEqual(controller.available_interval([dict(first=100,last=11250000001)]),(1,100))
 def test_only_expected_clean_stops_roll_over(self):
  cp=dict(next_patch=10,window=dict(last=20))
  self.assertEqual(controller.next_action(cp,dict(reason='Local journal byte cap reached',error=None),0),'rotate')
  for reason in ['Stop requested','Running CPU load budget exceeded','Storage free reserve reached']:
   self.assertEqual(controller.next_action(cp,dict(reason=reason,error=None),0),'stop')
  self.assertEqual(controller.next_action(cp,dict(reason='Local journal byte cap reached',error='bad'),0),'stop')
  cp['next_patch']=20
  self.assertEqual(controller.next_action(cp,dict(reason='Selected remaining shell endpoint reached',error=None),0),'next_reservation')
  self.assertEqual(controller.next_action(cp,dict(reason=None,error=None),controller.DEADLINE-10),'stop')
  self.assertEqual(controller.next_action(cp,dict(reason='Stop requested',error=None),0),'stop')
  self.assertEqual(controller.next_action(cp,dict(reason='Selected remaining shell endpoint reached',error=None),0,stop_intent=True),'stop')

class ShutdownTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.run=self.root/'local'/'run';self.rep=self.root/'replica';self.run.mkdir(parents=True);self.rep.mkdir()
  self.path=self.root/'production-config.json'
  self.c=dict(output=str(self.run),replica_output=str(self.rep),service_name='worker.service',run_id='test',manifest_sha256='2'*64,initial_patch=10,range_end=20,ledger_claim_sha256='3'*64,deadline_service_name='deadline.service')
  self.save(self.path,self.c)
  identity=dict(trial='test',source_identity=hashlib.sha256(json.dumps(dict(manifest_sha256=self.c['manifest_sha256'],config=self.c),sort_keys=True,separators=(',',':')).encode()).hexdigest())
  self.cp=dict(next_patch=15,window=dict(last=20),chunks=1,journal_offset=3,journal_sha256='1'*64,identity=identity)
  self.status=dict(status='stopped',reason='Local journal byte cap reached',error=None,journal_buffer=dict(pending_chunks=0,pending_bytes=0),**{k:self.cp[k] for k in ('chunks','journal_offset','next_patch','journal_sha256')})
  self.sup=dict(status='finished',error=None,worker_exit_code=0,leases_released=True,config_sha256=controller.release.sha(self.path))
  self.save(self.run.parent/'supervisor.json',self.sup);self.save(self.run/'status.json',self.status);self.save(self.run/'checkpoint.json',self.cp)
  (self.rep/'checkpoint.json').write_bytes((self.run/'checkpoint.json').read_bytes())
  receipt=dict(status='verified',checkpoint_sha256=controller.release.sha(self.run/'checkpoint.json'),next_patch=15,chunks=1,committed_bytes=3,journal_sha256='1'*64,raw_sha256=hashlib.sha256(b'abc').hexdigest(),identity=identity)
  self.final=dict(status='verified',compute_started=False,receipt=receipt)
  self.save(self.run/'final-replica.json',self.final);self.save(self.rep/'replica-state.json',receipt)
  for root in (self.run,self.rep):(root/'coverage.jsonl').write_bytes(b'abc')
  self.clock=0;self.on_sleep=None
  self.unit=dict(ActiveState='inactive',SubState='dead',MainPID='0',Result='success',ExecMainStatus='0')
  self.unit_mock=Mock(return_value=self.unit);self.call_mock=Mock()
  for target,value in [('ROOT',self.root),('STOP',False)]:
   p=patch.object(controller,target,value);p.start();self.addCleanup(p.stop)
  for target,value in [('state',self.unit_mock),('call',self.call_mock)]:
   p=patch.object(controller.units,target,value);p.start();self.addCleanup(p.stop)
  for target,value in [('time',lambda:0),('monotonic',lambda:self.clock),('sleep',self.sleep)]:
   p=patch.object(controller.time,target,value);p.start();self.addCleanup(p.stop)
 def save(self,path,value):path.write_text(json.dumps(value,sort_keys=True)+'\n')
 def sleep(self,seconds):
  self.clock+=seconds
  if self.on_sleep:self.on_sleep()
 def check(self,timeout=10):return controller.wait_for_completion(self.c,self.path,timeout)
 def test_waits_through_deactivating_and_inactive_with_live_mainpid(self):
  self.save(self.run.parent/'supervisor.json',dict(status='running',error=None,leases_released=False))
  self.unit_mock.side_effect=[dict(self.unit,ActiveState='deactivating',MainPID='123'),dict(self.unit,MainPID='123'),self.unit,self.unit]
  self.on_sleep=lambda:self.save(self.run.parent/'supervisor.json',self.sup) if self.clock>=4 else None
  self.assertEqual(self.check()[1],self.cp);self.assertEqual(self.clock,4)
 def test_waits_for_final_report_even_after_unit_exits(self):
  self.save(self.run.parent/'supervisor.json',dict(status='running',error=None,leases_released=False))
  self.on_sleep=lambda:self.save(self.run.parent/'supervisor.json',self.sup)
  self.assertEqual(self.check()[2],self.sup);self.assertEqual(self.clock,2)
 def test_missing_or_never_final_report_times_out(self):
  for incomplete in [None,dict(status='running',error=None,leases_released=False)]:
   with self.subTest(report=incomplete):
    self.clock=0
    if incomplete is None:(self.run.parent/'supervisor.json').unlink()
    else:self.save(self.run.parent/'supervisor.json',incomplete)
    with self.assertRaisesRegex(TimeoutError,'no automatic restart'):self.check(timeout=1)
 def test_failed_or_incomplete_final_supervisor_fails_closed(self):
  for changes in [dict(status='failed'),dict(error='bad'),dict(worker_exit_code=1),dict(worker_exit_code=False),dict(leases_released=False),dict(config_sha256='f'*64)]:
   with self.subTest(changes=changes):
    self.save(self.run.parent/'supervisor.json',dict(self.sup,**changes))
    with self.assertRaises(RuntimeError):self.check()
  missing=dict(self.sup);del missing['worker_exit_code'];self.save(self.run.parent/'supervisor.json',missing)
  with self.assertRaisesRegex(RuntimeError,'final supervisor report'):self.check()
 def test_failed_service_is_not_accepted(self):
  self.unit_mock.return_value=dict(self.unit,ActiveState='failed')
  with self.assertRaisesRegex(RuntimeError,'service failed'):self.check()
  self.unit_mock.return_value=dict(self.unit,ExecMainStatus='9')
  with self.assertRaisesRegex(RuntimeError,'exit successfully'):self.check()
 def test_nonempty_or_failed_worker_status_is_rejected(self):
  for changes in [dict(error='bad'),dict(status='running'),dict(journal_buffer=dict(pending_chunks=1,pending_bytes=1)),dict(journal_buffer=dict(pending_chunks=False,pending_bytes=False)),dict(next_patch=16)]:
   with self.subTest(changes=changes):
    self.save(self.run/'status.json',dict(self.status,**changes))
    with self.assertRaises(RuntimeError):self.check()
 def test_stale_or_unverified_replica_is_rejected(self):
  for changes in [dict(status='failed'),dict(compute_started=True),dict(receipt=dict(self.final['receipt'],checkpoint_sha256='f'*64)),dict(receipt=dict(self.final['receipt'],next_patch=14)),dict(receipt=dict(self.final['receipt'],raw_sha256=None))]:
   with self.subTest(changes=changes):
    self.save(self.run/'final-replica.json',dict(self.final,**changes))
    with self.assertRaises(RuntimeError):self.check()
  self.save(self.run/'final-replica.json',self.final);(self.rep/'checkpoint.json').write_bytes(b'{}')
  with self.assertRaisesRegex(RuntimeError,'Replica checkpoint differs'):self.check()
 def test_missing_final_copy_times_out_and_does_not_restart(self):
  (self.run/'final-replica.json').unlink()
  with self.assertRaisesRegex(TimeoutError,'verified replica files'):self.check(timeout=1)
  self.call_mock.assert_not_called()
 def test_committed_journal_and_published_receipt_must_match(self):
  (self.rep/'coverage.jsonl').write_bytes(b'abcd')
  with self.assertRaisesRegex(RuntimeError,'journal size'):self.check()
  (self.rep/'coverage.jsonl').write_bytes(b'abc');self.save(self.rep/'replica-state.json',{})
  with self.assertRaisesRegex(RuntimeError,'published replica state'):self.check()
 def test_typed_checkpoint_cursor_and_digest_are_required(self):
  for changes in [dict(next_patch=True),dict(next_patch=21),dict(journal_sha256='x')]:
   with self.subTest(changes=changes):
    cp=dict(self.cp,**changes);self.save(self.run/'checkpoint.json',cp)
    with self.assertRaises(RuntimeError):self.check()
 def test_stop_intent_arriving_during_wait_requests_stop(self):
  self.unit_mock.side_effect=[dict(self.unit,ActiveState='deactivating',MainPID='123'),self.unit,self.unit]
  self.on_sleep=lambda:self.save(self.root/'stop-request.json',dict(reason='stop'))
  self.check();self.call_mock.assert_called_once_with('stop','worker.service')
 def test_main_never_rolls_over_after_stop_intent(self):
  cp=dict(self.cp,next_patch=20)
  def completed(*args):self.save(self.root/'stop-request.json',{});return self.status,cp,self.sup,self.final
  with patch.object(controller,'start',return_value=self.c) as start,patch.object(controller,'verify_controller'),patch.object(controller.signal,'signal'),patch.object(controller,'wait_for_completion',side_effect=completed),patch.object(controller,'state') as state,patch.object(controller,'allocate_more') as allocate,patch.object(controller.subprocess,'run') as run:
   self.assertEqual(controller.main(),0);self.assertEqual(start.call_count,1);allocate.assert_not_called();run.assert_not_called();self.assertEqual(state.call_args.args[0],'stopped')
 def test_consumed_pending_reservation_cannot_be_reused(self):
  self.save(self.root/'controller-settings.json',dict(pending_consumed=True));cp=dict(self.cp,next_patch=20)
  def seal(*args,**kwargs):
   evidence=self.root/'rotation-evidence'/'test';self.save(evidence/'parent-seal.json',dict(sealed=True))
  with patch.object(controller,'start',return_value=self.c) as start,patch.object(controller,'verify_controller'),patch.object(controller.signal,'signal'),patch.object(controller,'wait_for_completion',return_value=(self.status,cp,self.sup,self.final)),patch.object(controller,'state') as state,patch.object(controller,'allocate_more',return_value=None) as allocate,patch.object(controller.subprocess,'run',side_effect=seal):
   self.assertEqual(controller.main(),0);allocate.assert_called_once();self.assertEqual(start.call_count,1);self.assertEqual(state.call_args.args[0],'completed_available_work')
 def test_start_rechecks_stop_intent_after_binding(self):
  def bind(path):self.save(self.root/'stop-request.json',{});return dict(self.c,output=str(self.root/'unused'),replica_output=str(self.root/'unused-replica'))
  with patch.object(controller,'bind',side_effect=bind),patch.object(controller.units,'start') as start:
   with self.assertRaises(controller.StopRequested):controller.start(self.path)
   start.assert_not_called()
 def test_stop_interface_persists_intent_before_systemctl_and_verifies_copy(self):
  self.save(self.root/'active-configuration.json',dict(config=str(self.path),config_sha256=controller.release.sha(self.path)))
  def call(*args,**kwargs):self.assertTrue((self.root/'stop-request.json').exists())
  with patch.object(stop_controller,'R',self.root),patch.object(stop_controller.subprocess,'run',side_effect=call) as calls,patch.object(controller,'wait_for_completion') as finish:
   self.assertEqual(stop_controller.main(),0);self.assertEqual(calls.call_count,2);finish.assert_called_once()

class InstallerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);(self.root/'evidence').mkdir();(self.root/'worker').mkdir()
  source=Path(__file__).resolve().parent
  for name in ['controller.py','test_controller.py','stop_controller.py','install_controller.py']:(self.root/name).write_bytes((source/name).read_bytes())
  for name in ['release.py','units.py','seal_previous.py','parallel_audit.py','collector.py','production-config.json','worker/base-config.json','worker/task.py']:(self.root/name).write_text('{}')
  self.save('worker/release-manifest.json',dict(files={'task.py':install_controller.sha(self.root/'worker/task.py')}))
  self.save('evidence/runtime-validation.json',dict(status='passed'))
  self.save('evidence/controller-validation.json',dict(status='passed',files={name:install_controller.sha(self.root/name) for name in ['controller.py','test_controller.py','stop_controller.py','install_controller.py']}))
  self.save('controller-settings.json',dict(pending_consumed=True))
  self.calls=Mock();self.unit=Mock(return_value=dict(ActiveState='inactive',MainPID='0'))
  for target,value in [('R',self.root),('UNIT_DIR',self.root/'user-units'),('PUBLISH_DIR',self.root/'share')]:
   p=patch.object(install_controller,target,value);p.start();self.addCleanup(p.stop)
  for target,value in [('run',self.calls)]:
   p=patch.object(install_controller.subprocess,target,value);p.start();self.addCleanup(p.stop)
  p=patch.object(install_controller.worker_units,'state',self.unit);p.start();self.addCleanup(p.stop)
  p=patch.object(install_controller.time,'time',return_value=0);p.start();self.addCleanup(p.stop)
 def save(self,name,value):(self.root/name).write_text(json.dumps(value)+'\n')
 def test_default_only_stages_and_does_not_install_or_start_services(self):
  self.assertEqual(install_controller.main(),0);self.calls.assert_not_called();self.unit.assert_not_called()
  self.assertTrue((self.root/'staged-systemd'/install_controller.CONTROLLER).exists());self.assertFalse((self.root/'user-units').exists());self.assertFalse((self.root/'share').exists())
  self.assertIn('TimeoutStopSec=960',(self.root/'staged-systemd'/install_controller.CONTROLLER).read_text())
  self.assertIn('OnCalendar=2026-11-11 22:59:50 UTC',(self.root/'staged-systemd'/'cabbage-extended-controller-20261109-deadline.timer').read_text())
  self.assertEqual(controller.DEADLINE,1794438000);self.assertEqual(install_controller.DEADLINE,controller.DEADLINE)
 def test_stage_then_explicit_start_is_supported(self):
  install_controller.main();self.assertEqual(install_controller.main(start_services=True),0)
  self.assertEqual(self.calls.call_args.args[0][-1],install_controller.CONTROLLER)
 def test_changed_source_after_testing_prevents_staging(self):
  (self.root/'controller.py').write_text('changed')
  with self.assertRaisesRegex(AssertionError,'changed since regression'):install_controller.main()
  self.calls.assert_not_called()
 def test_stop_intent_requires_explicit_authorized_clear(self):
  self.save('stop-request.json',dict(reason='old'))
  with self.assertRaisesRegex(AssertionError,'clear-stop-intent'):install_controller.main(start_services=True)
  self.calls.assert_not_called();self.assertTrue((self.root/'stop-request.json').exists())
 def test_active_controller_prevents_installation(self):
  self.unit.return_value=dict(ActiveState='deactivating',MainPID='123')
  with self.assertRaisesRegex(AssertionError,'inactive with MainPID'):install_controller.main(start_services=True)
  self.calls.assert_not_called()
 def test_new_stop_intent_is_not_erased_during_install(self):
  self.save('stop-request.json',dict(reason='old'))
  def command(*args,**kwargs):self.save('stop-request.json',dict(reason='new'))
  self.calls.side_effect=command
  with self.assertRaisesRegex(AssertionError,'new stop request'):install_controller.main(start_services=True,clear_stop_intent=True)
  self.assertEqual(json.loads((self.root/'stop-request.json').read_bytes())['reason'],'new');self.assertEqual(self.calls.call_count,2)
 def test_new_stop_intent_when_none_existed_prevents_start(self):
  self.calls.side_effect=lambda *args,**kwargs:self.save('stop-request.json',dict(reason='new'))
  with self.assertRaisesRegex(AssertionError,'stop request arrived'):install_controller.main(start_services=True)
  self.assertTrue((self.root/'stop-request.json').exists());self.assertEqual(self.calls.call_count,2)
 def test_explicit_old_child_timers_are_retired_only_at_start(self):
  self.save('controller-settings.json',dict(pending_consumed=True,retire_timers=['fifth-old-run-deadline.timer']))
  install_controller.main();self.calls.assert_not_called()
  install_controller.main(start_services=True)
  self.assertIn(['systemctl','--user','stop','fifth-old-run-deadline.timer'],[call.args[0] for call in self.calls.call_args_list])
if __name__=='__main__':unittest.main(verbosity=2)
