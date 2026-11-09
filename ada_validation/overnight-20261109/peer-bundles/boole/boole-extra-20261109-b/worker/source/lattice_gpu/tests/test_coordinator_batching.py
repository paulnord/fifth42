from dataclasses import replace
import os
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import coordinator_batching as batching
import coordinator_pipeline as pipeline
import scaling_core as core
from engine_session import EngineSession

SOURCE = Path(os.environ.get('SCALING_LATTICE_SOURCE', ROOT.parent / 'lattice_prototype'))


class SerialPool:
    def map(self, function, items, chunksize):
        return list(map(function, items))


class CoordinatorBatchingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(SOURCE)
        cls.window = pipeline.Window(64, 100, 0, 8, cap=2951)
        cls.chunks = tuple(pipeline.prepare_chunk(SerialPool(), w, 'packed')
                           for w in pipeline.partition(cls.window, 4))
        cls.tasks = tuple(task for chunk in cls.chunks for batch in chunk.plan.batches
                          for task in batch.tasks)

    def test_combines_contiguous_chunks_and_retains_full_routes(self):
        result = batching.aggregate_batches(iter(self.chunks))
        self.assertEqual(len(result.batches), 1)
        self.assertEqual(result.batches[0].tasks, self.tasks)
        self.assertEqual(result.points, sum(chunk.plan.points for chunk in self.chunks))
        routes = result.routes[0]
        for position, (task, route) in enumerate(zip(self.tasks, routes)):
            self.assertEqual(route.patch_id, task.id)
            self.assertEqual(route.chunk_index, position // 2)
            self.assertEqual(route.window, self.chunks[position // 2].window)
            self.assertEqual(route.points, task.points)
            self.assertEqual(route.certificate_sha256, self.chunks[position // 2].patches[position % 2][1])
        self.assertEqual([c.points for c in result.chunks], [c.plan.points for c in self.chunks])

    def test_descriptor_limit_splits_inside_source_chunk(self):
        result = batching.aggregate_batches(self.chunks, max_tasks=3)
        self.assertEqual([len(b.tasks) for b in result.batches], [3, 3, 2])
        self.assertEqual(tuple(t for b in result.batches for t in b.tasks), self.tasks)
        self.assertEqual([r.chunk_index for r in result.routes[0]], [0, 0, 1])
        for batch in result.batches:
            self.assertEqual(batch, core.encode_batch(batch.tasks, self.window.cap))

    def test_point_limit_and_impossible_task(self):
        limit = max(t.points for t in self.tasks)
        result = batching.aggregate_batches(self.chunks, max_points=limit)
        self.assertTrue(all(b.points <= limit for b in result.batches))
        self.assertEqual(sum(b.points for b in result.batches), result.points)
        with self.assertRaisesRegex(ValueError, 'Single task'):
            batching.aggregate_batches(self.chunks, max_points=limit - 1)

    def test_packet_byte_limit_is_exact_and_preserves_order(self):
        limit = max(len(core.encode_batch((t,), self.window.cap).packet.encode()) for t in self.tasks)
        result = batching.aggregate_batches(self.chunks, max_packet_bytes=limit)
        self.assertTrue(all(len(b.packet.encode()) <= limit for b in result.batches))
        self.assertEqual(tuple(t for b in result.batches for t in b.tasks), self.tasks)
        self.assertEqual(sum(len(r) for r in result.routes), len(self.tasks))
        with self.assertRaisesRegex(ValueError, 'byte limit'):
            batching.aggregate_batches(self.chunks, max_packet_bytes=1)

    def test_byte_prefix_search_agrees_with_greedy_encoding(self):
        full_bytes = len(core.encode_batch(self.tasks, self.window.cap).packet.encode())
        single_bytes = max(len(core.encode_batch((t,), self.window.cap).packet.encode()) for t in self.tasks)
        for limit in range(single_bytes, full_bytes + 1, 23):
            result = batching.aggregate_batches(self.chunks, max_packet_bytes=limit)
            remaining = list(self.tasks)
            expected = []
            while remaining:
                count = 1
                while count < len(remaining) and len(core.encode_batch(remaining[:count + 1], self.window.cap).packet.encode()) <= limit:
                    count += 1
                expected.append(core.encode_batch(remaining[:count], self.window.cap))
                del remaining[:count]
            self.assertEqual(result.batches, tuple(expected))

    def test_limits_cannot_enlarge_native_guards_or_accept_nonintegers(self):
        for key, ceiling in [('max_tasks', core.MAX_TASKS), ('max_points', core.MAX_POINTS),
                             ('max_packet_bytes', batching.MAX_PACKET_BYTES)]:
            for value in (0, -1, True, 1.0, ceiling + 1):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    batching.aggregate_batches(self.chunks, **{key: value})

    def test_empty_gap_duplicate_reordered_and_changed_shell_rejected(self):
        for chunks in ((), self.chunks[::2], self.chunks[::-1],
                       (self.chunks[0], self.chunks[0]),
                       (self.chunks[0], replace(self.chunks[1], window=replace(self.chunks[1].window, lo=65))),
                       (self.chunks[0], replace(self.chunks[1], window=replace(self.chunks[1].window, cap=42)))):
            with self.subTest(chunks=len(chunks)), self.assertRaises(ValueError):
                batching.aggregate_batches(chunks)

    def test_tampered_manifests_packets_and_summary_rejected(self):
        original = self.chunks[0]
        for chunk in (replace(original, patches=original.patches[:-1]),
                      replace(original, geometry_sha256='0' * 64),
                      replace(original, payload_bytes=original.payload_bytes + 1),
                      replace(original, plan=replace(original.plan, certificate_sha256='0' * 64)),
                      replace(original, plan=replace(original.plan, cap=42)),
                      replace(original, plan=replace(original.plan, points=original.plan.points + 1)),
                      replace(original, plan=replace(original.plan, batches=(replace(original.plan.batches[0], packet='bad'),)))):
            with self.subTest(chunk=chunk.geometry_sha256), self.assertRaises(ValueError):
                batching.aggregate_batches((chunk,))

    def test_native_patch_guard_retained(self):
        with patch.object(batching.night, 'native_safe', return_value=False):
            with self.assertRaisesRegex(ValueError, 'native patch guards'):
                batching.aggregate_batches(self.chunks)

    def test_exact_cpu_combined_hits_match_original_nonempty_fixture(self):
        result = batching.aggregate_batches(self.chunks, max_tasks=3)
        with EngineSession([str(ROOT / 'bin/scaling_cpu'), '--threads', '1'],
                           'emulated', time.monotonic() + 30) as session:
            expected, actual = set(), set()
            for chunk in self.chunks:
                for batch in chunk.plan.batches:
                    response, _ = session.run(batch.packet)
                    pipeline.validate_response_types(response)
                    expected.update(core.decode_batch(batch, response, session.backend))
            for batch, routes in zip(result.batches, result.routes):
                response, _ = session.run(batch.packet)
                pipeline.validate_response_types(response)
                actual.update(core.decode_batch(batch, response, session.backend))
                self.assertEqual(len(response['counts']), len(routes))
                self.assertEqual(sum(r.points for r in routes), response['points_visited'])
            self.assertIn((42, 71, 72, 2951), expected)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
