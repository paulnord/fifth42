"""A residual-load exception cannot remove lease, memory or busy-CPU blockers."""
import sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent/'worker'))
import transition_resources as t
class Resource:
    def lock_paths(self):return []
    def blockers(self,locks,running=False):return [t.IDLE_REASON,'busy lock: other job','less than 4 GiB memory available']
class TransitionTests(unittest.TestCase):
    def test_other_blockers_survive_filtering(self):
        self.assertEqual(t.FreshObservation(Resource()).blockers([]),['busy lock: other job','less than 4 GiB memory available'])
    def test_real_cpu_counter_sample_is_nonnegative_and_bounded(self):
        value=t.sample_busy_cores(.05);self.assertGreaterEqual(value,0);self.assertLessEqual(value,os_cpu_count()+1)
def os_cpu_count():
    import os
    return os.cpu_count()
if __name__=='__main__':unittest.main(verbosity=2)
