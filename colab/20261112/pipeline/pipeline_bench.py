"""TEST_ONLY: exact planning through locally durable selected-window receipts.

Regenerates the published packets. Never claims search ownership or coverage.
The frozen planner's Python/dependency, arithmetic and native guards stay intact.
"""
from pathlib import Path
import argparse
import cProfile
import hashlib
import importlib.metadata
import json
import multiprocessing as mp
import os
import random
import pstats
import signal
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORKER = HERE / "vendor/worker"
SOURCE = WORKER / "source/lattice_prototype"
sys.path[:0] = [str(ROOT), str(WORKER), str(WORKER / "source/lattice_gpu")]

import colab_bench as replay
from engine_session import EngineSession
import buffered_pipeline as buffering
import coordinator_pipeline as pipeline
import runtime_initialize
import scaling_core as core
import scheduling
import width_coverage as coverage


def require(condition, message):
    if not condition:
        raise ValueError(message)


def remaining(deadline):
    left = deadline - time.monotonic()
    if left <= 0:
        raise TimeoutError("Bounded pipeline benchmark deadline reached")
    return left


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class CheckedPool:
    def __init__(self, pool, deadline):
        self.pool, self.deadline = pool, deadline

    def map(self, function, items, chunksize=8):
        return self.pool.map_async(function, items, chunksize).get(
            timeout=min(25, remaining(self.deadline)))


def load_inputs(window_limit):
    metadata = json.loads((ROOT / "data/export.json").read_text())
    require(digest(ROOT / "data/packets.jsonl") == metadata["packet_file_sha256"],
            "Packet dataset identity changed")
    rows = [json.loads(line) for line in (ROOT / "data/packets.jsonl").read_text().splitlines()]
    require(len(rows) == 42, "Expected all 42 independently checked input packets")
    windows = {}
    for row in rows:
        require(hashlib.sha256(row["packet"].encode()).hexdigest() == row["packet_sha256"],
                "Input packet checksum changed")
        if row["group"] == "realistic":
            key = json.dumps(row["window"], sort_keys=True)
            windows.setdefault(key, []).append(row)
    selected = list(windows.values())
    require(len(selected) == 9, "Representative window set changed")
    if window_limit == 3:
        # One window from each of the three original regions, for local smoke tests.
        selected = [selected[0], selected[4], selected[5]]
    return rows, selected, metadata


def check_prepared(chunk, expected):
    buffering.validate_cached(chunk)
    batches = chunk.plan.batches
    require(chunk.window.identity() == expected[0]["window"], "Prepared window changed")
    require(len(batches) == len(expected), "Prepared packet count changed")
    for batch, row in zip(batches, expected):
        require(batch.packet == row["packet"] and batch.points == row["points"],
                "Regenerated native packet differs from published independently checked bytes")
        require(chunk.plan.certificate_sha256 == row["window_certificate_sha256"],
                "Exact window certificate changed")


def profile_serial_preparation(selected):
    class Serial:
        def map(self, function, items, chunksize=8):
            return list(map(function, items))
    profiler = cProfile.Profile()
    began = time.perf_counter()
    for rows in (selected[0], selected[-1]):
        chunk = profiler.runcall(buffering.prepare_cached, Serial(),
                                 pipeline.Window(**rows[0]["window"]), 2)
        check_prepared(chunk, rows)
    path = ROOT / "results/preparation-profile.prof"
    profiler.dump_stats(path)
    stats = pstats.Stats(profiler)
    functions = []
    for (filename, line, name), (primitive, calls, self_time, cumulative, callers) in sorted(
            stats.stats.items(), key=lambda item: item[1][3], reverse=True)[:40]:
        functions.append(dict(file=Path(filename).name, line=line, function=name,
                              primitive_calls=primitive, calls=calls,
                              self_seconds=self_time, cumulative_seconds=cumulative))
    return dict(seconds=time.perf_counter() - began, functions=functions,
                scope="Two serial preparation profiles outside pipeline timings; exact packet bytes checked.")


