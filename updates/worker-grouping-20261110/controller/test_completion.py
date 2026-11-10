"""Pure completion-gate tests; never import host service implementations."""
import copy
import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import patch

HERE=pathlib.Path(__file__).resolve().parent
# The deployed controller imports host-specific modules. Stubs forbid side effects.
release=types.ModuleType('release');release.sha=lambda _: 'config-hash'
units=types.ModuleType('units')
def forbidden(*a,**kw):raise AssertionError('Unexpected service operation')
units.call=units.start=forbidden
mirror=types.ModuleType('durable_mirror');mirror.atomic=forbidden
with patch.dict(sys.modules,release=release,units=units,durable_mirror=mirror):
 spec=importlib.util.spec_from_file_location('controller_under_test',HERE/'controller.py')
 controller=importlib.util.module_from_spec(spec);spec.loader.exec_module(controller)

class CompletionTests(unittest.TestCase):
 def setUp(self):
  controller.STOP=False
  self.status={'status':'stopped','error':None,'reason':'Local journal byte cap reached'}
  self.sup={'status':'finished','error':None,'config_sha256':'config-hash','worker_exit_code':0,'leases_released':True,'all_owned_processes_exited_utc':'2026-11-10T18:00:00Z'}
 def state(self):return controller.completion_state(self.status,self.sup,'config-hash')
 def test_exact_clean_completion(self):self.assertEqual(self.state(),'complete')
 def test_missing_exit_code_is_pending_not_success_or_keyerror(self):
  del self.sup['worker_exit_code'];self.assertEqual(self.state(),'pending')
 def test_null_exit_code_is_pending(self):
  self.sup['worker_exit_code']=None;self.assertEqual(self.state(),'pending')
 def test_every_final_field_is_required(self):
  for key in ['status','error','worker_exit_code','leases_released','all_owned_processes_exited_utc']:
   sup=dict(self.sup);del sup[key]
   self.assertEqual(controller.completion_state(self.status,sup,'config-hash'),'pending',key)
 def test_failure_is_not_restartable(self):
  for code in [1,-15,'0',False]:
   self.sup['worker_exit_code']=code
   with self.assertRaises(RuntimeError):self.state()
 def test_worker_error_rejected(self):
  self.status['error']='bad';
  with self.assertRaises(RuntimeError):self.state()
 def test_supervisor_error_rejected(self):
  self.sup['error']='bad'
  with self.assertRaises(RuntimeError):self.state()
 def test_failed_phase_rejected_even_with_zero(self):
  self.sup['status']='failed'
  with self.assertRaises(RuntimeError):self.state()
 def test_stale_or_unknown_config_rejected(self):
  for value in [None,'other']:
   self.sup['config_sha256']=value
   with self.assertRaises(RuntimeError):self.state()
 def test_only_boolean_lease_evidence(self):
  for value in [False,None,1,'true']:
   self.sup['leases_released']=value;self.assertEqual(self.state(),'pending')
 def test_cleanup_timestamp_required(self):
  self.sup['all_owned_processes_exited_utc']='';self.assertEqual(self.state(),'pending')
 def test_running_report_pending(self):
  self.sup['status']='running';self.assertEqual(self.state(),'pending')
 def test_terminal_worker_required(self):
  self.status['status']='running';self.assertEqual(self.state(),'pending')
 def test_waits_for_atomic_final_report(self):
  incomplete=dict(self.sup);del incomplete['worker_exit_code']
  cp={'next_patch':123}
  with patch.object(controller,'load',side_effect=[self.status,incomplete,self.status,self.sup,cp]),patch.object(controller.time,'time',return_value=0),patch.object(controller.time,'monotonic',side_effect=[0,1,2]),patch.object(controller.time,'sleep') as sleep:
   self.assertEqual(controller.await_completion({'output':'/unused/run'},'/config'),(self.status,cp,self.sup));sleep.assert_called_once_with(2)
 def test_timeout_does_not_infer_success(self):
  incomplete=dict(self.sup);del incomplete['worker_exit_code']
  with patch.object(controller,'load',side_effect=[self.status,incomplete]),patch.object(controller.time,'time',return_value=0),patch.object(controller.time,'monotonic',side_effect=[0,121]):
   with self.assertRaises(TimeoutError):controller.await_completion({'output':'/unused/run'},'/config')
 def test_deadline_stops_wait_without_restart(self):
  with patch.object(controller.time,'time',return_value=controller.DEADLINE),patch.object(controller,'load') as load:
   self.assertIsNone(controller.await_completion({'output':'/unused/run'},'/config'));load.assert_not_called()
 def test_stop_stops_wait_without_restart(self):
  controller.STOP=True
  with patch.object(controller,'load') as load:
   self.assertIsNone(controller.await_completion({'output':'/unused/run'},'/config'));load.assert_not_called()
 def test_missing_files_then_terminal_report(self):
  cp={}
  with patch.object(controller,'load',side_effect=[FileNotFoundError(),self.status,self.sup,cp]),patch.object(controller.time,'time',return_value=0),patch.object(controller.time,'monotonic',side_effect=[0,1]),patch.object(controller.time,'sleep'):
   self.assertEqual(controller.await_completion({'output':'/unused/run'},'/config'),(self.status,cp,self.sup))
 def test_explicit_failure_no_polling(self):
  self.sup['worker_exit_code']=1
  with patch.object(controller,'load',side_effect=[self.status,self.sup]),patch.object(controller.time,'time',return_value=0),patch.object(controller.time,'sleep') as sleep:
   with self.assertRaises(RuntimeError):controller.await_completion({'output':'/unused/run'},'/config')
   sleep.assert_not_called()
 def test_signaled_supervisor_does_not_rollover_at_endpoint(self):
  cp={'next_patch':20,'window':{'last':20}}
  for trigger in ['signal','absolute_deadline']:
   self.assertEqual(controller.next_action(cp,self.status,0,{'stop_trigger':trigger}),'stop')
 def test_next_action_still_preserves_manual_stop(self):
  cp={'next_patch':10,'window':{'last':20}}
  for reason in ['Stop requested','Running CPU load budget exceeded','Storage free reserve reached']:
   self.assertEqual(controller.next_action(cp,{'reason':reason,'error':None},0),'stop')
  self.assertEqual(controller.next_action(cp,self.status,0),'rotate')

if __name__=='__main__':unittest.main(verbosity=2)
