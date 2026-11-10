#!/usr/bin/env python3
"""Independent, bounded mathematical coverage audit; run python audit_tests.py."""
import itertools
import random
import unittest
from fractions import Fraction as Q
import lattice5 as L


def brute_positive(n, cap_at):
    return {(a,b,c,a**5+b**5-c**5)
            for c in range(2,n+1) for b in range(1,c) for a in range(1,b+1)
            if abs(a**5+b**5-c**5)<=cap_at(c)}


def inverse(a):
    d=L.det3(a)
    return [[Q(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3],d) for j in range(3)] for i in range(3)]


class IndependentAudit(unittest.TestCase):
    def test_root_enclosures(self):
        values=[Q(0),Q(1),Q(1,2),Q(32),Q(1,10**25),Q(123456789,987654321)]
        values += [Q(i,16)**5 for i in range(1,25)]
        for bits in (1,8,48):
            for x in values:
                lo,hi=L.root_bracket(x,bits)
                self.assertLessEqual(lo**5,x)
                self.assertLessEqual(x,hi**5)
                self.assertLessEqual(hi-lo,Q(1,2**bits))

    def test_exact_sphere_against_independent_box(self):
        rng=random.Random(816)
        for _ in range(16):
            # Well-conditioned input with exact rational entries and random shear.
            a=[[Q(1),Q(rng.randint(-2,2),3),Q(rng.randint(-2,2),3)],
               [Q(0),Q(1),Q(rng.randint(-2,2),3)], [Q(0),Q(0),Q(1)]]
            b,u=L.lll(a)
            self.assertEqual(L.matmul(u,a),b)
            self.assertEqual(abs(L.det3(u)),1)
            inv=inverse(b)
            self.assertEqual(L.matmul(b,inv),[[Q(i==j) for j in range(3)] for i in range(3)])
            # ||x||<=sqrt(3)<2 implies |n_j|<=2 sum_i |B^-1_ij|.
            bounds=[L.floor(2*sum(abs(inv[i][j]) for i in range(3))) for j in range(3)]
            expected=set()
            for n in itertools.product(*(range(-k,k+1) for k in bounds)):
                x=[sum(n[i]*b[i][j] for i in range(3)) for j in range(3)]
                if sum(v*v for v in x)<=3:
                    expected.add(n)
            got=set(L.sphere_coefficients(b,L.Stats(),L.Budget()))
            self.assertEqual(got,expected)
        identity=[[Q(i==j) for j in range(3)] for i in range(3)]
        # All eight cube corners lie exactly on the enclosing sphere.
        self.assertEqual(len(set(L.sphere_coefficients(identity,L.Stats(),L.Budget()))),27)

    def test_sharp_upper_u_boundary(self):
        p=L.make_patch(10,10,Q(4,5),Q(9,10),18098)
        self.assertTrue(p.contains(9,9,10))
        self.assertIn((9,9,10,18098),L.patch_search(p,lambda r,c:True))
        result=L.search_positive(10,cap=18098)
        self.assertIn((9,9,10,18098),result['hits'])

    def test_patch_contains_every_brute_candidate(self):
        for cmin,cmax,cap in [(3,5,42),(8,15,846),(16,20,18098)]:
            candidates=brute_positive(cmax,lambda c:cap)
            for i in range(9):
                p=L.make_patch(cmin,cmax,Q(i,10),Q(i+1,10),cap)
                for a,b,c,r in candidates:
                    if c>=cmin and p.left*c<=a<=p.right*c:
                        self.assertTrue(p.contains(a,b,c),(p,a,b,c,r))

    def test_full_hit_sets_and_signed_box(self):
        for cap in (0,42,846,18098):
            for width in (1,3):
                result=L.search_positive(40,cap=cap,width=width)
                self.assertTrue(result['complete'])
                self.assertEqual(set(result['hits']),brute_positive(40,lambda c:cap))
        result=L.search_positive(60,mode='healy')
        self.assertEqual(set(result['hits']),brute_positive(60,lambda c:5*c*c))
        result=L.signed42(100)
        self.assertEqual(set(result['signed_hits']),L.signed_reference(100,42))
        self.assertEqual(L.signed_reference(2,42),set())

    def test_direct_fallback_internal_budget(self):
        # A single oversized shell must stop inside its loops, not at shell end.
        for cap in (0,10**30):
            stats=L.Stats()
            with self.assertRaisesRegex(L.BudgetExceeded,"direct fallback work limit"):
                L.direct_positive(1000,1000,lambda c:cap,lambda r,c:True,
                                  stats,L.Budget(max_nodes=20))
            self.assertLessEqual(stats.direct_pairs,256)
            self.assertLessEqual(stats.direct_candidates,256)
        with self.assertRaisesRegex(L.BudgetExceeded,"direct fallback work limit"):
            L.search_positive(1000,cap=10**30,max_nodes=20)

    def test_fail_closed_budget(self):
        with self.assertRaises(L.BudgetExceeded):
            L.search_positive(40,max_nodes=0)
        with self.assertRaises(L.BudgetExceeded):
            L.search_positive(40,max_patches=0)

if __name__=='__main__':
    unittest.main(verbosity=2)
