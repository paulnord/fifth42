from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import exploration_plan as e
import region_coverage as r


class ExplorationPlanning(unittest.TestCase):
    def test_plan_is_bounded_disjoint_and_has_no_novelty_overclaim(self):
        plan=e.build_plan()
        self.assertEqual(plan['status'],'prepared_not_launched')
        self.assertFalse(plan['prior_coverage_is_exhaustive'])
        self.assertEqual(sum(m['seconds_budget'] for m in plan['methods']),180)
        for i,a in enumerate(plan['methods']):
            for b in plan['methods'][i+1:]:self.assertFalse(r.intersection(a['planned_scope'],b['planned_scope']))

    def test_lazy_specifications_tile_remaining_rational_scope_exactly(self):
        method=dict(width=32,remaining_scope=[r.rectangle(100,199,[1,10],[9,10])])
        specs=list(e.iter_specifications(method))
        self.assertEqual(len(specs),3)
        self.assertEqual(specs[0][3],(1,10));self.assertEqual(specs[-1][4],(9,10))
        for a,b in zip(specs,specs[1:]):self.assertEqual(a[4],b[3])
        covered=[r.rectangle(s[1],s[2],s[3],s[4]) for s in specs]
        self.assertEqual(r.canonical_union(covered),method['remaining_scope'])

    def test_previously_committed_region_is_not_scheduled_again(self):
        initial=e.build_plan()['methods'][0]['planned_scope'][0]
        prior=[dict(initial,right=e.pair(Fraction(*initial['left'])+Fraction(1,200000)))]
        plan=e.build_plan(prior)
        self.assertFalse(r.intersection(plan['methods'][0]['remaining_scope'],prior))
        self.assertEqual(r.canonical_union(prior+plan['methods'][0]['remaining_scope']),[initial])

    def test_result_accounting_uses_new_geometry_not_patch_count(self):
        scope=[r.rectangle(10,19,[1,10],[3,10])]
        old=[r.rectangle(10,19,[1,10],[2,10])]
        committed=[r.rectangle(10,19,[1,10],[3,10])]
        report=e.result_accounting(dict(planned_scope=scope),old,committed,elapsed_ns=2000000000)
        self.assertEqual(report['new_ratio_denominator_measure_per_second'],[1,2])
        self.assertFalse(report['algorithm_speedup_claim'])
        with self.assertRaises(ValueError):e.result_accounting(dict(planned_scope=scope),old,[r.rectangle(1,100,[1,10],[4,10])],elapsed_ns=1)


if __name__=='__main__':unittest.main()
