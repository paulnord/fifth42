import itertools
import importlib.util
import unittest
from fractions import Fraction as Q
import lattice5 as l
import modular_filters as f

class ModularTests(unittest.TestCase):
    def test_coefficient_mapping_and_residues(self):
        u = [[1,2,-1],[0,1,3],[0,0,1]]
        filt = f.TargetFilter(u, [-42,42,12])
        for n in itertools.product(range(-4,5), repeat=3):
            c,a,b = [sum(n[k]*u[k][j] for k in range(3)) for j in range(3)]
            expected = all(any((a**5+b**5-c**5-t) % m == 0 for t in filt.targets) for m in filt.moduli)
            self.assertEqual(filt.accepts_original(c,a,b), expected)
            self.assertEqual(all(n[0] % m in filt.allowed_first(m,n[1],n[2]) for m in filt.moduli), expected)

    def test_filtered_sphere_exact_set(self):
        a = [[Q(1,4),Q(1,5),Q(0)],[Q(0),Q(1,3),Q(1,7)],[Q(0),Q(0),Q(1,2)]]
        b,u = l.lll(a)
        for targets in ([0],[-42,42],[12,384]):
            filt = f.TargetFilter(u, targets)
            full = set(l.sphere_coefficients(b,l.Stats(),l.Budget()))
            want = {n for n in full if filt.accepts_original(*[sum(n[k]*u[k][j] for k in range(3)) for j in range(3)])}
            got = set(f.filtered_sphere(b,filt,l.Stats(),l.Budget(),f.FilterStats()))
            self.assertEqual(got,want)
            if targets == [0]:
                self.assertIn((0,0,0),got)

    def test_nonempty_patch_controls(self):
        p = l.make_patch(17,34,Q(13,17),Q(4,5),384)
        expected = {(13,16,17,12),(26,32,34,384)}
        for mods in ((25,),(31,),(61,),(25,31,61),()):
            for mode in ('none','post','prune','progression','interval'):
                got = f.search_patch(p,[12,384],mode,mods)
                self.assertEqual(set(map(tuple,got['hits'])),expected)

    def test_empty_42_is_not_only_control(self):
        p = l.make_patch(17,34,Q(13,17),Q(4,5),42)
        expected = l.patch_search(p, lambda r,c: abs(r)==42)
        for mode in ('none','post','prune','progression','interval'):
            self.assertEqual(set(map(tuple,f.search_patch(p,[-42,42],mode)['hits'])),expected)

    @unittest.skipUnless(importlib.util.find_spec('fpylll'), 'optional fpylll dependency absent')
    def test_fpylll_nonempty_and_mapping(self):
        p = l.make_patch(17,34,Q(13,17),Q(4,5),384)
        b,u = l.reduce_basis(p.basis(), 'fpylll')
        self.assertEqual(l.matmul(u,p.basis()),b)
        self.assertEqual(abs(l.det3(u)),1)
        expected = {(13,16,17,12),(26,32,34,384)}
        for mode in ('none','post','prune','progression','interval'):
            self.assertEqual(set(map(tuple,f.search_patch(p,[12,384],mode,backend='fpylll')['hits'])),expected)

    def test_full_positive_nonempty_and_signed42(self):
        expected = {(13,16,17,12),(26,32,34,384)}
        for mode in ('none','post','prune','progression','interval'):
            result = f.search_targets_positive(34,[12,384],mode=mode)
            self.assertEqual(set(map(tuple,result['hits'])),expected)
            result = f.signed42_filtered(40,mode=mode)
            self.assertEqual(set(map(tuple,result['signed_hits'])),l.signed_reference(40,42))
            self.assertEqual(result['shells'],l.signed42(40)['shells'])
        with self.assertRaises(l.BudgetExceeded):
            f.signed42_filtered(100,mode='prune',max_nodes=1)
        with self.assertRaises(l.BudgetExceeded):
            f.signed42_filtered(100,mode='prune',max_patches=1)

    def test_generator_moduli(self):
        p = l.make_patch(17,34,Q(13,17),Q(4,5),384)
        for call,args in ((f.search_patch,(p,[12,384])),
                          (f.search_targets_positive,(34,[12,384]))):
            tuple_result = call(*args,mode='prune',moduli=(25,31,61))
            generator_result = call(*args,mode='prune',moduli=(m for m in (25,31,61)))
            self.assertEqual(tuple_result['hits'],generator_result['hits'])
            self.assertEqual(tuple_result['filter_stats'],generator_result['filter_stats'])
            self.assertEqual(tuple_result['moduli'],generator_result['moduli'])

    def test_random_progressions_and_intervals(self):
        import random
        rng=random.Random(325)
        for trial in range(20):
            a=[[Q(rng.randint(-3,3),rng.randint(1,5)) for j in range(3)] for i in range(3)]
            if not l.det3(a):continue
            b,u=l.lll(a)
            for targets,mods in [([0],()),([-42,42],(25,31,61)),([12,384],(25,))]:
                filt=f.TargetFilter(u,targets,mods)
                base_stats=l.Stats()
                want=set(f.filtered_sphere(b,filt,base_stats,l.Budget(),f.FilterStats()))
                for interval in [False,True]:
                    stats=l.Stats()
                    got=set(f.filtered_sphere(b,filt,stats,l.Budget(),f.FilterStats(),True,interval))
                    self.assertEqual(got,want)
                    self.assertEqual(stats.enumeration_nodes,base_stats.enumeration_nodes)
        for mode in ['progression','interval']:
            with self.assertRaises(l.BudgetExceeded):
                f.signed42_filtered(100,mode=mode,max_nodes=1)

    def test_fail_closed(self):
        p = l.make_patch(17,34,Q(13,17),Q(4,5),384)
        with self.assertRaises(l.BudgetExceeded):
            f.search_patch(p,[12,384],'prune',budget=l.Budget(max_nodes=0))
        with self.assertRaises(ValueError):
            f.search_patch(p,[385])

if __name__ == '__main__':
    unittest.main(verbosity=2)
