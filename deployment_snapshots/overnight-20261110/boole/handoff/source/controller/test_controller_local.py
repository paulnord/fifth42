"""Queue adoption and artifact tests without touching the running computation."""
import hashlib,json,sys,tarfile,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import controller,delegated_publication
class ControllerAdmissionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.stage=json.loads((ROOT/'stages.json').read_bytes())['stages'][0]
  cls.config=controller.load_stage(cls.stage)
 def test_actual_frozen_archive_readback(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as temp:
   p=Path(temp)/'source.tar.gz';digest=delegated_publication.archive(Path(self.stage['root']),p,controller)
   self.assertEqual(digest,controller.sha(p))
   with tarfile.open(p) as t:
    self.assertEqual(t.extractfile('production-config.json').read(),Path(self.stage['config']).read_bytes())
    self.assertEqual(hashlib.sha256(t.extractfile('worker/bin/scaling_gmp').read()).hexdigest(),'8d514a59a5488de9a16a2f7ab0ecd351fdc13816298ddb777a18d9aa94158eb6')
 def test_changed_configuration_is_rejected(self):
  bad=dict(self.stage,config_sha256='0'*64)
  with self.assertRaisesRegex(RuntimeError,'configuration changed'):controller.load_stage(bad)
 def test_changed_manifest_is_rejected(self):
  with self.assertRaisesRegex(RuntimeError,'manifest changed'):controller.load_stage(dict(self.stage,manifest_sha256='0'*64))
 def test_partial_predecessor_is_rejected(self):
  old=Path('/home/pnord/fifth42-local-runs/TEST_ONLY_boole_extra_20261109/boole-extra-test-rollover-r1-b-20261109/run')
  c=json.loads((ROOT.parent/'boole-overnight-controller-20261109/test-b-config.json').read_bytes())
  c['range_end']+=256
  with self.assertRaisesRegex(RuntimeError,'partial'):controller.verify_finished(c,allow_test=True)
 def test_existing_output_is_rejected(self):
  p=Path('/home/pnord/boole-overnight-controller-20261109/test-b-config.json');c=json.loads(p.read_bytes());c['stop_epoch']=1794351600
  with self.assertRaisesRegex(RuntimeError,'Existing output'):controller.start_stage(dict(root='/unused'),c)
 def test_adopts_completed_stage_without_restart(self):
  path=Path('/home/pnord/boole-overnight-controller-20261109/test-b-config.json');c=json.loads(path.read_bytes())
  spec=dict(root='/home/pnord/boole-extra-20261109-b',config=str(path),config_sha256=controller.sha(path),manifest_sha256=c['manifest_sha256'],first=c['initial_patch'],last=c['range_end'])
  with tempfile.TemporaryDirectory(dir=ROOT) as folder:
   folder=Path(folder);plan=dict(TEST_ONLY=True,automatic_resume=False,stop_epoch=c['stop_epoch'],stop_local=c['stop_local'],controller_sha256=controller.sha(ROOT/'controller.py'),stages=[spec],status_file=str(folder/'status.json'))
   path=folder/'plan.json';controller.atomic(path,plan)
   with patch.object(sys,'argv',['controller.py','--plan',str(path),'--plan-sha256',controller.sha(path),'--adopt-first']),patch.object(controller.time,'time',return_value=c['stop_epoch']-120),patch.object(controller,'unit',return_value=dict(ActiveState='inactive')),patch.object(controller,'free_lock',return_value=True),patch.object(controller.subprocess,'check_output',return_value=''),patch.object(controller,'start_stage') as start:
    controller.main();start.assert_not_called()
   report=json.loads((folder/'status.json').read_bytes());self.assertEqual(report['status'],'all_assigned_work_complete');self.assertEqual(len(report['completed']),1)
if __name__=='__main__':unittest.main(verbosity=2)
