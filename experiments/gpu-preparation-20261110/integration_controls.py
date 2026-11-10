"""Finite exact gates for isolated GPU preparation. TEST_ONLY; no journals.

Run only while holding the experiment's GPU lease. Both proposed and cold CPU
bases are enumerated by the native GPU and GMP separately. Different valid
bases may have different boxes; their final exact candidate sets must agree.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
WORKER = ROOT / "worker"
SOURCE = WORKER / "source/lattice_prototype"
sys.path[:0] = [str(WORKER), str(WORKER / "source/lattice_gpu")]

import adapter_runtime as adapter
import buffered_pipeline as buffering
import coordinator_pipeline as pipeline
import gpu_preparation as preparation
import runtime_initialize
import scaling_core as core


class Serial:
    """Unmodified cold CPU preparation in this exact-runtime process."""

    def map(self, function, arguments, chunksize):
        return list(map(function, arguments))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_spans(chunk):
    cursor = chunk.window.first
    for first, last in chunk.window.spans:
        if not (first == cursor and first < last <= chunk.window.last):
            raise AssertionError(("Noncontiguous logical coverage", cursor, first, last))
        cursor = last
    if cursor != chunk.window.last:
        raise AssertionError(("Incomplete logical coverage", cursor, chunk.window.last))
    if len(chunk.window.spans) != chunk.plan.tasks:
        raise AssertionError("Physical spans do not identify every admitted task")


def check_chunk(chunk):
    # Neither validator is replaced or weakened for this gate.
    check_spans(chunk)
    buffering.validate_cached(chunk)
    pipeline.validate_chunk(chunk)
    # A copied/replaced object must not inherit the private checked-data seal.
    try:
        buffering.validate_cached(replace(chunk))
    except ValueError as exc:
        if "seal" not in str(exc):
            raise
    else:
        raise AssertionError("Unchecked chunk copy inherited a private seal")


def brute_force(lo=136, hi=153, cap=708588):
    powers = [value**5 for value in range(hi + 1)]
    hits = {
        (a, b, c, powers[a] + powers[b] - powers[c])
        for c in range(lo, hi + 1)
        for b in range(1, c)
        for a in range(1, b + 1)
        if abs(powers[a] + powers[b] - powers[c]) <= cap
    }
    if (117, 144, 153, 708588) not in hits:
        raise AssertionError("Full small-shell oracle lost the known positive")
    return hits


def enumerate_and_check(chunk, engine, directory, timeout):
    directory.mkdir()
    check_chunk(chunk)
    hits = set()
    packets = []
    for index, batch in enumerate(chunk.plan.batches):
        stem = directory / f"batch-{index:03d}"
        stem.with_suffix(".packet").write_text(batch.packet)
        began = time.perf_counter()
        raw, _ = engine.run(batch.packet, timeout=timeout)
        gpu_seconds = time.perf_counter() - began
        write_json(stem.with_suffix(".gpu.json"), raw)
        pipeline.validate_response_types(raw)
        decoded = core.decode_batch(batch, raw, "gpu")
        began = time.perf_counter()
        command = [str(WORKER / "bin/gmp_reference")]
        done = subprocess.run(
            command, input=batch.packet, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
        gmp_seconds = time.perf_counter() - began
        stem.with_suffix(".gmp.stdout").write_text(done.stdout)
        stem.with_suffix(".gmp.stderr").write_text(done.stderr)
        if done.returncode:
            raise RuntimeError(f"GMP reference exited {done.returncode}: {done.stderr}")
        reference = json.loads(done.stdout)
        pipeline.validate_response_types(reference)
        reference_hits = core.decode_batch(batch, reference, "emulated")
        counts = adapter.normalized_counts(batch, raw)
        native_hits = adapter.normalized_hits(batch, raw)
        if counts != adapter.normalized_counts(batch, reference):
            raise AssertionError(("GPU/GMP per-task count mismatch", index))
        if native_hits != adapter.normalized_hits(batch, reference):
            raise AssertionError(("GPU/GMP native candidate mismatch", index))
        if decoded != reference_hits:
            raise AssertionError(("GPU/GMP exact decoded-hit mismatch", index))
        hits.update(decoded)
        packets.append(dict(
            index=index, packet_sha256=hashlib.sha256(batch.packet.encode()).hexdigest(),
            points=batch.points, counts=counts, native_hit_records=native_hits,
            exact_hits=sorted(decoded), gpu_seconds=gpu_seconds,
            gmp_seconds=gmp_seconds, gpu_gmp_exact_equal=True,
        ))
    # Recheck the same sealed object after native work.
    check_chunk(chunk)
    return dict(
        points=chunk.plan.points, physical_tasks=chunk.plan.tasks,
        logical_spans=chunk.window.spans, geometry_sha256=chunk.geometry_sha256,
        certificate_sha256=chunk.plan.certificate_sha256,
        payload_bytes=chunk.payload_bytes, packets=packets, hits=sorted(hits),
        contiguous_coverage=True, unchanged_buffer_validation=True,
        copied_chunk_without_seal_rejected=True,
    ), hits


def cases():
    for group in (4, 8, 16):
        yield f"known-positive-group{group}", pipeline.Window(
            136, 153, 0, 16, 8, 222, 708588, "adaptive"
        ), group, True
    for name, first, group in (
        ("Ada", 4564955776, 4),
        ("Cabbage", 2572492928, 8),
        ("dense", 9562500096, 4),
    ):
        yield name, pipeline.Window(
            100000000001, 200000000000, first, first + 256,
            8, 222, 42, "adaptive",
        ), group, False


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    available = tuple(sorted(os.sched_getaffinity(0)))
    if len(available) < args.workers:
        raise RuntimeError("Requested worker count exceeds allowed CPU affinity")
    cpus = available[:args.workers]
    os.sched_setaffinity(0, set(cpus))
    runtime_initialize.initialize(SOURCE)
    expected = brute_force()
    write_json(args.output / "small-shell-full-brute-force.json", sorted(expected))
    result = dict(
        status="running", TEST_ONLY=True, production_coverage=False,
        production_changed=False, native_backend="gpu", workers=args.workers,
        cpus=cpus, cases=[], errors=[], quality_gate=args.quality_gate,
        proposal_fault=args.proposal_fault,
        comparison_policy=("Each basis must agree with its own GMP counts and native hits; "
                           "GPU-prepared and cold CPU bases must have identical exact hits. "
                           "Basis matrices, box sizes and physical subdivisions may differ."),
        hashes={str(path.relative_to(ROOT)): sha256(path) for path in (
            ROOT / "integration_controls.py", ROOT / "gpu_preparation.py",
            ROOT / "gpu_candidate/candidate_reduction.py",
            WORKER / "buffered_pipeline.py",
            WORKER / "source/lattice_gpu/coordinator_pipeline.py",
        )},
    )
    write_json(args.output / "result.json", result)
    stage = preparation.GPUStage(args.workers, require_lll=args.quality_gate == "exact-lll")
    pool = engine = None
    began = time.monotonic()
    try:
        pool = mp.get_context("spawn").Pool(
            args.workers, initializer=preparation.initialize,
            initargs=stage.initargs(SOURCE, cpus),
        )
        warmed = {}
        warm_deadline = time.monotonic() + 20
        while len(warmed) < args.workers:
            if time.monotonic() > warm_deadline:
                raise TimeoutError("Exact-runtime workers did not all become ready")
            warmed.update(pool.map(core.worker_identity, range(4 * args.workers), 1))
        adapter.verify_workers(warmed, cpus)
        result["worker_identities"] = warmed
        stage.start()
        fault = dict(injected=False)
        if args.proposal_fault != "none":
            original_reduce = stage.gpu.reduce_flat

            def corrupt_one(*arguments, **keywords):
                out, timing = original_reduce(*arguments, **keywords)
                if not fault["injected"]:
                    if not keywords.get("raw"):
                        raise AssertionError("Fault gate requires the raw native proposal buffer")
                    if args.proposal_fault == "zero-u":
                        for index in range(9):
                            out[0].u[index] = 0
                        out[0].status = 0
                    else:
                        out[0].status = 1
                    fault["injected"] = True
                return out, timing

            stage.gpu.reduce_flat = corrupt_one
        engine = adapter.open_session(
            WORKER / "bin/scaling_gpu", "gpu", began + args.deadline,
        )
        dispatch = preparation.GPUPool(pool, stage, 1)
        for name, window, group, full_oracle in cases():
            if args.case and name not in args.case:
                continue
            if time.monotonic() - began >= args.deadline:
                raise TimeoutError("Finite correctness gate exceeded its deadline")
            entry = dict(name=name, requested_group=group, window=window.identity())
            result["cases"].append(entry)
            directory = args.output / name
            directory.mkdir()
            try:
                start = time.perf_counter()
                cold = buffering.prepare_cached(Serial(), window, group)
                entry["cold_cpu_prepare_seconds"] = time.perf_counter() - start
                start = time.perf_counter()
                proposed = buffering.prepare_cached(dispatch, window, group)
                entry["gpu_prepare_seconds"] = time.perf_counter() - start
                entry["gpu_prepared"], proposed_hits = enumerate_and_check(
                    proposed, engine, directory / "gpu-prepared", args.timeout,
                )
                entry["cold_cpu"], cold_hits = enumerate_and_check(
                    cold, engine, directory / "cold-cpu", args.timeout,
                )
                if proposed_hits != cold_hits:
                    raise AssertionError(("GPU-prepared/cold CPU exact hits differ", name,
                                          sorted(proposed_hits), sorted(cold_hits)))
                entry["cross_basis_exact_hits_equal"] = True
                entry["identical_geometry"] = proposed.geometry_sha256 == cold.geometry_sha256
                if full_oracle:
                    if proposed_hits != expected or cold_hits != expected:
                        raise AssertionError(("Full small-shell brute-force mismatch", name,
                                              sorted(proposed_hits), sorted(expected)))
                    entry["full_small_shell_brute_force_equal"] = True
                    entry["known_positive_present"] = True
                entry["status"] = "passed"
            except Exception as exc:
                entry.update(status="failed", error_type=type(exc).__name__, error=str(exc),
                             traceback=traceback.format_exc())
                result["errors"].append(dict(case=name, type=type(exc).__name__, error=str(exc)))
            entry["gpu_stage_metrics_cumulative"] = json.loads(json.dumps(stage.metrics))
            write_json(directory / "result.json", entry)
            write_json(args.output / "result.json", result)
            print(json.dumps(dict(case=name, status=entry["status"],
                                  error=entry.get("error"))), flush=True)
            if stage.error:
                raise RuntimeError("GPU preparation service failed") from stage.error
        if not result["cases"]:
            raise ValueError("No requested correctness cases matched")
        if args.proposal_fault != "none":
            reason = "Transform is not unimodular" if args.proposal_fault == "zero-u" else "iteration_budget"
            if not fault["injected"] or stage.metrics["fallbacks"].get(reason, 0) < 1:
                raise AssertionError(("Corrupted proposal did not trigger exact/guarded cold fallback", fault, stage.metrics))
            result["forced_fault_cold_fallback_verified"] = True
        result["status"] = "failed" if result["errors"] else "passed"
    except BaseException as exc:
        result.update(status="failed", fatal_error_type=type(exc).__name__,
                      fatal_error=str(exc), fatal_traceback=traceback.format_exc())
    finally:
        if engine is not None:
            engine.close()
        if pool is not None:
            pool.terminate()
            pool.join()
        stage.close()
        result["elapsed_seconds"] = time.monotonic() - began
        result["gpu_stage_metrics"] = dict(stage.metrics)
        write_json(args.output / "result.json", result)
    print(json.dumps(dict(status=result["status"], output=str(args.output))), flush=True)
    return 0 if result["status"] == "passed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, choices=(1, 2, 4, 8, 16), default=4)
    parser.add_argument("--quality-gate", choices=("native-bounds", "exact-lll"),
                        default="native-bounds")
    parser.add_argument("--case", action="append", choices=[case[0] for case in cases()],
                        help="Run only named cases (repeatable); default all six")
    parser.add_argument("--proposal-fault", choices=("none", "zero-u", "status1"),
                        default="none", help="Corrupt exactly one isolated GPU proposal to verify cold fallback")
    parser.add_argument("--timeout", type=float, default=30,
                        help="Per native packet/GMP timeout in seconds")
    parser.add_argument("--deadline", type=float, default=300,
                        help="Bound on the complete isolated gate in seconds")
    args = parser.parse_args()
    if args.timeout <= 0 or not 0 < args.deadline <= 900:
        parser.error("Require positive packet timeout and deadline at most 900 seconds")
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
