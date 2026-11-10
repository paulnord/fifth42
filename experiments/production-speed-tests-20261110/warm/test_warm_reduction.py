import importlib.util
import os
from pathlib import Path
import sys
import unittest
from fractions import Fraction as Q
from warm_reduction import WarmReducer,verify


def load(path):
    spec=importlib.util.spec_from_file_location('warm_reference',path)
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    return mod

SOURCE=Path(os.environ['LATTICE_SOURCE'])
L=load(SOURCE)

class WarmTests(unittest.TestCase):
    def test_neighbor_exact(self):
        reducer=WarmReducer(L,'reference')
        for j in range(8):
            a=L.make_patch(20,40,Q(j+1,100),Q(j+2,100),42,48).basis()
            b,u=reducer(a)
            verify(L,a,b,u)
            # Exact LLL conditions, not merely equivalent lattice.
            mu,n=L.gram_schmidt(b)
            for i in range(3):
                for k in range(i):self.assertLessEqual(abs(mu[i][k]),Q(1,2))
            for i in (1,2):self.assertGreaterEqual(n[i],(Q(3,4)-mu[i][i-1]**2)*n[i-1])
        self.assertEqual(reducer.stats.warm,7)

    def test_complete_sphere_point_sets(self):
        r=WarmReducer(L,'reference')
        total=0
        for j in range(4):
            patch=L.make_patch(20,40,Q(20+j,100),Q(21+j,100),100000,48)
            a=patch.basis();cold=L.reduce_basis(a);warm=r(a)
            def points(pair):
                b,u=pair
                return {tuple(sum(n[k]*u[k][col] for k in range(3)) for col in range(3))
                        for n in L.sphere_coefficients(b,L.Stats(),L.Budget())}
            expected,actual=points(cold),points(warm)
            self.assertEqual(expected,actual);total+=len(actual)
        self.assertGreater(total,0)

    def test_invalid_seed_fallback(self):
        for seed in ([[2,0,0],[0,1,0],[0,0,1]],[[1,0,0],[0,1,0],[1<<100,0,1]],[[1]]):
            r=WarmReducer(L,'reference');r.seed=seed
            a=[[Q(1),Q(0),Q(0)],[Q(0),Q(2),Q(0)],[Q(0),Q(0),Q(3)]]
            b,u=r(a);verify(L,a,b,u);self.assertEqual(r.stats.fallbacks,1)

    def test_wrong_result_fallback(self):
        count=0
        def broken_once(a,backend):
            nonlocal count
            count+=1
            if count==1:return a,[[2,0,0],[0,1,0],[0,0,1]]
            return L.reduce_basis(a,backend)
        r=WarmReducer(L,'reference',reducer=broken_once);r.seed=[[1,0,0],[0,1,0],[0,0,1]]
        a=[[Q(1),Q(0),Q(0)],[Q(0),Q(2),Q(0)],[Q(0),Q(0),Q(3)]]
        b,u=r(a);verify(L,a,b,u);self.assertEqual(r.stats.fallbacks,1)

    def test_bad_cold_raises(self):
        def bad(a,_):return a,[[2,0,0],[0,1,0],[0,0,1]]
        r=WarmReducer(L,'reference',reducer=bad)
        with self.assertRaises(ValueError):r([[Q(1),Q(0),Q(0)],[Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(1)]])

    def test_reset(self):
        r=WarmReducer(L,'reference');r.seed=[[1,0,0],[0,1,0],[0,0,1]];r.clear();self.assertIsNone(r.seed)

if __name__=='__main__':unittest.main()
