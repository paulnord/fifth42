from pathlib import Path
import ctypes,dataclasses,json,math,os,subprocess,unittest
from fractions import Fraction
import candidate_reduction as c
class CertificateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  os.sched_setaffinity(0,{4,5,6,7});c.initialize()
  cls.spec=(0,16,31,(0,1),(9,10),42,88)
  cls.patch,cls.a=c.patch_basis(cls.spec);cls.b,cls.u=c.core.lattice().reduce_basis(cls.a,'fpylll')
  cls.u=tuple(tuple(int(v) for v in row) for row in cls.u)
 def test_correct_exact_transform_and_independent_certificate(self):
  task,token=c.certify_transform(self.spec,self.u,self.patch,self.a)
  self.assertEqual(c.host.certify_task(task),token)
  self.assertEqual(c.core.read(task.B),self.b)
 def test_singular_and_noninteger_U_rejected(self):
  for u in [((0,0,0),)*3,((1.,0,0),(0,1,0),(0,0,1)),((True,0,0),(0,1,0),(0,0,1)),((2,0,0),(0,1,0),(0,0,1))]:
   with self.assertRaises(ValueError):c.certify_transform(self.spec,u)
 def test_oversize_transform_rejected(self):
  u=((1,2**64,0),(0,1,0),(0,0,1))
  with self.assertRaises(ValueError):c.certify_transform(self.spec,u)
 def test_bad_precomputed_basis_cannot_pass_existing_certification(self):
  a=[list(row) for row in self.a];a[0][0]*=2
  with self.assertRaises(ValueError):c.certify_transform(self.spec,self.u,self.patch,a,require_lll=False)
 def test_nonreduced_basis_rejected_without_weakening_guard(self):
  with self.assertRaises(ValueError):c.certify_transform(self.spec,((1,0,0),(0,1,0),(0,0,1)))
 def test_dd_keeps_second_float_and_refuses_underflow(self):
  values=c.double_double([[c.core.lattice().Q(1,3)]*3 for _ in range(3)])
  self.assertEqual(len(values),18);self.assertNotEqual(values[1],0)
  with self.assertRaises(ValueError):c.double_double([[c.core.lattice().Q(1,10**1000)]*3 for _ in range(3)])
 def test_native_GMP_nonempty_candidate(self):
  task,token=c.certify_transform(self.spec,self.u,self.patch,self.a);batch=c.core.encode_batch([task],42)
  done=subprocess.run([str(c.WORKER/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=20)
  result=json.loads(done.stdout);self.assertTrue(result['box_complete']);self.assertEqual(result['points_visited'],task.points)
  values=c.core.decode_batch(batch,result,'emulated');self.assertIn((13,16,17,12),values)
 def test_structure_layout(self):self.assertEqual(ctypes.sizeof(c.Output),80)
if __name__=='__main__':unittest.main(verbosity=2)
