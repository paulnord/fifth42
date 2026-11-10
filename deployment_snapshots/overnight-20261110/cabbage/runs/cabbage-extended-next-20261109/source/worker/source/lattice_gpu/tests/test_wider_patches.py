import os
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scaling_core as core
import wider_patch_experiment as wider
from engine_session import EngineSession


class WiderPatches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(Path(os.environ.get('SCALING_LATTICE_SOURCE', ROOT.parent / 'lattice_prototype')))

    def test_exact_shared_endpoints_and_nested_partitions(self):
        previous = None
        for width in wider.WIDTHS:
            specs = wider.shared_specs(width)
            self.assertEqual(len(specs), wider.SPAN // width)
            self.assertEqual(Fraction(*specs[0][3]), wider.LEFT)
            self.assertEqual(Fraction(*specs[-1][4]), wider.RIGHT)
            for spec in specs:
                self.assertEqual(spec[1:3], (wider.HIGH_LO, wider.HIGH_HI))
                self.assertEqual((Fraction(*spec[4]) - Fraction(*spec[3])) * wider.HIGH_LO, width)
            for a, b in zip(specs, specs[1:]):
                self.assertEqual(a[4], b[3])
            endpoints = {s[3] for s in specs} | {specs[-1][4]}
            if previous is not None:
                self.assertTrue(endpoints <= previous)
            previous = endpoints

    def test_full_small_domain_and_nonempty_independent_oracles(self):
        with EngineSession([str(ROOT / 'bin/scaling_cpu'), '--threads', '1'],
                           'emulated', time.monotonic() + 120) as session:
            for bound, cap in ((34, 384), (34, 42), (100, 2951), (100, 42)):
                expected = wider.independent_oracle(bound, cap)
                if cap != 42:
                    self.assertTrue(expected)
                for width in wider.WIDTHS:
                    with self.subTest(bound=bound, cap=cap, width=width):
                        report, plan = wider.prepare_trial(width, bound, cap)
                        if bound == 100 and width >= 64:
                            self.assertIsNone(plan)
                            self.assertEqual(report['status'], 'incomplete_guard')
                            self.assertEqual(report['error'], 'Patch point allowance mismatch')
                            self.assertFalse(report['coverage_complete'])
                            continue
                        self.assertIsNotNone(plan, report)
                        result = wider.execute_trial(report, plan, session, expected)
                        self.assertTrue(result['coverage_complete'])
                        self.assertTrue(result['oracle_equal'])

    def test_guard_invalidates_entire_trial_and_restores_range(self):
        original = core.MAX_BOUND
        with patch.object(core, 'certify_task', side_effect=ValueError('Patch point allowance mismatch')):
            report, plan = wider.prepare_trial(128, high=True)
        self.assertIsNone(plan)
        self.assertEqual(report['status'], 'incomplete_guard')
        self.assertFalse(report['complete'])
        self.assertFalse(report['coverage_complete'])
        self.assertEqual(report['requested_patches'], 16)
        self.assertEqual(core.MAX_BOUND, original)

    def test_certificate_failure_is_not_mislabeled_as_guard(self):
        with patch.object(core, 'certify_task', side_effect=ValueError('Exact reduction certificate mismatch')):
            with self.assertRaisesRegex(ValueError, 'certificate mismatch'):
                wider.prepare_trial(16)

    def test_all_small_shells_remain_covered(self):
        for width in wider.WIDTHS:
            specs, direct = core.specs(100, 42, width)
            shells = sorted(set((s[1], s[2]) for s in specs) | set(direct))
            self.assertEqual(shells[0][0], 1)
            self.assertEqual(shells[-1][1], 100)
            for a, b in zip(shells, shells[1:]):
                self.assertEqual(a[1] + 1, b[0])
            for shell in {(s[1], s[2]) for s in specs}:
                rows = [s for s in specs if s[1:3] == shell]
                self.assertEqual(rows[0][3], (0, 1))
                self.assertEqual(rows[-1][4], (9, 10))
                for a, b in zip(rows, rows[1:]):
                    self.assertEqual(a[4], b[3])


if __name__ == '__main__':
    unittest.main()
