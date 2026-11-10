import json
from fractions import Fraction
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from region_coverage import (
    rectangle as r, canonical_union, difference, intersection, measure, coverage_report,
    exact_difference, exact_intersection, boundary_intersection, boundary_overlaps,
)


class RegionCoverageTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(canonical_union([]), [])
        self.assertEqual(measure([]), 0)
        self.assertEqual(coverage_report([])['regions']['planned_gaps'], [])

    def test_normalize_and_reject(self):
        self.assertEqual(r(1, 2, [0, 7], [6, 10])['right'], [3, 5])
        invalid = [(0, 1, [0, 1], [1, 2]), (2, 1, [0, 1], [1, 2]),
                   (1, 200000000001, [0, 1], [1, 2]), (True, 2, [0, 1], [1, 2]),
                   (1, 2, [0, 0], [1, 2]), (1, 2, [0, -1], [1, 2]),
                   (1, 2, [-1, 2], [1, 2]), (1, 2, [1, 2], [1, 2]),
                   (1, 2, [3, 4], [1, 2]), (1, 2, [0, 1], [1, 1]),
                   (1, 2, [0.0, 1], [1, 2]), (1, 2, [0, 1], [True, 2])]
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                r(*args)
        with self.assertRaises(ValueError):
            canonical_union([{}])

    def test_nested_duplicate_and_adjacent(self):
        a = r(1, 3, [0, 1], [1, 2])
        nested = r(2, 2, [1, 10], [2, 5])
        adjacent = r(1, 3, [1, 2], [9, 10])
        self.assertEqual(canonical_union([a, nested, a, adjacent]),
                         [r(1, 3, [0, 1], [9, 10])])
        self.assertEqual(canonical_union([r(1, 1, [0, 1], [1, 2]),
                                          r(2, 3, [0, 1], [1, 2])]), [a])

    def test_denominator_slabs(self):
        a, b = r(1, 3, [0, 1], [1, 2]), r(3, 5, [1, 4], [3, 4])
        self.assertEqual(canonical_union([b, a]), [r(1, 2, [0, 1], [1, 2]),
            r(3, 3, [0, 1], [3, 4]), r(4, 5, [1, 4], [3, 4])])
        self.assertEqual(measure([a, b]), Fraction(11, 4))
        self.assertEqual(measure([a, b], True), Fraction(33, 4))
        self.assertEqual(measure(intersection([a], [b])), Fraction(1, 4))

    def test_gaps_novelty_and_attempts(self):
        plan = r(1, 4, [0, 1], [9, 10])
        old = r(1, 2, [0, 1], [1, 2])
        new = r(2, 3, [1, 4], [3, 4])
        report = coverage_report([plan], [old], [new, new], [plan], [plan])
        m = report['measures']['row_ratio_area']
        self.assertEqual(m['newly_covered'], [3, 4])
        self.assertEqual(m['prior_overlap'], [1, 4])
        self.assertEqual(m['committed_duplicate_excess'], [1, 1])
        self.assertEqual(m['committed_non_novel_excess'], [5, 4])
        self.assertEqual(m['planned_gaps'], [37, 20])
        self.assertEqual(m['total_covered'], [7, 4])
        self.assertEqual(json.loads(json.dumps(report)), report)
        self.assertEqual(coverage_report([plan], guarded=[plan], incomplete=[plan])
                         ['regions']['planned_gaps'], [plan])

    def test_difference_endpoints_and_large_rows(self):
        full = r(1, 200000000000, [0, 1], [9, 10])
        middle = r(1, 200000000000, [1, 5], [3, 5])
        self.assertEqual(difference([full], [middle]), [
            r(1, 200000000000, [0, 1], [1, 5]),
            r(1, 200000000000, [3, 5], [9, 10])])
        self.assertEqual(measure([full]), 180000000000)
        self.assertEqual(difference([full], [full]), [])
        self.assertEqual(intersection([r(1, 1, [0, 1], [1, 2])],
                                       [r(1, 1, [1, 2], [9, 10])]), [])

    def test_exact_narrow_width_and_outside_plan(self):
        denominator = 10**30
        narrow = r(1, 1, [1, 2], [denominator + 1, 2 * denominator])
        self.assertEqual(measure([narrow]), Fraction(1, 2 * denominator))
        plan = r(1, 1, [0, 1], [1, 5])
        report = coverage_report([plan], committed=[narrow])
        self.assertEqual(report['regions']['covered_outside_plan'], [narrow])
        self.assertEqual(report['regions']['planned_gaps'], [plan])
        self.assertEqual(measure([r(200000000000, 200000000000,
                                    [0, 1], [1, 2])], True), 100000000000)

    def test_exact_difference_membership(self):
        a, b, c = [1, 10], [1, 2], [9, 10]
        def component(left, right, lc, rc):
            return dict(cmin=1, cmax=3, left=left, right=right,
                        left_closed=lc, right_closed=rc)
        cases = [([r(1, 3, a, b)], [r(1, 3, b, c)], [component(a, b, True, False)]),
                 ([r(1, 3, a, c)], [r(1, 3, b, c)], [component(a, b, True, False)]),
                 ([r(1, 3, a, c)], [r(1, 3, a, b)], [component(b, c, False, True)])]
        for first, second, expected in cases:
            self.assertEqual(exact_difference(first, second), expected)
        self.assertEqual(exact_difference([r(1, 3, a, c)], [r(1, 3, a, c)]), [])
        self.assertEqual(exact_difference([r(1, 3, a, c)], []),
                         [component(a, c, True, True)])
        # Do not silently re-close exact components when fed to the closed API.
        with self.assertRaises(ValueError):
            canonical_union(cases[0][2])

    def test_boundary_intersections_and_report(self):
        left = r(1, 3, [0, 1], [1, 2])
        right = r(2, 4, [1, 2], [9, 10])
        point = dict(cmin=2, cmax=3, left=[1, 2], right=[1, 2],
                     left_closed=True, right_closed=True)
        self.assertEqual(exact_intersection([left], [right]), [point])
        self.assertEqual(boundary_intersection([left], [right]), [point])
        self.assertEqual(boundary_overlaps([left, right, right]), [point])
        self.assertEqual(boundary_intersection([left], [left]), [])
        report = coverage_report([r(1, 4, [0, 1], [9, 10])], [left], [right])
        self.assertEqual(report['boundary_overlaps']['prior'], [point])
        self.assertEqual(report['exact_regions']['prior_overlap'], [point])
        self.assertFalse(report['exact_regions']['newly_covered'][0]['left_closed'])
        self.assertTrue(report['exact_regions']['newly_covered'][1]['left_closed'])
        json.dumps(report)

    def test_small_grid_reference(self):
        rng = random.Random(471)
        def sample():
            lo, hi = sorted(rng.sample(range(1, 8), 2))
            left, right = sorted(rng.sample(range(10), 2))
            return r(lo, hi, [left, 10], [right, 10])
        def cells(regions):
            return {(c, x) for a in regions for c in range(a['cmin'], a['cmax'] + 1)
                    for x in range(9) if Fraction(*a['left']) <= Fraction(2*x+1, 20)
                    < Fraction(*a['right'])}
        for _ in range(80):
            a, b = [sample() for _ in range(6)], [sample() for _ in range(4)]
            ca, cb = cells(a), cells(b)
            self.assertEqual(measure(a), Fraction(len(ca), 10))
            self.assertEqual(cells(difference(a, b)), ca - cb)
            self.assertEqual(cells(intersection(a, b)), ca & cb)
            self.assertEqual(canonical_union(canonical_union(a)), canonical_union(a))
            self.assertEqual(measure(a), measure(difference(a, b)) + measure(intersection(a, b)))
            def contains(regions, c, x):
                return any(region['cmin'] <= c <= region['cmax']
                           and (Fraction(*region['left']) < x or
                                (Fraction(*region['left']) == x and region.get('left_closed', True)))
                           and (x < Fraction(*region['right']) or
                                (x == Fraction(*region['right']) and region.get('right_closed', True)))
                           for region in regions)
            exact = exact_difference(a, b)
            overlap = exact_intersection(a, b)
            for c in range(1, 8):
                for numerator in range(19):
                    x = Fraction(numerator, 20)
                    in_a, in_b = contains(a, c, x), contains(b, c, x)
                    self.assertEqual(contains(exact, c, x), in_a and not in_b)
                    self.assertEqual(contains(overlap, c, x), in_a and in_b)


if __name__ == '__main__':
    unittest.main()
