import unittest
from unittest.mock import patch
from fractions import Fraction as Q
import random
import lattice5 as l

class PublishedBackends(unittest.TestCase):
    def test_random_transforms_and_enumeration(self):
        rng=random.Random(20261104)
        for backend in ['sympy','fpylll']:
            for _ in range(15):
                a=[[Q(rng.randint(-3,3),rng.randint(1,5)) for j in range(3)] for i in range(3)]
                if not l.det3(a):continue
                ref,ur=l.lll(a); b,u=l.reduce_basis(a,backend)
                self.assertEqual(abs(l.det3(u)),1);self.assertEqual(l.matmul(u,a),b)
                def physical(b,u):
                    return {tuple(sum(n[k]*u[k][j] for k in range(3)) for j in range(3)) for n in l.sphere_coefficients(b,l.Stats(),l.Budget())}
                self.assertEqual(physical(ref,ur),physical(b,u))
    def test_positive_nonempty_targets(self):
        for target in [12,42,2951]:
            expected=l.direct_positive(1,50,lambda c:target,lambda r,c:abs(r)<=target)
            for backend in ['sympy','fpylll']:
                actual=l.search_positive(50,cap=target,backend=backend)
                self.assertEqual(set(actual['hits']),expected)
        self.assertTrue(any(abs(row[3])==12 for row in l.search_positive(50,cap=12,backend='fpylll')['hits']))
    def test_invalid_transform_fails_closed(self):
        for backend in ['sympy','fpylll']:
            with patch.object(l,'det3',return_value=2):
                with self.assertRaises(l.BudgetExceeded):
                    l.reduce_basis([[1,0,0],[0,1,0],[0,0,1]],backend)
    def test_guards_all_backends(self):
        for backend in ['sympy','fpylll']:
            with self.assertRaises(l.BudgetExceeded):l.search_positive(100,backend=backend,max_patches=0)
            with self.assertRaises(l.BudgetExceeded):l.search_positive(100,backend=backend,max_nodes=0)
    def test_no_silent_unknown_backend(self):
        with self.assertRaises(ValueError):l.search_positive(1,backend='typo')
if __name__=='__main__':unittest.main()
