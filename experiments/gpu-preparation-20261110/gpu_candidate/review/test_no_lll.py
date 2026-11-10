"""CPU-only adversarial admission checks with optional LLL gate disabled."""
import os,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import candidate_reduction as c

class NoLLLGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.sched_setaffinity(0,{4,5,6,7});c.initialize()
        cls.spec=(0,16,31,(0,1),(9,10),42,88)
        cls.patch,cls.a=c.patch_basis(cls.spec)
        cls.b,u=c.core.lattice().reduce_basis(cls.a,'fpylll')
        cls.u=tuple(tuple(int(v) for v in row) for row in u)
    def test_no_gram_schmidt_but_identical_independent_certificate(self):
        expected=c.certify_transform(self.spec,self.u,self.patch,self.a)
        with patch.object(c,'is_exact_lll',side_effect=AssertionError('LLL called')):
            actual=c.certify_transform(self.spec,self.u,self.patch,self.a,require_lll=False)
        self.assertEqual(expected,actual)
    def test_unimodular_non_LLL_still_independently_certifies(self):
        u=[list(row) for row in self.u];u[0]=[x+y for x,y in zip(u[0],u[1])]
        b=c.core.lattice().matmul(u,self.a)
        self.assertFalse(c.is_exact_lll(b))
        task,token=c.certify_transform(self.spec,u,self.patch,self.a,require_lll=False)
        self.assertEqual(c.host.certify_task(task),token)
        self.assertTrue(c.night.native_safe(task))
    def test_malicious_transform_types_determinant_and_overflow(self):
        proposals=[((0,0,0),)*3,((2,0,0),(0,1,0),(0,0,1)),
            ((1.,0,0),(0,1,0),(0,0,1)),((True,0,0),(0,1,0),(0,0,1)),
            ((1,2**64,0),(0,1,0),(0,0,1)),
            ((1,c.core.MAX_I64,0),(0,1,0),(0,0,1))]
        for u in proposals:
            with self.subTest(u=u),self.assertRaises(ValueError):
                c.certify_transform(self.spec,u,self.patch,self.a,require_lll=False)
    def test_wrong_precomputed_A_fails_independent_reconstruction(self):
        a=[list(row) for row in self.a];a[0][0]*=2
        with self.assertRaises(ValueError):
            c.certify_transform(self.spec,self.u,self.patch,a,require_lll=False)

if __name__=='__main__':unittest.main(verbosity=2)
