from pathlib import Path
import sys
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bounded_prefetch import BoundedPrefetch, PrefetchLimitError


class BoundedPrefetchTests(unittest.TestCase):
    def stream(self, items=range(10), prepare=lambda x: x, **kwargs):
        options = dict(estimate_size=lambda _: (4, 2), max_outstanding=3,
                       max_item_bytes=8, max_item_points=4,
                       max_queued_bytes=12, max_queued_points=6)
        options.update(kwargs)
        return BoundedPrefetch(items, prepare, **options)

    def wait_for(self, predicate):
        deadline = time.monotonic() + 2
        while not predicate():
            if time.monotonic() > deadline:
                self.fail("timed out waiting for worker")
            time.sleep(.001)

    def test_order_and_single_background_worker(self):
        threads = []
        def prepare(i):
            threads.append(threading.get_ident())
            time.sleep(.001 if i % 2 else .003)
            return i * 2
        with self.stream(prepare=prepare) as stream:
            self.assertEqual(list(stream), list(range(0, 20, 2)))
        self.assertEqual(len(set(threads)), 1)
        self.assertNotEqual(threads[0], threading.get_ident())

    def test_outstanding_includes_consumer_and_inflight(self):
        entered = threading.Event()
        release = threading.Event()
        def prepare(i):
            if i == 2:
                entered.set()
                release.wait(2)
            return i
        with self.stream(prepare=prepare) as stream:
            self.assertEqual(next(stream), 0)
            self.assertTrue(entered.wait(2))
            self.assertEqual(stream.snapshot()['outstanding'], 3)
            self.assertEqual(stream.snapshot()['reserved_bytes'], 12)
            release.set()
            self.assertEqual(list(stream), list(range(1, 10)))
        self.assertEqual(stream.snapshot()['peak_outstanding'], 3)
        self.assertEqual(stream.snapshot()['outstanding'], 0)

    def test_aggregate_reservation_before_preparation(self):
        prepared = []
        with self.stream(prepare=lambda i: prepared.append(i) or i,
                         max_outstanding=8, max_queued_bytes=8,
                         max_queued_points=4) as stream:
            self.wait_for(lambda: len(prepared) == 2)
            self.assertEqual(next(stream), 0)
            time.sleep(.01)
            self.assertEqual(prepared, [0, 1])
            self.assertEqual(list(stream), list(range(1, 10)))
        self.assertEqual(stream.snapshot()['peak_outstanding'], 2)
        self.assertEqual(stream.snapshot()['peak_reserved_bytes'], 8)
        self.assertEqual(stream.snapshot()['peak_reserved_points'], 4)

    def test_ordered_prepare_failure(self):
        def prepare(i):
            if i == 2:
                raise RuntimeError('failed 2')
            return i
        with self.stream(prepare=prepare) as stream:
            self.assertEqual(next(stream), 0)
            self.assertEqual(next(stream), 1)
            with self.assertRaisesRegex(RuntimeError, 'failed 2'):
                next(stream)
            with self.assertRaises(StopIteration):
                next(stream)

    def test_ordered_source_failure(self):
        def source():
            yield 0
            raise RuntimeError('source failed')
        with self.stream(items=source()) as stream:
            self.assertEqual(next(stream), 0)
            with self.assertRaisesRegex(RuntimeError, 'source failed'):
                next(stream)

    def test_oversized_items_never_prepare(self):
        for size in [(9, 1), (1, 5), (7, 1)]:
            called = []
            with self.subTest(size=size), self.stream(
                    prepare=called.append, estimate_size=lambda _: size,
                    max_queued_bytes=6) as stream:
                with self.assertRaises(PrefetchLimitError):
                    next(stream)
            self.assertEqual(called, [])

    def test_actual_size_cannot_exceed_reservation(self):
        with self.stream(actual_size=lambda _: (5, 2)) as stream:
            with self.assertRaisesRegex(PrefetchLimitError, 'reservation'):
                next(stream)
        self.assertEqual(stream.snapshot()['outstanding'], 0)

    def test_close_full_queue(self):
        stream = self.stream()
        stream.__enter__()
        self.wait_for(lambda: stream.snapshot()['outstanding'] == 3)
        closer = threading.Thread(target=stream.close, daemon=True)
        closer.start()
        closer.join(2)
        self.assertFalse(closer.is_alive())
        self.assertEqual(stream.snapshot()['outstanding'], 0)
        self.assertEqual(list(stream), [])
        stream.close()

    def test_cooperative_cancel_inflight(self):
        entered = threading.Event()
        def prepare(i):
            entered.set()
            stream.cancel_event.wait(2)
            return i
        stream = self.stream(prepare=prepare)
        stream.__enter__()
        self.assertTrue(entered.wait(2))
        stream.close()
        self.assertEqual(stream.snapshot()['outstanding'], 0)
        self.assertEqual(list(stream), [])

    def test_empty_and_single_slot(self):
        with self.stream(items=[]) as stream:
            self.assertEqual(list(stream), [])
        with self.stream(max_outstanding=1) as stream:
            self.assertEqual(list(stream), list(range(10)))
            self.assertEqual(stream.snapshot()['peak_outstanding'], 1)

    def test_invalid_sizes_and_limits(self):
        with self.assertRaises(ValueError):
            self.stream(max_outstanding=0)
        for size in [(-1, 0), (True, 2), (1.1, 2), (1,), None]:
            with self.subTest(size=size), self.stream(
                    estimate_size=lambda _: size) as stream:
                with self.assertRaises(PrefetchLimitError):
                    next(stream)


if __name__ == '__main__':
    unittest.main()
