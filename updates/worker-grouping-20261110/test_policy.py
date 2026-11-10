import copy,json,unittest
from pathlib import Path
from plan_update import choose,reconcile
S=json.loads((Path(__file__).parent/'published-samples.json').read_text())
class Tests(unittest.TestCase):
 def test_published_win(self):self.assertEqual(choose(S,2572492928,'s','cabbage','cabbage')['group_limit'],8)
 def test_ada_region(self):self.assertEqual(choose(S,4564955776,'s','cabbage','cabbage')['group_limit'],4)
 def test_dense(self):self.assertEqual(choose(S,9562500096,'s','cabbage','cabbage')['group_limit'],4)
 def test_wrong_host(self):
  with self.assertRaises(ValueError):choose(S,2572492928,'s','boole','cabbage')
 def test_current_unmeasured(self):
  with self.assertRaises(ValueError):choose(S,1538849024,'s','cabbage','cabbage')
 def test_duplicate(self):
  with self.assertRaises(ValueError):choose(S+S,2572492928,'s','cabbage','cabbage')
 def test_failed_audit(self):
  s=copy.deepcopy(S)
  for r in s:r['audit_count']=0
  with self.assertRaises(ValueError):choose(s,2572492928,'s','cabbage','cabbage')
 def test_bad_repeat(self):
  s=copy.deepcopy(S);next(r for r in s if r['first']==2572492928)['points']=-1
  with self.assertRaises(ValueError):choose(s,2572492928,'s','cabbage','cabbage')
 def test_checkpoint(self):
  cp=dict(next_patch=8,window=dict(first=1,last=9))
  self.assertEqual(reconcile(cp,cp,dict(worker_exit_code=0,leases_released=True,error=None)),8)
  with self.assertRaises(ValueError):reconcile(cp,dict(cp,next_patch=9),dict(worker_exit_code=0,leases_released=True,error=None))
 def test_partial_supervisor(self):
  with self.assertRaises(ValueError):reconcile({}, {}, dict(error=None))
if __name__=='__main__':unittest.main()
