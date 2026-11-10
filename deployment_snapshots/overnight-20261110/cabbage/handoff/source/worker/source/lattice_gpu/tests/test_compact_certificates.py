from dataclasses import replace
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'lattice_gpu'))
import compact_certificate_opt as compact
import coordinator_pipeline as pipeline
import packing_opt
import scaling_core as core


class SerialPool:
    def map(self, function, values, chunksize):
        return list(map(function, values))


class CompactCertificates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(Path(os.environ.get('SCALING_LATTICE_SOURCE', ROOT / 'lattice_prototype')))

    def task(self):
        return core.prepare_task(pipeline.Window(64, 100, 0, 1, cap=2951).specifications()[0])

    def test_round_trip_all_fields_and_canonical_certificate(self):
        task = self.task()
        recovered = compact.decode_task(compact.encode_task(task))
        self.assertEqual(task, recovered)
        self.assertEqual(packing_opt.task_payload(task), packing_opt.task_payload(recovered))
        self.assertEqual(core.certify_task(task), core.certify_task(recovered))

    def test_existing_packed_plan_and_geometry_unchanged(self):
        window = pipeline.Window(64, 100, 0, 8, cap=2951)
        baseline = pipeline.prepare_chunk(SerialPool(), window, 'packed')
        result = compact.prepare_chunk(SerialPool(), window)
        for field in ('window', 'plan', 'patches', 'geometry_sha256', 'payload_bytes'):
            self.assertEqual(getattr(result, field), getattr(baseline, field))
        pipeline.validate_chunk(result)

    def test_corruption_and_malformed_input_rejected(self):
        blob = compact.encode_task(self.task())
        for bad in (b'', blob[:-1], blob + b'x', b'FAIL' + blob[4:],
                    blob[:4] + b'\0' + blob[5:], blob[:-1] + b'\xff',
                    blob[:5] + b'\xff' * 4 + blob[9:], bytearray(blob)):
            with self.assertRaises(ValueError):
                compact.decode_task(bad)

    def test_changed_transport_cannot_bypass_certificate_or_spec_binding(self):
        window = pipeline.Window(64, 100, 0, 1, cap=2951)
        original = compact.prepare_certified_compact
        for field, delta in (('id', 1), ('points', 2)):
            def corrupt(spec):
                blob, token, timings = original(spec)
                task = compact.decode_task(blob)
                return compact.encode_task(replace(task, **{field: getattr(task, field) + delta})), token, timings
            with patch.object(compact, 'prepare_certified_compact', side_effect=corrupt):
                with self.assertRaises(ValueError):
                    compact.prepare_chunk(SerialPool(), window)

    def test_native_guard_and_total_allowance_preserved(self):
        window = pipeline.Window(64, 100, 0, 1, cap=2951)
        with patch.object(pipeline.night, 'native_safe', return_value=False):
            with self.assertRaises(pipeline.GuardedPatch):
                compact.prepare_chunk(SerialPool(), window)
        with patch.object(core, 'MAX_TOTAL_POINTS', 1):
            with self.assertRaises(ValueError):
                compact.prepare_chunk(SerialPool(), window)


if __name__ == '__main__':
    unittest.main()