def verify_all_inputs(engine, rows, backend, deadline):
    began = time.perf_counter()
    for row in rows:
        response, _ = engine.run(row["packet"], timeout=min(30, remaining(deadline)))
        replay.verify(row["packet"], response, backend, row["expected"])
        reference = subprocess.run(
            [str(ROOT / "bin/gmp_reference")], input=row["packet"], text=True,
            capture_output=True, check=True, timeout=min(30, remaining(deadline)))
        replay.verify(row["packet"], json.loads(reference.stdout), "emulated", row["expected"])
    control = next(row for row in rows if row["group"] == "control")
    response, _ = engine.run(control["packet"], timeout=min(30, remaining(deadline)))
    try:
        replay.verify(control["packet"], dict(response, points_visited=response["points_visited"] - 1),
                      backend, control["expected"])
    except ValueError:
        pass
    else:
        raise AssertionError("Incomplete native response accepted")
    return dict(all_42_packets_match_gmp=True, fresh_gmp_all_42_packets=True,
                incomplete_response_rejected=True, seconds=time.perf_counter() - began)


def run_trial(pool, engine, selected, workers, repeat, deadline, output, source_identity, binary_hash):
    trial_id = f"workers-{workers}-repeat-{repeat}"
    windows = [pipeline.Window(**rows[0]["window"]) for rows in selected]
    expected = {json.dumps(rows[0]["window"], sort_keys=True): rows for rows in selected}
    # Each source region is contiguous; separate journals prevent artificial gaps.
    regions = {}
    for window in windows:
        region = next((key for key, value in regions.items() if value[-1].last == window.first), None)
        if region is None:
            region = str(len(regions))
            regions[region] = []
        regions[region].append(window)
    journal_for = {}
    journals = []
    identities = []
    stages = dict(prepare_worker_wall_seconds=0., prepare_worker_cpu_seconds=0.,
                  certify_worker_wall_seconds=0., certify_worker_cpu_seconds=0.,
                  prepared_consistency_seconds=0., engine_rpc_seconds=0.,
                  exact_verification_seconds=0., kernel_seconds=0.,
                  journal_accept_seconds=0.)
    # Startup is measured separately from the steady selected-window pipeline.
    setup = time.perf_counter()
    for region, group in regions.items():
        first, last = group[0], group[-1]
        whole = coverage.Window(first.lo, first.hi, first.first, last.last,
                                first.width, first.bits, first.cap, first.geometry_policy, 2)
        identity = dict(trial=trial_id, source_identity=source_identity,
                        binary_sha256=binary_hash, TEST_ONLY=True)
        directory = output / trial_id / f"region-{region}"
        journal = buffering.BufferedJournal(directory, identity, whole, records=8)
        journals.append(journal)
        identities.append((directory, identity, whole))
        for window in group:
            journal_for[json.dumps(window.identity(), sort_keys=True)] = journal
    journal_setup_seconds = time.perf_counter() - setup
    # Frozen production functions; one window ahead and two ready buffers.
    def prepare_many(group):
        remaining(deadline)
        yield from scheduling.prepare_many(pool, group, 2, cache=True)

    stream = scheduling.BulkStream(windows, prepare_many, batch_windows=1, ready_limit=2)
    points = requests = completed = 0
    began = time.perf_counter()
    queue_metrics = None
    try:
        with stream:
            for chunk in stream:
                remaining(deadline)
                key = json.dumps(chunk.window.identity(), sort_keys=True)
                checked = time.perf_counter()
                check_prepared(chunk, expected[key])
                stages["prepared_consistency_seconds"] += time.perf_counter() - checked
                record = pipeline.execute_chunk(chunk, engine, trial=trial_id, coordinator=0,
                                                timeout=min(30, remaining(deadline)))
                coverage.add_coverage(record, chunk, 2)
                for row in chunk.worker_seconds:
                    for index, name in enumerate(("prepare_worker_wall_seconds", "prepare_worker_cpu_seconds",
                                                  "certify_worker_wall_seconds", "certify_worker_cpu_seconds")):
                        stages[name] += row[index]
                for name, target in (("prepared_plan_consistency", "prepared_consistency_seconds"),
                                     ("engine_rpc", "engine_rpc_seconds"),
                                     ("exact_output_verification", "exact_verification_seconds")):
                    stages[target] += record["stages"][name]["wall_seconds"]
                # Existing exact response/certificate verification is retained above.
                # Match all returned native counts/hits to supplied independent GMP.
                checked = time.perf_counter()
                for receipt, row, batch in zip(record["batches"], expected[key], chunk.plan.batches):
                    require(receipt["native_counts"] == [
                        (task.id, count["expected"], count["visited"])
                        for task, count in zip(batch.tasks, row["expected"]["counts"])],
                        "Trial native counts differ from independent GMP")
                    expected_hits = sorted((batch.tasks[hit["task"]].id, hit["linear"],
                                            hit["a"], hit["b"], hit["c"])
                                           for hit in row["expected"]["hits"])
                    require(receipt["native_hit_records"] == expected_hits,
                            "Trial native hits differ from independent GMP")
                    stages["kernel_seconds"] += receipt.get("kernel_seconds") or 0.
                stages["exact_verification_seconds"] += time.perf_counter() - checked
                checked = time.perf_counter()
                journal_for[key].commit(record)
                stages["journal_accept_seconds"] += time.perf_counter() - checked
                points += chunk.plan.points
                requests += len(chunk.plan.batches)
                completed += 1
                stream.ack(chunk)
            queue_metrics = stream.snapshot()
        checked = time.perf_counter()
        for journal in journals:
            journal.close()  # Includes final fsync/checkpoint/directory sync.
        stages["journal_close_seconds"] = time.perf_counter() - checked
        elapsed = time.perf_counter() - began
    finally:
        for journal in journals:
            if not journal.lock.closed:
                journal.close()
    # Recovery verifies independently re-read durable cursors and hash chains.
    recovery = time.perf_counter()
    for directory, identity, whole in identities:
        reopened = buffering.BufferedJournal(directory, identity, whole, records=8)
        try:
            require(reopened.state["next_patch"] == whole.last, "Durable cursor is incomplete")
            require(reopened.state["completed_bound"] is None, "Benchmark claimed a global bound")
        finally:
            reopened.close()
    recovery_seconds = time.perf_counter() - recovery
    require(completed == len(windows), "Incomplete selected-window pipeline")
    require(points == sum(row["points"] for rows in selected for row in rows), "Trial point total changed")
    return dict(workers=workers, repeat=repeat, windows=completed, requests=requests,
                verified_positions=points, pipeline_seconds=elapsed,
                logical_cells=sum(w.last - w.first for w in windows),
                cells_per_second=sum(w.last - w.first for w in windows) / elapsed,
                stages=stages, queue=queue_metrics, journal_setup_seconds=journal_setup_seconds,
                journal_flush_seconds=sum(j.flush_seconds for j in journals),
                journal_flush_count=sum(j.flush_count for j in journals),
                durable_recovery_seconds=recovery_seconds,
                durable_recovery_passed=True, regenerated_packet_bytes_match=True)


