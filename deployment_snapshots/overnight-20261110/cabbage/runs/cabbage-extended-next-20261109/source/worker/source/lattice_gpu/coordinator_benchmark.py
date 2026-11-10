#!/usr/bin/env python3
"""Bounded scratch CPU/CUDA adapter; requires external ADA guard and leases."""
import argparse
from contextlib import nullcontext
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import statistics
import sys
import time
import uuid

import coordinator_pipeline as pipeline
from bounded_prefetch import BoundedPrefetch
from engine_session import EngineSession
from adapter_runtime import open_session, verify_workers, normalized_counts, normalized_hits
import overnight_search as night
import scaling_core as core

ROOT = Path(__file__).resolve().parent
MODES = ('baseline', 'fused', 'packed', 'prefetch')


class DeadlinePool:
    def __init__(self, pool, deadline):
        self.pool, self.deadline = pool, deadline

    def map(self, function, items, chunksize):
        left = self.deadline - time.monotonic()
        if left <= 0:
            raise TimeoutError('Trial preparation deadline reached')
        return self.pool.map_async(function, items, chunksize).get(timeout=left)


def source_identity(source, binary):
    paths = list(ROOT.glob('*.py')) + list((ROOT / 'src').glob('*'))
    paths += list((ROOT / 'vendor').glob('*')) + list((ROOT / 'reference').glob('*'))
    files = {'gpu/' + str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in paths if p.is_file()}
    files.update({'lattice/' + str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in source.rglob('*.py') if p.is_file()})
    files['engine_binary'] = hashlib.sha256(binary.read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def chunks(window, count):
    return tuple(pipeline.Window(window.lo, window.hi, first, min(first + count, window.last),
                                 window.width, window.bits, window.cap)
                 for first in range(window.first, window.last, count))


def run_trial(args, mode, repeat, window, source, cpus, output, fingerprint):
    started = time.perf_counter()
    deadline = time.monotonic() + args.max_seconds
    context = multiprocessing.get_context('spawn')
    trial_id = f'{repeat}-{mode}-{uuid.uuid4().hex}'
    folder = output / trial_id
    pool = context.Pool(args.workers, initializer=night.initialize, initargs=(source, cpus))
    session = None
    try:
        bounded_pool = DeadlinePool(pool, deadline)
        # Warm imports/LLL once per spawned worker. Startup is reported separately.
        warmed = {}
        while len(warmed) < args.workers:
            warmed.update(bounded_pool.map(core.worker_identity, range(args.workers * 4), 1))
        verify_workers(warmed, cpus)
        if not args.host_only:
            session = open_session(args.engine, args.backend, deadline, args.engine_threads)
        engine = pipeline.OwnedEngine(session) if session else None
        work = chunks(window, args.chunk_patches)
        pipeline.verify_partition(window, work)
        mode_prepare = 'packed' if mode in ('packed', 'prefetch') else mode
        def prepare(item):
            return pipeline.prepare_chunk(bounded_pool, item, mode_prepare, args.map_chunksize)
        reservation_bytes = 8 * 1024 * 1024
        reservation_points = core.MAX_TOTAL_POINTS
        if mode == 'prefetch':
            stream = BoundedPrefetch(work, prepare, estimate_size=lambda _: (reservation_bytes, reservation_points),
                max_outstanding=args.ready_chunks + 1, max_item_bytes=reservation_bytes,
                max_item_points=reservation_points,
                max_queued_bytes=(args.ready_chunks + 1) * reservation_bytes,
                max_queued_points=(args.ready_chunks + 1) * reservation_points,
                actual_size=lambda item: (item.payload_bytes, item.plan.points))
        else:
            stream = map(prepare, work)
        journal = (nullcontext(None) if args.host_only else
                   pipeline.TrialJournal(folder, dict(trial=trial_id, source_identity=fingerprint), window))
        rows, signatures = [], []
        stages = pipeline.Stages()
        cpu_started = time.process_time()
        startup = time.perf_counter() - started
        steady_started = time.perf_counter()
        stream_context = stream if mode == 'prefetch' else nullcontext(stream)
        with journal as writer, stream_context:
            iterator = iter(stream)
            while True:
                with stages.time('wait_for_next_prepared_chunk'):
                    try:
                        chunk = next(iterator)
                    except StopIteration:
                        break
                # Actual byte/point checks also apply to sequential controls.
                if chunk.payload_bytes > reservation_bytes or chunk.plan.points > reservation_points:
                    raise ValueError('Prepared chunk exceeds finite reservation')
                signatures.append(dict(window=chunk.window.identity(), patches=chunk.patches,
                                       geometry_sha256=chunk.geometry_sha256,
                                       certificate_sha256=chunk.plan.certificate_sha256,
                                       packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in chunk.plan.batches]))
                if engine:
                    record = pipeline.execute_chunk(chunk, engine, trial=trial_id, coordinator=0,
                                                    timeout=max(.001, deadline-time.monotonic()))
                    with stages.time('journal_write_fsync_checkpoint'):
                        writer.commit(record)
                else:
                    record = dict(hits=None, stages={}, complete=False)
                rows.append(dict(window=chunk.window.identity(), points=chunk.plan.points,
                                 preparation_stages=chunk.stages, worker_seconds=chunk.worker_seconds,
                                 consumption_stages=record['stages'], hits=record['hits'], native_batches=record.get('batches',[])))
        steady = time.perf_counter() - steady_started
        coordinator_cpu = time.process_time() - cpu_started
        queue = stream.snapshot() if mode == 'prefetch' else None
        # Startup/shutdown and expensive report formatting are not steady-state.
        shutdown_started = time.perf_counter()
        if session:
            session.close()
            session = None
        pool.close()
        pool.join()
        shutdown = time.perf_counter() - shutdown_started
        point_count = sum(row['points'] for row in rows)
        result = dict(mode=mode, repeat=repeat, trial=trial_id, window=window.identity(),
                      status='prepared_only' if args.host_only else 'exact_'+args.backend+'_verified', backend=args.backend,
                      no_full_box_claim=True, total_seconds=time.perf_counter()-started,
                      startup_seconds=startup, steady_seconds=steady, shutdown_seconds=shutdown,
                      coordinator_process_cpu_seconds=coordinator_cpu, warmed_workers=len(warmed),
                      worker_cpu_seconds=sum(x[1]+x[3] for row in rows for x in row['worker_seconds']),
                      patches=window.last-window.first, points=point_count,
                      patches_per_second=(window.last-window.first)/steady,
                      coefficient_points_per_second=point_count/steady,
                      parent_stages=stages.values, queue=queue, rows=rows,
                      signatures=signatures)
        return result
    finally:
        if session:
            session.close()
        pool.terminate()
        pool.join()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT.parent/'lattice_prototype')
    parser.add_argument('--backend', choices=('emulated','gpu'), default='emulated')
    parser.add_argument('--engine', type=Path, default=ROOT/'bin/scaling_cpu')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--lo', type=int, default=4096)
    parser.add_argument('--hi', type=int, default=8191)
    parser.add_argument('--first', type=int, default=0)
    parser.add_argument('--patches', type=int, default=256)
    parser.add_argument('--bits', type=int, default=48)
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--cap', type=int, default=42)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--engine-threads', type=int, default=1)
    parser.add_argument('--chunk-patches', type=int, default=256)
    parser.add_argument('--map-chunksize', type=int, default=8)
    parser.add_argument('--ready-chunks', type=int, default=2)
    parser.add_argument('--repeats', type=int, default=5)
    parser.add_argument('--max-seconds', type=float, default=60)
    parser.add_argument('--host-only', action='store_true', help='Do not execute an engine or claim completed coverage')
    args = parser.parse_args()
    for name, value, maximum in [('patches', args.patches, 4096), ('workers', args.workers, 16),
                                  ('engine-threads', args.engine_threads, 16), ('chunk-patches', args.chunk_patches, 256),
                                  ('ready-chunks', args.ready_chunks, 4), ('repeats', args.repeats, 5),
                                  ('map-chunksize', args.map_chunksize, 256)]:
        if not 1 <= value <= maximum:
            parser.error(f'{name} must be in [1,{maximum}]')
    if not 0 < args.max_seconds <= 120 or args.width != 8 or not 48 <= args.bits <= 256 or not 0 <= args.cap <= 1_000_000:
        parser.error('Unsupported time, width, precision, or residual limit')
    source, args.engine = args.source.resolve(), args.engine.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    window = pipeline.Window(args.lo, args.hi, args.first, args.first+args.patches, args.width, args.bits, args.cap)
    window.specifications()
    allowed = sorted(os.sched_getaffinity(0))
    if len(allowed) < args.workers:
        parser.error('Not enough allowed CPUs')
    cpus = tuple(allowed[:args.workers])
    os.sched_setaffinity(0, set(cpus))
    night.initialize(source)
    fingerprint = source_identity(source, args.engine)
    config = dict(source_identity=fingerprint, backend=args.backend, cpus=cpus, workers=args.workers,
                  engine_threads=args.engine_threads, ready_chunks=args.ready_chunks,
                  max_total_outstanding_chunks=args.ready_chunks+1, chunk_patches=args.chunk_patches,
                  map_chunksize=args.map_chunksize, repeats=args.repeats,
                  host_only=args.host_only, physical_core_topology_verified=len({(Path(f'/sys/devices/system/cpu/cpu{c}/topology/physical_package_id').read_text().strip(), Path(f'/sys/devices/system/cpu/cpu{c}/topology/core_id').read_text().strip()) for c in cpus})==len(cpus),
                  allocation='All workers, coordinator and CPU engine share this affinity set; not an ADA 16-physical-core comparison')
    night.atomic_json(args.output/'config.json', config)
    results = []
    expected = None
    try:
        for repeat in range(args.repeats):
            # Rotate order to reduce ordering bias; five repeats are not a
            # fully balanced multiple of the four candidate configurations.
            order = MODES[repeat % len(MODES):] + MODES[:repeat % len(MODES)]
            for mode in order:
                result = run_trial(args, mode, repeat, window, source, cpus, args.output, fingerprint)
                comparable = (result['signatures'], [row['hits'] for row in result['rows']])
                if expected is None:
                    expected = comparable
                elif comparable != expected:
                    raise RuntimeError('Exact geometry, packet, patch coverage or hit set changed across modes')
                results.append(result)
                night.atomic_json(args.output/f'{repeat}-{mode}.json', result)
                print(json.dumps({k:result[k] for k in ('mode','repeat','status','steady_seconds','patches_per_second')}), flush=True)
        summary = {mode:dict(median_seconds=statistics.median(r['steady_seconds'] for r in results if r['mode']==mode),
                             min_seconds=min(r['steady_seconds'] for r in results if r['mode']==mode),
                             max_seconds=max(r['steady_seconds'] for r in results if r['mode']==mode)) for mode in MODES}
        night.atomic_json(args.output/'summary.json', dict(status='passed', config=config, window=window.identity(),
                          comparisons=len(results), exact_signatures_and_hits_equal=True,
                          completed_coverage=not args.host_only, no_full_box_claim=True, modes=summary))
        return 0
    except BaseException as error:
        night.atomic_json(args.output/'failure.json', dict(status='failed', error=f'{type(error).__name__}: {error}',
                          successful_trials=len(results), no_full_box_claim=True))
        raise


if __name__ == '__main__':
    raise SystemExit(main())
