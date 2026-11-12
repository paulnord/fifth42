"""TEST_ONLY: compare CPU dispatch policies with unchanged certified packets."""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import math
import multiprocessing as mp
import os
import random
import signal
import statistics
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import pipeline_bench as base


class MeasuredPool:
    """Map time includes worker execution, IPC and parent deserialization."""
    def __init__(self, pool, deadline, chunksize):
        self.pool, self.deadline, self.chunksize = pool, deadline, chunksize
        self.calls = self.segments = 0
        self.wall_seconds = 0.

    def map(self, function, items, ignored=8):
        items = list(items)
        began = time.perf_counter()
        self.calls += 1
        self.segments += len(items)
        try:
            return self.pool.map_async(function, items, self.chunksize).get(
                timeout=min(25, base.remaining(self.deadline)))
        finally:
            self.wall_seconds += time.perf_counter() - began


def run_trial(pool, engine, selected, args, repeat, batch_windows, chunksize,
              deadline, output, source_identity, binary_hash):
    tag = f"windows-{batch_windows}-chunks-{chunksize}-repeat-{repeat}"
    originals = [base.pipeline.Window(**rows[0]["window"]) for rows in selected]
    expected = {json.dumps(rows[0]["window"], sort_keys=True): rows for rows in selected}
    windows = originals * args.passes
    regions = []
    for window in originals:
        if not regions or regions[-1][-1].last != window.first:
            regions.append([])
        regions[-1].append(window)
    journals, identities, journal_for = [], [], {}
    stages = dict(prepare_worker_wall_seconds=0., prepare_worker_cpu_seconds=0.,
                  certify_worker_wall_seconds=0., certify_worker_cpu_seconds=0.,
                  prepared_consistency_seconds=0., engine_rpc_seconds=0.,
                  exact_verification_seconds=0., kernel_seconds=0., journal_accept_seconds=0.)
    setup = time.perf_counter()
    for pass_index in range(args.passes):
        for region_index, group in enumerate(regions):
            first, last = group[0], group[-1]
            whole = base.coverage.Window(first.lo, first.hi, first.first, last.last,
                                         first.width, first.bits, first.cap, first.geometry_policy, 2)
            identity = dict(trial=f"{tag}-pass-{pass_index}", TEST_ONLY=True,
                            source_identity=source_identity, binary_sha256=binary_hash,
                            workers=args.workers, preparation_batch_windows=batch_windows,
                            map_chunksize=chunksize, replay_pass=pass_index)
            directory = output / tag / f"pass-{pass_index}" / f"region-{region_index}"
            journal = base.buffering.BufferedJournal(directory, identity, whole, records=8)
            journals.append(journal)
            identities.append((directory, identity, whole))
            for window in group:
                journal_for[(pass_index, json.dumps(window.identity(), sort_keys=True))] = journal
    setup_seconds = time.perf_counter() - setup

    measured_pool = MeasuredPool(pool, deadline, chunksize)
    def prepare_many(group):
        base.remaining(deadline)
        yield from base.scheduling.prepare_many(measured_pool, group, 2, cache=True)

    # The frozen scheduler uses ready_limit=1 for multiwindow batches. Report
    # this derived behavior rather than claiming queue depth is held identical.
    stream = base.scheduling.BulkStream(windows, prepare_many, batch_windows=batch_windows,
                                       ready_limit=2, max_item_bytes=12 * 1024**2)
    points = requests = completed = 0
    began = time.perf_counter()
    try:
        with stream:
            for chunk in stream:
                base.remaining(deadline)
                base.require(completed < len(windows) and
                             chunk.window.identity() == windows[completed].identity(),
                             "Original window visits were omitted, duplicated or reordered")
                pass_index = completed // len(originals)
                key = json.dumps(chunk.window.identity(), sort_keys=True)
                checked = time.perf_counter()
                base.check_prepared(chunk, expected[key])
                stages["prepared_consistency_seconds"] += time.perf_counter() - checked
                journal = journal_for[(pass_index, key)]
                record = base.pipeline.execute_chunk(
                    chunk, engine, trial=journal.identity["trial"], coordinator=0,
                    timeout=min(30, base.remaining(deadline)))
                base.coverage.add_coverage(record, chunk, 2)
                for row in chunk.worker_seconds:
                    for index, name in enumerate(("prepare_worker_wall_seconds", "prepare_worker_cpu_seconds",
                                                  "certify_worker_wall_seconds", "certify_worker_cpu_seconds")):
                        stages[name] += row[index]
                for name, target in (("prepared_plan_consistency", "prepared_consistency_seconds"),
                                     ("engine_rpc", "engine_rpc_seconds"),
                                     ("exact_output_verification", "exact_verification_seconds")):
                    stages[target] += record["stages"][name]["wall_seconds"]
                checked = time.perf_counter()
                for receipt, row, batch in zip(record["batches"], expected[key], chunk.plan.batches):
                    expected_counts = [(task.id, count["expected"], count["visited"])
                                       for task, count in zip(batch.tasks, row["expected"]["counts"])]
                    expected_hits = sorted((batch.tasks[hit["task"]].id, hit["linear"], hit["a"], hit["b"], hit["c"])
                                           for hit in row["expected"]["hits"])
                    base.require(receipt["native_counts"] == expected_counts and
                                 receipt["native_hit_records"] == expected_hits,
                                 "Timed counts/hits differ from independent GMP")
                    stages["kernel_seconds"] += receipt.get("kernel_seconds") or 0.
                stages["exact_verification_seconds"] += time.perf_counter() - checked
                checked = time.perf_counter()
                journal.commit(record)
                stages["journal_accept_seconds"] += time.perf_counter() - checked
                points += chunk.plan.points
                requests += len(chunk.plan.batches)
                completed += 1
                stream.ack(chunk)
            queue_metrics = stream.snapshot()
        checked = time.perf_counter()
        for journal in journals:
            journal.close()
        stages["journal_close_seconds"] = time.perf_counter() - checked
        elapsed = time.perf_counter() - began
    finally:
        for journal in journals:
            if not journal.lock.closed:
                journal.close()
    recovery = time.perf_counter()
    for directory, identity, whole in identities:
        reopened = base.buffering.BufferedJournal(directory, identity, whole, records=8)
        try:
            base.require(reopened.state["next_patch"] == whole.last and
                         reopened.state["completed_bound"] is None, "Incomplete durable replay pass")
        finally:
            reopened.close()
    recovery_seconds = time.perf_counter() - recovery
    base.require(completed == 9 * args.passes and requests == 23 * args.passes and
                 points == 775687194 * args.passes, "Incomplete repeated-input workload")
    base.require(measured_pool.calls == math.ceil(len(windows) / batch_windows) and
                 measured_pool.segments == 128 * len(windows), "CPU dispatch omitted or duplicated segments")
    base.require(queue_metrics["peak_reserved_bytes"] <= 48 * 1024**2,
                 "Prepared objects exceed the common 48 MiB reservation ceiling")
    return dict(variant=f"windows-{batch_windows}-chunks-{chunksize}", repeat=repeat,
                workers=args.workers, preparation_batch_windows=batch_windows, map_chunksize=chunksize,
                replay_passes=args.passes, unique_windows=9, window_visits=completed, requests=requests,
                unique_logical_cells=2304, logical_cell_visits=2304 * args.passes,
                verified_positions=points, pipeline_seconds=elapsed,
                logical_cell_visits_per_second=2304 * args.passes / elapsed,
                stages=stages, queue=queue_metrics,
                dispatch=dict(calls=measured_pool.calls, submitted_segments=measured_pool.segments,
                              map_wall_seconds=measured_pool.wall_seconds),
                journal_setup_seconds=setup_seconds,
                journal_flush_seconds=sum(journal.flush_seconds for journal in journals),
                journal_flush_count=sum(journal.flush_count for journal in journals),
                durable_recovery_seconds=recovery_seconds, durable_recovery_passed=True,
                regenerated_packet_bytes_match=True)