def main(args):
    start = time.monotonic()
    deadline = start + args.max_seconds
    def alarm(signum, frame):
        raise TimeoutError("Overall pipeline benchmark time limit reached")
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, args.max_seconds)
    report = dict(status="running", TEST_ONLY=True, new_scientific_coverage=False,
                  backend=args.backend, hardware=replay.hardware(), trials=[],
                  compute_units_per_hour_observed_by_user=args.units_per_hour,
                  exclusions="Fixed replay windows only; no new reservation, ownership or search coverage.",
                  limitations="Local pipeline: CPU planning, exact certification, packets, native execution, exact verification and fsynced local journals. Network delivery, remote mirrors/checkpoints and production GMP audit cadence are excluded. Fresh independent GMP verification of all 42 packets is a separately timed preflight.")
    target = ROOT / "results/pipeline-benchmark.json"
    pools = {}
    try:
        rows, selected, metadata = load_inputs(args.window_limit)
        report["packet_export_sha256"] = metadata["packet_file_sha256"]
        provenance = json.loads((HERE / "SOURCE_PROVENANCE.json").read_text())
        for name, expected in provenance["files_byte_identical_to_frozen_worker"].items():
            require(digest(HERE / name) == expected, "Frozen planner source changed: " + name)
        source_identity = digest(HERE / "SOURCE_PROVENANCE.json")
        report["planner_source_identity"] = source_identity
        report["dependencies"] = {name: importlib.metadata.version(name)
                                  for name in ("sympy", "fpylll", "cysignals", "numpy", "gmpy2")}
        runtime_initialize.initialize(SOURCE)
        pipeline.validate_chunk = buffering.validate_cached
        available = len(os.sched_getaffinity(0))
        counts = [count for count in args.workers if count <= max(1, available - 1)]
        require(1 in counts, "One-worker baseline is required")
        report["worker_counts"] = counts
        report["skipped_worker_counts"] = [count for count in args.workers if count not in counts]
        report["policy"] = dict(group_limit=2, logical_window_cells=256,
                                preparation_batch_windows=1, ready_limit=2,
                                journal_buffer_records=8, journal_max_age_seconds=.25,
                                native_max_packet_positions=50_000_000,
                                native_max_task_positions=10_000_000)
        binary = ROOT / "bin" / ("scaling_gpu" if args.backend == "gpu" else "scaling_cpu")
        backend = "gpu" if args.backend == "gpu" else "emulated"
        report["binary_sha256"] = digest(binary)
        report["windows"] = [row[0]["window"] for row in selected]
        report["pool_startup_seconds"] = {}
        output = ROOT / "results" / ("pipeline-journals-" + str(time.time_ns()))
        output.mkdir(parents=True)
        report["journal_directory"] = output.name
        with EngineSession([str(binary)], backend, deadline) as session:
            engine = pipeline.OwnedEngine(session)
            report["engine_startup_seconds"] = session.startup_seconds
            report["preflight"] = verify_all_inputs(session, rows, backend, deadline)
            report["preparation_profile"] = profile_serial_preparation(selected)
            for count in counts:
                began = time.perf_counter()
                pool = mp.get_context("spawn").Pool(count, initializer=runtime_initialize.initialize,
                                                   initargs=(SOURCE,))
                pools[count] = pool
                checked = CheckedPool(pool, deadline)
                identities = {}
                while len(identities) < count:
                    remaining(deadline)
                    identities.update(checked.map(core.worker_identity, range(4 * count), 1))
                report["pool_startup_seconds"][str(count)] = time.perf_counter() - began
            rng = random.Random(20261112)
            for repeat in range(args.repeats):
                order = list(counts)
                rng.shuffle(order)
                for count in order:
                    remaining(deadline)
                    trial = run_trial(CheckedPool(pools[count], deadline), engine, selected,
                                      count, repeat, deadline, output, source_identity,
                                      report["binary_sha256"])
                    report["trials"].append(trial)
                    replay.save(target, report)
                    print(json.dumps({key: trial[key] for key in
                          ("workers", "repeat", "pipeline_seconds", "cells_per_second")}), flush=True)
        medians = {str(count): statistics.median(trial["pipeline_seconds"] for trial in report["trials"]
                                              if trial["workers"] == count) for count in counts}
        report["summary"] = dict(median_pipeline_seconds=medians,
                               speedup_vs_one_worker={key: medians["1"] / value for key, value in medians.items()},
                               fastest_tested_worker_count=int(min(medians, key=medians.get)),
                               stage_warning="Worker sums and producer/consumer timings overlap; do not add them or call queue wait GPU utilization.")
        report["status"] = "passed"
    except BaseException as error:
        report.update(status="failed", error=repr(error))
        raise
    finally:
        for pool in pools.values():
            pool.terminate()
        for pool in pools.values():
            pool.join()
        signal.setitimer(signal.ITIMER_REAL, 0)
        report["elapsed_seconds"] = time.monotonic() - start
        replay.save(target, report)
    print(json.dumps(report["summary"], indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("cpu", "gpu"), default="gpu")
    parser.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4, 8])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--window-limit", type=int, choices=(3, 9), default=9)
    parser.add_argument("--max-seconds", type=int, default=480)
    parser.add_argument("--units-per-hour", type=float)
    args = parser.parse_args()
    if (not 1 <= args.repeats <= 3 or not 30 <= args.max_seconds <= 600 or
            not args.workers or args.workers[0] != 1 or len(set(args.workers)) != len(args.workers) or
            any(count not in (1, 2, 4, 8) for count in args.workers)):
        parser.error("Use bounded unique worker counts starting with 1, 1-3 repeats and 30-600 seconds")
    main(args)
