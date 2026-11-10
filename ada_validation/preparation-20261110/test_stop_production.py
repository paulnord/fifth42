"""Manual stop intent precedes controller shutdown and dynamic owner shutdown."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import stop_production as stop
class StopTests(unittest.TestCase):
 def test_intent_precedes_every_stop_and_targets_current_rotation(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);worker=root/'new-worker';worker.mkdir();(root/'rotation-state.json').write_text(json.dumps(dict(active=dict(worker=str(worker),service='owned-new-rotation.service'))));calls=[]
   def run(args,**kw):
    self.assertTrue((root/'STOP_CONTROLLER').exists())
    if args[-1]=='owned-new-rotation.service':self.assertTrue((worker/'STOP').exists())
    calls.append(args[-1])
   with patch.object(stop,'R',root),patch.object(stop.subprocess,'run',side_effect=run),patch.object(stop.time,'sleep'):
    stop.main()
   self.assertEqual(calls,['ada-preparation-rotation-20261110.service','owned-new-rotation.service','owned-new-rotation.service'])
 def test_initial_owner_is_targeted_before_controller_state_exists(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'worker').mkdir();calls=[]
   def run(args,**kw):self.assertTrue((root/'STOP_CONTROLLER').exists());calls.append(args[-1])
   with patch.object(stop,'R',root),patch.object(stop.subprocess,'run',side_effect=run),patch.object(stop.time,'sleep'):stop.main()
   self.assertEqual(calls[-1],'ada-preparation-20261110.service');self.assertTrue((root/'worker/STOP').exists())
if __name__=='__main__':unittest.main(verbosity=2)
