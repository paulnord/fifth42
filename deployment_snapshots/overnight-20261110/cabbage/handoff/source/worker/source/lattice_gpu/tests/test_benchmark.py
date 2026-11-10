"""Coverage and resource boundaries of the separate larger CUDA benchmark."""
import copy
import fcntl
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import benchmark as bench

class LargerBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.work=Path(self.temp.name)
        (self.work/'model.py').write_text((ROOT/'model.py').read_text())
        for name in ('UPSTREAM.json','reference/lattice5.py','reference/COVERAGE.md','vendor/exact.hpp'):
            target=self.work/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((ROOT/name).read_bytes())
        self.model=bench.expanded_model(self.work)

    def tearDown(self):
        self.temp.cleanup()

    def test_extended_domains_have_complete_adjacent_shells_with_finite_limits(self):
        for bound in (2000,4000,8000):
            specs,direct=self.model.expected_specs(bound,'constant',42,2)
            intervals=sorted(set((s[0],s[1]) for s in specs).union(map(tuple,direct)))
            self.assertEqual(intervals[0][0],1)
            self.assertEqual(intervals[-1][1],bound)
            for left,right in zip(intervals,intervals[1:]):
                self.assertEqual(left[1]+1,right[0])
            self.assertLessEqual(len(specs),4096)
        self.assertEqual(self.model.MAX_POINTS,50_000_000)
        self.assertEqual(self.model.MAX_PATCH_POINTS,10_000_000)
        for invalid in (0,8001,True):
            with self.assertRaises(ValueError):self.model.expected_specs(invalid,'constant',42,2)
        # The original validated source still rejects 1001.
        original=bench.load_module('original_gpu_model_for_test',self.work/'model.py')
        with self.assertRaises(ValueError):original.expected_specs(1001,'constant',42,2)

    def test_extended_profile_rejects_missing_counts_and_tampered_transforms(self):
        plan=self.model.make_plan(4)
        self.assertTrue(self.model.verify_plan(plan))
        bad=copy.deepcopy(plan);bad['tasks'][0]['U'][0][0]+=1
        with self.assertRaises(ValueError):self.model.verify_plan(bad)
        output=dict(backend='gpu',box_complete=True,points_visited=plan['points'],counts=[],hits=[])
        with self.assertRaises(ValueError):self.model.decode(plan,output,'gpu')

    def test_busy_cpu_lease_does_not_hold_the_gpu_lease(self):
        class Guard:
            PRODUCTION=self.work
            @staticmethod
            def lock_paths():return []
            @staticmethod
            def blockers(paths):return []
        old_cpu,old_gpu=bench.CPU_ROOT,bench.SOURCE_ROOT
        bench.CPU_ROOT=self.work;bench.SOURCE_ROOT=self.work
        try:
            with (self.work/'cpu-benchmark.lock').open('a+') as cpu:
                fcntl.flock(cpu,fcntl.LOCK_EX|fcntl.LOCK_NB)
                with self.assertRaises(RuntimeError):bench.acquire_leases(Guard(),False)
                with (self.work/'validation.lock').open('a+') as gpu:
                    fcntl.flock(gpu,fcntl.LOCK_EX|fcntl.LOCK_NB)
        finally:
            bench.CPU_ROOT=old_cpu;bench.SOURCE_ROOT=old_gpu

if __name__=='__main__':unittest.main(verbosity=2)
