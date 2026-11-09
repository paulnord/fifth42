import dataclasses,os,time,unittest
from pathlib import Path
from types import SimpleNamespace
import buffered_pipeline as b
import scheduling as s
import runtime_initialize,coordinator_pipeline as pipeline,width_coverage as coverage
ROOT=Path(__file__).resolve().parent
class Serial:
    def map(self,fn,args,chunksize):return list(map(fn,args))
class SchedulingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):runtime_initialize.initialize(ROOT/'worker/source/lattice_prototype')
    def test_multiwindow_same_certificates_geometry_packets_and_order(self):
        windows=[pipeline.Window(100000000001,200000000000,4398843264+i*256,4398843520+i*256,8,222,42,'adaptive') for i in range(4)]
        chunks=list(s.prepare_many(Serial(),windows,2,True))
        for window,chunk in zip(windows,chunks):
            reference=coverage.prepare_chunk(Serial(),window,2);b.validate_cached(chunk);pipeline.validate_chunk(chunk)
            self.assertEqual(reference.plan,chunk.plan);self.assertEqual(reference.patches,chunk.patches);self.assertEqual(reference.window,chunk.window)
            self.assertEqual(reference.geometry_sha256,chunk.geometry_sha256)
    def test_source_is_lazy_and_consumption_stays_bounded(self):
        consumed=[]
        def source():
            for number in range(10**12):
                self.assertLess(len(consumed),32,'Source was eagerly exhausted')
                consumed.append(number);yield number
        def prepare(windows):
            for number in windows:yield SimpleNamespace(number=number,payload_bytes=1,plan=SimpleNamespace(points=1))
        q=s.ReadyQueue(source(),prepare,batch=2,ready_limit=1,active_limit=1)
        self.assertEqual(consumed,[])
        with q:
            for expected in range(5):
                chunk=q.get();self.assertEqual(chunk.number,expected);q.ack(chunk)
            time.sleep(.01)
            self.assertLessEqual(len(consumed)-5,q.max_outstanding+q.batch)
        self.assertFalse(q.thread.is_alive())
    def test_lazy_partial_last_batch_preserves_order(self):
        def prepare(windows):
            for number in windows:yield SimpleNamespace(number=number,payload_bytes=1,plan=SimpleNamespace(points=1))
        got=[]
        with s.ReadyQueue(iter(range(7)),prepare,batch=4,ready_limit=1) as q:
            for chunk in q:got.append(chunk.number);q.ack(chunk)
        self.assertEqual(got,list(range(7)))
    def test_ready_depth_bounds_order_and_wait_accounting(self):
        def prepare(windows):
            for number in windows:yield SimpleNamespace(number=number,payload_bytes=100,plan=SimpleNamespace(points=20))
        q=s.ReadyQueue(range(10),prepare,batch=2,ready_limit=1,active_limit=1,max_item_bytes=100,max_item_points=20)
        got=[]
        with q:
            time.sleep(.02)
            for chunk in q:got.append(chunk.number);q.ack(chunk);time.sleep(.001)
            snap=q.snapshot()
        self.assertEqual(got,list(range(10)));self.assertEqual(snap['peak_ready'],1)
        self.assertLessEqual(snap['peak_outstanding'],4);self.assertEqual(snap['outstanding'],0)
        self.assertGreater(snap['producer_wait_full_seconds'],.001);self.assertGreater(snap['mean_ready_depth'],0)
        self.assertEqual(q.snapshot()['outstanding'],0)
    def test_active_buffers_are_reserved_until_explicit_release(self):
        def prepare(windows):
            for number in windows:yield SimpleNamespace(number=number,payload_bytes=1,plan=SimpleNamespace(points=1))
        q=s.ReadyQueue(range(4),prepare,batch=1,ready_limit=1,active_limit=3)
        with q:
            chunks=[q.get() for _ in range(3)];self.assertEqual(q.snapshot()['active'],3)
            for chunk in chunks:q.ack(chunk)
            with self.assertRaises(ValueError):q.ack(chunks[0])
    def test_failure_and_size_limit_propagate_without_deadlock(self):
        def fail(windows):raise RuntimeError('worker failed');yield
        with s.ReadyQueue([0],fail) as q:
            with self.assertRaises(RuntimeError):q.get()
        def huge(windows):yield SimpleNamespace(payload_bytes=100,plan=SimpleNamespace(points=20))
        with s.ReadyQueue([0],huge,max_item_bytes=50) as q:
            with self.assertRaises(ValueError):q.get()
    def test_incomplete_preparation_batch_rejected(self):
        def incomplete(windows):yield SimpleNamespace(payload_bytes=1,plan=SimpleNamespace(points=1))
        with s.ReadyQueue([0,1],incomplete,batch=2) as q:
            item=q.get();q.ack(item)
            with self.assertRaises(ValueError):q.get()
if __name__=='__main__':unittest.main(verbosity=2)
