import copy,json,sys,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'worker'));import policy as p
class ContinuationPolicyTests(unittest.TestCase):
 def fixture(self):
  c=dict(initial_patch=p.FIRST+512,range_end=p.LAST,parent_selected_patches=512,parent_journal_sha256='a'*64,parent_journal_offset=1234,parent_journal_raw_sha256='b'*64,parent_checkpoint_sha256='c'*64,reservation_manifest_sha256=p.ORIGINAL_MANIFEST,reservation_initial_patch=p.FIRST,ledger_claim_sha256=p.ORIGINAL_CLAIM,ledger_job=p.ORIGINAL_JOB)
  cp=dict(identity=dict(trial=p.ORIGINAL_JOB,source_identity=p.ORIGINAL_SOURCE),completed_bound=None,next_patch=c['initial_patch'],patches=512,journal_sha256='a'*64,journal_offset=1234)
  status=dict(status='stopped',error=None,next_patch=c['initial_patch'])
  audit=dict(status='verified_final_prefix',source_closed=True,run_id=p.ORIGINAL_JOB,manifest_sha256=p.ORIGINAL_MANIFEST,config_sha256=p.ORIGINAL_CONFIG,source_identity=p.ORIGINAL_SOURCE,next_patch=c['initial_patch'],journal_sha256='a'*64,journal_offset=1234,raw_sha256='b'*64,checkpoint_sha256='c'*64)
  receipt=dict(status='verified',source_closed=True,source_retained=True,captured_next_patch=c['initial_patch'],journal_chain_sha256='a'*64,committed_bytes=1234,raw_sha256='b'*64,captured_checkpoint_sha256='c'*64)
  supervisor=dict(leases_released=True,worker_exit_code=0,error=None,config_sha256=p.ORIGINAL_CONFIG)
  return [c,cp,status,audit,receipt,supervisor]
 def test_exact_parent_links_pass(self):p.validate_links(*self.fixture())
 def test_gaps_overlaps_and_claim_changes_reject(self):
  for key,value in [('initial_patch',p.FIRST+511),('initial_patch',p.FIRST+513),('range_end',p.LAST+1),('reservation_manifest_sha256','0'*64),('ledger_claim_sha256','0'*64),('parent_selected_patches',511),('ledger_job','other')]:
   with self.subTest(key=key,value=value):
    args=self.fixture();args[0][key]=value
    with self.assertRaises(RuntimeError):p.validate_links(*args)
 def test_active_unclosed_failed_and_changed_archive_reject(self):
  for index,key,value in [(2,'status','running'),(2,'error','failed'),(3,'source_closed',False),(4,'source_closed',False),(4,'raw_sha256','0'*64),(4,'committed_bytes',1235),(4,'captured_checkpoint_sha256','0'*64),(5,'leases_released',False),(5,'worker_exit_code',2)]:
   with self.subTest(index=index,key=key):
    args=self.fixture();args[index][key]=value
    with self.assertRaises(RuntimeError):p.validate_links(*args)
 def test_wrong_storage_paths_reject_before_creating_output(self):
  for path in ['/tmp/must-not-create-cabbage-continuation','/mnt/nfs_share/fifth42-shared-20261107/jobs/other/run','/mnt/fifth42-storage/runs/another-claim/new/run']:
   c=dict(output=path,TEST_ONLY=False,run_id='cabbage-bulk-test',output_device=-1)
   with self.assertRaises(RuntimeError):p.validate_output(c)
 def test_quiescent_timeout_recovery_requires_all_pinned_checks(self):
  args=self.fixture();c,cp,status,audit,receipt,sup=args
  status['status']='running';sup['leases_released']=False;sup.pop('worker_exit_code')
  c.update(parent_archive_receipt_sha256='d'*64,parent_quiescence_receipt_sha256='e'*64)
  q=dict(status='VERIFIED_QUIESCENT_AFTER_STOP_TIMEOUT',original_owner_lock_acquired=True,gpu_lease_acquired=True,gpu_compute_processes=[],unit_state='MainPID=0\nResult=timeout',checkpoint_sha256=c['parent_checkpoint_sha256'],journal_bytes=c['parent_journal_offset'])
  review=dict(status='verified_final_checkpoint_safe_for_fresh_continuation',original_stop='systemd_stop_timeout',parent_archive_receipt_sha256='d'*64,parent_checkpoint_sha256=c['parent_checkpoint_sha256'],parent_journal_raw_sha256=c['parent_journal_raw_sha256'],parent_journal_offset=c['parent_journal_offset'],parent_quiescence_receipt_sha256='e'*64,reviewed_checks={k:True for k in ('all_committed_bytes_accounted','full_chain_counts_verified','no_trailing_bytes','source_files_unchanged','owner_and_gpu_locks_released','new_KillMode_mixed_test_passed')})
  p.validate_links(*args,q,review)
  for key,value in [('original_owner_lock_acquired',False),('gpu_compute_processes',[123]),('checkpoint_sha256','0'*64)]:
   bad=copy.deepcopy(q);bad[key]=value
   with self.assertRaises(RuntimeError):p.validate_links(*args,bad,review)
  wrong=copy.deepcopy(review);wrong['parent_journal_raw_sha256']='0'*64
  with self.assertRaises(RuntimeError):p.validate_links(*args,q,wrong)
 def test_same_mathematical_and_native_sources(self):
  root=Path(__file__).resolve().parent;original=json.loads((root/'original-runtime-manifest.json').read_text())
  import hashlib
  for name,h in original['files'].items():
   if name.startswith(('source/','native-baseline/','bin/','independent/')):
    self.assertEqual(hashlib.sha256((root/'worker'/name).read_bytes()).hexdigest(),h,name)
if __name__=='__main__':unittest.main(verbosity=2)
