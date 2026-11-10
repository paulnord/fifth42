"""CPU-only failure injection for the shared-memory GPU preparation service.

The real spawn workers construct one ordinary patch.  A CPU stub replaces the
GPU backend before GPUStage.start(), so this test creates no CUDA context.
"""
import argparse
import hashlib
import io
import json
import multiprocessing as mp
from multiprocessing import shared_memory
import os
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

import gpu_preparation as gp

ROOT = Path(__file__).resolve().parent
ARGUMENT = (100000000001, 200000000000, 2572492928, 2572492932,
            222, 42, 'adaptive')
RECORDS = []


class RaisingCPUBackend:
    """Expose the GPU API while never loading its shared library."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.calls = 0
        self.closed = False

    def reduce_flat(self, values, count, *, raw=False):
        assert raw and count == 1 and values.shape == (1, 18)
        self.calls += 1
        raise RuntimeError('Injected CPU-only GPU service failure')

    def close(self):
        self.closed = True


def require_unlinked(test, names):
    for name in names:
        try:
            unexpected = shared_memory.SharedMemory(name=name)
        except FileNotFoundError:
            continue
        unexpected.close()
        test.fail(f'Shared memory was not unlinked: {name}')


class FakeWorker:
    def __init__(self, pid, alive=True):
        self.pid, self.alive = pid, alive

    def is_alive(self):
        return self.alive


class ControlledPending:
    def __init__(self, pool):
        self.pool = pool
        self.waits = 0

    def ready(self):
        return False

    def wait(self, timeout):
        self.waits += 1
        if self.pool.change == 'replacement':
            self.pool._pool = [FakeWorker(987654322)]
        else:
            self.pool._pool[0].alive = False

    def get(self):
        raise AssertionError('A failed worker must never return Tasks')


class ControlledPool:
    def __init__(self, change):
        self.change = change
        self._pool = [FakeWorker(987654321)]
        self.pending = ControlledPending(self)

    def map_async(self, function, blocks, chunksize):
        assert function is gp.prepare_block
        assert blocks == [[ARGUMENT]] and chunksize == 1
        return self.pending


class FailureInjectionTests(unittest.TestCase):
    def test_real_spawn_service_failure_is_explicit_and_bounded(self):
        started = time.monotonic()
        stage = gp.GPUStage(2, capacity=4)
        names = [memory.name for memory in stage.memory]
        pool = None
        processes = []
        result = None
        error = None
        dispatch_seconds = None
        try:
            cpus = tuple(sorted(os.sched_getaffinity(0)))
            pool = mp.get_context('spawn').Pool(
                2, initializer=gp.initialize,
                initargs=stage.initargs(ROOT/'worker/source/lattice_prototype', cpus))
            processes = list(pool._pool)
            warmed = set()
            while len(warmed) < 2:
                self.assertLess(time.monotonic()-started, 4.)
                rows = pool.map_async(gp.core.worker_identity, range(4), 1).get(timeout=2)
                warmed.update(row[0] for row in rows)
            with patch.object(gp.candidate, 'GPUCandidates', RaisingCPUBackend):
                stage.start()
            dispatch_started = time.monotonic()
            try:
                result = stage.dispatch(pool, [ARGUMENT])
            except RuntimeError as exc:
                error = str(exc)
            dispatch_seconds = time.monotonic()-dispatch_started
            self.assertIsNone(result, 'Service failure returned an admitted Task')
            self.assertIsNotNone(error, 'Service failure was silently accepted')
            self.assertIn('GPU preparation service failed', error)
            self.assertLess(dispatch_seconds, 5.)
            self.assertIsInstance(stage.error, RuntimeError)
            self.assertEqual(str(stage.error), 'Injected CPU-only GPU service failure')
            self.assertEqual(stage.gpu.calls, 1)
            self.assertEqual(stage.metrics['accepted'], 0)
            self.assertEqual(stage.metrics['fallbacks'], {})
            self.assertTrue(all(event.is_set() for event in stage.events))
        finally:
            if pool is not None:
                pool.terminate()
                pool.join()
            stage.close()
        require_unlinked(self, names)
        self.assertTrue(all(not process.is_alive() for process in processes))
        self.assertFalse(stage.thread.is_alive())
        self.assertTrue(stage.gpu.closed)
        elapsed = time.monotonic()-started
        self.assertLess(elapsed, 5., 'Startup, error propagation and cleanup exceeded bound')
        RECORDS.append(dict(test='real_spawn_service_failure', status='passed',
            segment=ARGUMENT, expected_error=error, injected_error=str(stage.error),
            dispatch_seconds=dispatch_seconds, startup_dispatch_cleanup_seconds=elapsed,
            returned_tasks=False, gpu_backend='raising CPU-only stub',
            worker_pids=[process.pid for process in processes],
            worker_exitcodes=[process.exitcode for process in processes],
            workers_joined=True, service_thread_joined=True, backend_closed=True,
            shared_memory_names=names, shared_memory_unlinked=True))

    def check_worker_failure(self, change):
        started = time.monotonic()
        stage = gp.GPUStage(1, capacity=1)
        names = [memory.name for memory in stage.memory]
        controlled = ControlledPool(change)
        result = None
        error = None
        try:
            try:
                result = stage.dispatch(controlled, [ARGUMENT])
            except RuntimeError as exc:
                error = str(exc)
            self.assertIsNone(result)
            self.assertEqual(error, 'Preparation worker died or was replaced')
            self.assertEqual(controlled.pending.waits, 1)
            self.assertIsNone(stage.gpu, 'Worker failure test created a GPU backend')
        finally:
            stage.close()
        require_unlinked(self, names)
        elapsed = time.monotonic()-started
        self.assertLess(elapsed, 5.)
        RECORDS.append(dict(test='controlled_worker_'+change, status='passed',
            expected_error=error, startup_dispatch_cleanup_seconds=elapsed,
            returned_tasks=False, gpu_backend_created=False,
            shared_memory_names=names, shared_memory_unlinked=True))

    def test_worker_pid_replacement_is_detected(self):
        self.check_worker_failure('replacement')

    def test_worker_death_is_detected(self):
        self.check_worker_failure('death')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evidence/service-failure.json')
    args = parser.parse_args()
    allowed = os.sched_getaffinity(0)
    selected = allowed.intersection({4, 5})
    if not selected:
        selected = set(sorted(allowed)[:2])
    os.sched_setaffinity(0, selected)
    logs = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FailureInjectionTests)
    result = unittest.TextTestRunner(stream=logs, verbosity=2).run(suite)
    report = dict(status='passed' if result.wasSuccessful() else 'failed', TEST_ONLY=True,
        GPU_used=False, production_modified=False, production_restarted=False,
        cpu_affinity=sorted(selected), tests_run=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), results=RECORDS,
        command=[sys.executable, str(Path(__file__).resolve()), '--output', str(args.output)],
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
            for name in ('test_service_failure.py', 'gpu_preparation.py')},
        unittest_log=logs.getvalue())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(logs.getvalue(), end='')
    print(json.dumps(dict(status=report['status'], tests_run=result.testsRun,
                         evidence=str(args.output))))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
