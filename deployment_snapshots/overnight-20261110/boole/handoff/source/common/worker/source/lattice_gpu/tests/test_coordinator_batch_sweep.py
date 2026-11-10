import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import coordinator_batch_sweep as sweep
import coordinator_batching as batching
import coordinator_pipeline as p
import scaling_core as core
from engine_session import EngineSession


class SerialPool:
    def map(self,f,items,chunksize):return list(map(f,items))


class AggregatedExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(Path(os.environ.get('SCALING_LATTICE_SOURCE',ROOT.parent/'lattice_prototype')))

    def test_cross_chunk_native_packet_retains_exact_hits_and_checkpoint_boundaries(self):
        window=p.Window(64,100,0,8,cap=2951)
        chunks=tuple(p.prepare_chunk(SerialPool(),w,'packed') for w in p.partition(window,2))
        plan=batching.aggregate_batches(chunks,max_tasks=6)
        with EngineSession([str(ROOT/'bin/scaling_cpu'),'--threads','2'],'emulated',time.monotonic()+20) as session:
            records,timings=sweep.execute_aggregated(plan,chunks,p.OwnedEngine(session),'test',time.monotonic()+20)
        self.assertEqual(len(timings['packets']),2)
        self.assertEqual([len(r['patches']) for r in records],[4,4])
        expected=core.lattice().direct_positive(64,100,lambda _:2951,lambda r,c:abs(r)<=2951)
        self.assertIn((42,71,72,2951),expected)
        self.assertEqual({tuple(h) for r in records for h in r['hits']},expected)
        with tempfile.TemporaryDirectory() as folder:
            with p.TrialJournal(folder,dict(trial='test',source_identity='fixed'),window) as journal:
                journal.commit(records[0]);self.assertEqual(journal.state['next_patch'],4)
                journal.commit(records[1]);self.assertEqual(journal.state['next_patch'],8)
                self.assertEqual(journal.state['chunks'],2)

    def test_incomplete_aggregate_never_returns_committable_records(self):
        chunk=p.prepare_chunk(SerialPool(),p.Window(64,100,0,8,cap=2951),'packed')
        plan=batching.aggregate_batches((chunk,),max_tasks=4)
        class Broken:
            backend='emulated'
            def run(self,*args,**kwargs):return dict(box_complete=False),0
        with self.assertRaises(ValueError):sweep.execute_aggregated(plan,(chunk,),Broken(),'test',time.monotonic()+10)


if __name__=='__main__':unittest.main()
