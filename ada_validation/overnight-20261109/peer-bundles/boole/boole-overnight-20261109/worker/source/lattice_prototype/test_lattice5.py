import itertools
import random
import unittest
from fractions import Fraction as Q
import lattice5 as l


class ExactArithmeticTests(unittest.TestCase):
    def test_integer_roots(self):
        for n in list(range(1000))+[10**55-1,10**55,10**55+1,2**256]:
            r=l.iroot(n)
            self.assertLessEqual(r**5,n)
            self.assertGreater((r+1)**5,n)

    def test_outward_roots(self):
        for x in [Q(0),Q(1),Q(1,32),Q(7,11),Q(2**200,3),Q(1,10**20)]:
            for bits in [16,48,96]:
                lo,hi=l.root_bracket(x,bits)
                self.assertLessEqual(lo**5,x)
                self.assertGreaterEqual(hi**5,x)
                self.assertLessEqual(hi-lo,Q(1,2**bits))

    def test_unimodular_reconstruction_and_lll(self):
        rng=random.Random(7321)
        for _ in range(25):
            a=[[Q(rng.randrange(-20,21),rng.randrange(1,10)) for j in range(3)] for i in range(3)]
            if l.det3(a)==0:
                continue
            b,u=l.lll(a)
            self.assertEqual(l.matmul(u,a),b)
            self.assertEqual(abs(l.det3(u)),1)
            mu,n=l.gram_schmidt(b)
            for i in range(3):
                for j in range(i):
                    self.assertLessEqual(abs(mu[i][j]),Q(1,2))
            for i in range(1,3):
                self.assertGreaterEqual(n[i],(Q(3,4)-mu[i][i-1]**2)*n[i-1])

    def test_sphere_enumeration_against_cube_oracle(self):
        matrices=[[[Q(1),Q(0),Q(0)],[Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(1)]],
                  [[Q(1,2),Q(1,3),Q(0)],[Q(0),Q(2,3),Q(1,4)],[Q(0),Q(0),Q(3,4)]]]
        for a in matrices:
            b,u=l.lll(a)
            actual=set(l.sphere_coefficients(b,l.Stats(),l.Budget()))
            expected=set()
            for ns in itertools.product(range(-10,11),repeat=3):
                v=[sum(ns[i]*b[i][j] for i in range(3)) for j in range(3)]
                if l.dot(v,v)<=3:
                    expected.add(ns)
            self.assertEqual(actual,expected)


class CoverageTests(unittest.TestCase):
    def test_nonempty_healy_overlap(self):
        got=l.search_positive(100,mode="healy")
        exact=l.direct_positive(1,100,lambda c:5*c*c,lambda r,c:abs(r)<=5*c*c)
        self.assertEqual(set(map(tuple,got['hits'])),exact)
        self.assertEqual(len(exact),5)
        self.assertIn((13,16,17,12),exact)
        self.assertIn((42,71,72,2951),exact)

    def test_constant_caps_and_boundaries(self):
        for bound,cap in [(2,42),(17,12),(34,384),(10,18098),(40,0),(40,42),(25,10000)]:
            actual=l.search_positive(bound,cap=cap)
            exact=l.direct_positive(1,bound,lambda c:cap,lambda r,c:abs(r)<=cap)
            self.assertEqual(set(map(tuple,actual['hits'])),exact,(bound,cap))

    def test_selected_patch_boundary(self):
        # Both denominator endpoints and a/c patch edges are inclusive.
        p=l.make_patch(17,34,Q(13,17),Q(4,5),384)
        hits=l.patch_search(p,lambda r,c:True)
        self.assertIn((13,16,17,12),hits)
        self.assertIn((26,32,34,384),hits)
        p=l.make_patch(10,10,Q(4,5),Q(9,10),18098)
        self.assertIn((9,9,10,18098),l.patch_search(p,lambda r,c:True))

    def test_signed42_full_box(self):
        for bound in [1,2,8,40,100]:
            result=l.signed42(bound)
            self.assertEqual(set(map(tuple,result['signed_hits'])),l.signed_reference(bound,42))

    def test_fail_closed_budget(self):
        with self.assertRaises(l.BudgetExceeded):
            l.search_positive(100,max_nodes=1)
        with self.assertRaises(l.BudgetExceeded):
            l.search_positive(100,max_patches=1)

    def test_reject_bad_parameters(self):
        for args in [(0,1,Q(0),Q(1,2),42),(1,2,Q(0),Q(1),42),
                     (1,2,Q(0),Q(9,10),42)]:
            with self.assertRaises(ValueError):
                l.make_patch(*args)

if __name__=='__main__':
    unittest.main(verbosity=2)