def main(args):
    start = time.monotonic()
    deadline = start + args.max_seconds
    def alarm(signum, frame):
        raise TimeoutError("Overall batching benchmark deadline reached")
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, args.max_seconds)
    report = dict(status="running", TEST_ONLY=True, new_scientific_coverage=False,
                  backend=args.backend, hardware=base.replay.hardware(), trials=[], workers=args.workers,
                  replay_passes=args.passes, repetitions=args.repeats,
                  compute_units_per_hour_observed_by_user=args.units_per_hour,
                  limitations="Repeated-input local pipeline policy comparison. Queue behavior changes with batching under the frozen scheduler. Map time includes computation, IPC and deserialization, not isolated serialization cost. Network/remote mirrors and production GMP audit cadence are excluded. No new scientific coverage.")
    target = ROOT / "results/batching-benchmark.json"
    pool = None
    try:
        base.require(args.workers <= max(1, len(os.sched_getaffinity(0)) - 1),
                     "Insufficient CPU affinity for requested workers plus coordinator")
        rows, selected, metadata = base.load_inputs(9)
        provenance = json.loads((ROOT / "pipeline/SOURCE_PROVENANCE.json").read_text())
        for name, expected in provenance["files_byte_identical_to_frozen_worker"].items():
            base.require(base.digest(ROOT / "pipeline" / name) == expected, "Frozen planner source changed")
        report["packet_export_sha256"] = metadata["packet_file_sha256"]
        report["planner_source_identity"] = base.digest(ROOT / "pipeline/SOURCE_PROVENANCE.json")
        report["base_pipeline_runner_sha256"] = base.digest(ROOT / "pipeline/pipeline_bench.py")
        base.require(report["base_pipeline_runner_sha256"] == "60e750ef9988075fa297812a14f0adc659da1f8176d10f98ba3b22d1f68d3e77",
                     "Original validated pipeline runner changed")
        report["batching_runner_sha256"] = base.digest(__file__)
        source_identity = hashlib.sha256(json.dumps({key: report[key] for key in
            ("planner_source_identity", "base_pipeline_runner_sha256", "batching_runner_sha256")},
            sort_keys=True).encode()).hexdigest()
        report["source_identity"] = source_identity
        report["dependencies"] = {name: importlib.metadata.version(name)
                                  for name in ("sympy", "fpylll", "cysignals", "numpy", "gmpy2")}
        base.runtime_initialize.initialize(base.SOURCE)
        base.pipeline.validate_chunk = base.buffering.validate_cached
        variants = [(windows, chunks) for windows in args.batch_windows for chunks in args.map_chunksizes]
        report["variants"] = [dict(preparation_batch_windows=windows, map_chunksize=chunks)
                              for windows, chunks in variants]
        report["policy"] = dict(group_limit=2, logical_window_cells=256, workers=args.workers,
                                journal_buffer_records=8, journal_max_age_seconds=.25,
                                ready_limit_single_window=2, ready_limit_multiwindow=1,
                                prepared_item_max_bytes=12 * 1024**2,
                                prepared_reservation_ceiling_bytes=48 * 1024**2,
                                native_max_packet_positions=50000000, native_max_task_positions=10000000)
        report["windows"] = [row[0]["window"] for row in selected]
        output = ROOT / "results" / ("batching-journals-" + str(time.time_ns()))
        output.mkdir(parents=True)
        report["journal_directory"] = output.name
        binary = ROOT / "bin" / ("scaling_gpu" if args.backend == "gpu" else "scaling_cpu")
        backend = "gpu" if args.backend == "gpu" else "emulated"
        report["binary_sha256"] = base.digest(binary)
        with base.EngineSession([str(binary)], backend, deadline) as session:
            report["engine_startup_seconds"] = session.startup_seconds
            report["preflight"] = base.verify_all_inputs(session, rows, backend, deadline)
            began = time.perf_counter()
            pool = mp.get_context("spawn").Pool(args.workers, initializer=base.runtime_initialize.initialize,
                                               initargs=(base.SOURCE,))
            identities = {}
            checked = base.CheckedPool(pool, deadline)
            while len(identities) < args.workers:
                identities.update(checked.map(base.core.worker_identity, range(4 * args.workers), 1))
            report["pool_startup_seconds"] = time.perf_counter() - began
            engine = base.pipeline.OwnedEngine(session)
            rng = random.Random(20261113)
            for repeat in range(args.repeats):
                order = list(variants)
                rng.shuffle(order)
                for windows, chunks in order:
                    base.remaining(deadline)
                    trial = run_trial(pool, engine, selected, args, repeat, windows, chunks,
                                      deadline, output, source_identity, report["binary_sha256"])
                    report["trials"].append(trial)
                    base.replay.save(target, report)
                    print(json.dumps({key: trial[key] for key in ("variant", "repeat", "pipeline_seconds",
                                                                 "logical_cell_visits_per_second")}), flush=True)
        medians = {f"windows-{windows}-chunks-{chunks}": statistics.median(
            trial["pipeline_seconds"] for trial in report["trials"]
            if trial["preparation_batch_windows"] == windows and trial["map_chunksize"] == chunks)
            for windows, chunks in variants}
        baseline = medians["windows-1-chunks-8"]
        report["summary"] = dict(median_pipeline_seconds=medians,
                                speedup_vs_matched_baseline={key: baseline / value for key, value in medians.items()},
                                fastest_tested_variant=min(medians, key=medians.get),
                                baseline="windows-1-chunks-8",
                                stage_warning="Worker sums and producer/consumer times overlap; batching queue units differ. Do not add stages or call map wall time isolated serialization cost.")
        report["status"] = "passed"
    except BaseException as error:
        report.update(status="failed", error=repr(error))
        raise
    finally:
        if pool is not None:
            pool.terminate()
            pool.join()
        signal.setitimer(signal.ITIMER_REAL, 0)
        report["elapsed_seconds"] = time.monotonic() - start
        base.replay.save(target, report)
    print(json.dumps(report["summary"], indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("cpu", "gpu"), default="gpu")
    parser.add_argument("--workers", type=int, choices=(1, 2, 4, 8), default=8)
    parser.add_argument("--batch-windows", type=int, nargs="+", default=[1, 2, 4, 8])
    parser.add_argument("--map-chunksizes", type=int, nargs="+", default=[8, 32])
    parser.add_argument("--passes", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-seconds", type=int, default=480)
    parser.add_argument("--units-per-hour", type=float)
    args = parser.parse_args()
    if (not 1 <= args.passes <= 3 or not 1 <= args.repeats <= 3 or not 30 <= args.max_seconds <= 600
            or len(set(args.batch_windows)) != len(args.batch_windows)
            or any(windows not in (1, 2, 4, 8) for windows in args.batch_windows)
            or len(set(args.map_chunksizes)) != len(args.map_chunksizes)
            or any(chunks not in (8, 16, 32) for chunks in args.map_chunksizes)
            or 1 not in args.batch_windows or 8 not in args.map_chunksizes):
        parser.error("Use bounded unique policies including windows=1/chunks=8, 1-3 passes/repeats and 30-600 seconds")
    main(args)
