import multiprocessing as mp
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import coordinator_count_experiment as candidate
import coordinator_pipeline as pipe


class ProtocolTests(unittest.TestCase):
    def message(self, sequence, batch=0, count=1):
        return dict(identity=candidate.identity('trial', 0, sequence.parts[sequence.window_index], batch), batches=count)

    def test_exact_partition_and_fixed_boundaries(self):
        original = candidate.helpers.chunks(candidate.WINDOW, 256)
        split = pipe.partition(candidate.WINDOW, 2)
        self.assertEqual(original, tuple(c for w in split for c in candidate.helpers.chunks(w,256)))
        pipe.verify_partition(candidate.WINDOW, split)

    def test_rejects_stale_trial_coordinator_window_batch_and_type(self):
        for key, value in [('trial','old'), ('coordinator',1), ('batch',1), ('batch',False), ('window',{})]:
            seq = candidate.Sequence('trial', 0, candidate.WINDOW)
            message = self.message(seq)
            message['identity'][key] = value
            with self.assertRaises(ValueError): seq.accept(message)
            self.assertEqual(seq.window_index, 0)

    def test_rejects_duplicate_reordered_and_changed_batch_count(self):
        seq = candidate.Sequence('trial',0,candidate.WINDOW)
        first = self.message(seq, count=2)
        seq.accept(first)
        with self.assertRaises(ValueError): seq.accept(first)
        with self.assertRaises(ValueError): seq.accept(self.message(seq,batch=1,count=3))
        seq.accept(self.message(seq,batch=1,count=2))
        while not seq.finished(): seq.accept(self.message(seq))
        with self.assertRaises(ValueError): seq.accept(first)

    def test_leaf_initializer_uses_last_identity_and_retains_guards(self):
        process = type('Process', (), {'_identity': (17,2)})()
        with patch.object(candidate.mp,'current_process',return_value=process), \
             patch.object(candidate.exact_host_opt,'initialize') as initialize, \
             patch.object(candidate.os,'sched_setaffinity') as affinity:
            candidate.leaf_initialize('/source', (10,11))
            initialize.assert_called_once_with('/source', (), 'combined')
            affinity.assert_called_once_with(0,{11})

    def test_response_identity_rejected_before_acceptance(self):
        class Connection:
            def send(self, item): self.sent=item
            def poll(self, timeout): return True
            def recv(self): return dict(kind='result', identity=dict(self.sent['identity'], trial='old'))
        batch=type('Batch',(),{'packet':'exact'})()
        plan=type('Plan',(),{'batches':(batch,)})()
        chunk=type('Chunk',(),{'plan':plan,'window':candidate.WINDOW})()
        engine=candidate.RemoteEngine(Connection(),'trial',0,chunk,float('inf'))
        with self.assertRaises(ValueError): engine.run('exact')
        self.assertEqual(engine.index,0)


if __name__ == '__main__': unittest.main()
