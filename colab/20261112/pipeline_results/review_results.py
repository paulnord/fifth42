"""Independently check saved pipeline receipts against the published packet oracle.

Reads JSON and bytes only; never executes code supplied in a results archive.
The separately reconstructed original benchmark bundle supplies data/packets.jsonl.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import statistics
import zipfile


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def window_key(window):
    return canonical(window).decode()


def review(archive_path, bundle, sources):
    with zipfile.ZipFile(archive_path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)), "Duplicate result ZIP names")
        require(sum(entry.file_size for entry in entries) <= 32 * 1024**2,
                "Results exceed finite export allowance")
        for entry in entries:
            rel = Path(entry.filename)
            require(not rel.is_absolute() and ".." not in rel.parts and not entry.is_dir(),
                    "Unsafe result member")
            require((entry.external_attr >> 16) & 0o170000 != 0o120000, "Symlink result member")
        require(archive.testzip() is None, "ZIP CRC failure")
        data = {name: archive.read(name) for name in names}
    checksums = {}
    for line in data["RESULT_SHA256SUMS"].decode().splitlines():
        expected, name = line.split("  ", 1)
        require(name not in checksums and name in data and sha(data[name]) == expected,
                "Result member checksum mismatch: " + name)
        checksums[name] = expected
    require(set(checksums) == set(data) - {"RESULT_SHA256SUMS"}, "Unmanifested result member")
    for name in ("SHA256SUMS", "data/export.json"):
        require(data[name] == (bundle / name).read_bytes(), "Original bundle identity differs")
    for name in ("MANIFEST.json", "SOURCE_PROVENANCE.json", "requirements.txt"):
        require(data["pipeline/" + name] == (sources / name).read_bytes(),
                "Planner source identity differs: " + name)
    meta = json.loads(data["data/export.json"])
    packet_bytes = (bundle / "data/packets.jsonl").read_bytes()
    require(sha(packet_bytes) == meta["packet_file_sha256"], "Independent packet data identity differs")
    rows = [json.loads(line) for line in packet_bytes.splitlines()]
    expected_windows = {}
    for row in rows:
        require(sha(row["packet"].encode()) == row["packet_sha256"], "Oracle packet changed")
        if row["group"] == "realistic":
            expected_windows.setdefault(window_key(row["window"]), []).append(row)
    report = json.loads(data["results/pipeline-benchmark.json"])
    build = json.loads(data["results/build.json"])
    require(report["status"] == build["status"] == "passed", "Run/build did not pass")
    require(report["TEST_ONLY"] is True and report["new_scientific_coverage"] is False,
            "Unexpected scientific coverage claim")
    require(report["backend"] == "gpu" and "NVIDIA L4" in report["hardware"]["gpu"],
            "This reviewed run must identify its L4 GPU")
    require(report["packet_export_sha256"] == sha(packet_bytes), "Run input identity differs")
    require(report["planner_source_identity"] == sha(data["pipeline/SOURCE_PROVENANCE.json"]),
            "Planner identity digest differs")
    require(report["binary_sha256"] == build["binaries"]["scaling_gpu"], "Executed binary identity differs")
    require(report["dependencies"] == dict(sympy="1.14.0", fpylll="0.6.4", cysignals="1.12.5",
                                          numpy="2.3.5", gmpy2="2.2.2"), "Dependency pins changed")
    require(report["hardware"]["python"].startswith("3.12."), "Wrong planner Python")
    for name in ("all_42_packets_match_gmp", "fresh_gmp_all_42_packets", "incomplete_response_rejected"):
        require(report["preflight"].get(name) is True, "Missing exact preflight: " + name)
    require({window_key(window) for window in report["windows"]} == set(expected_windows)
            and len(report["windows"]) == len(expected_windows) == 9, "Selected windows changed")
    require(report["worker_counts"] == [1, 2, 4, 8] and not report["skipped_worker_counts"],
            "Worker sweep changed")
    require(report["policy"] == dict(group_limit=2, logical_window_cells=256,
                                     preparation_batch_windows=1, ready_limit=2,
                                     journal_buffer_records=8, journal_max_age_seconds=.25,
                                     native_max_packet_positions=50000000,
                                     native_max_task_positions=10000000), "Pipeline policy changed")
    trials = report["trials"]
    require(len(trials) == 12 and {(t["workers"], t["repeat"]) for t in trials} ==
            {(workers, repeat) for workers in (1, 2, 4, 8) for repeat in range(3)},
            "Missing or duplicated randomized trial")
    journal_total = record_total = batch_total = 0
    all_checkpoint_names = {name for name in names if name.endswith("/checkpoint.json")}
    used_checkpoints = set()
    for trial in trials:
        require(trial["windows"] == 9 and trial["requests"] == 23 and trial["logical_cells"] == 2304
                and trial["verified_positions"] == 775687194 and trial["regenerated_packet_bytes_match"]
                and trial["durable_recovery_passed"], "Incomplete trial")
        require(math.isclose(trial["cells_per_second"], 2304 / trial["pipeline_seconds"], rel_tol=1e-12),
                "Trial throughput summary differs")
        require(all(trial["queue"][name] == 0 for name in ("ready", "inflight", "active", "outstanding"))
                and trial["queue"]["peak_ready"] <= 2 and trial["queue"]["peak_outstanding"] <= 4,
                "Preparation queue did not drain within its bounds")
        trial_name = f"workers-{trial['workers']}-repeat-{trial['repeat']}"
        prefix = f"results/{report['journal_directory']}/{trial_name}/"
        checkpoint_names = sorted(name for name in all_checkpoint_names if name.startswith(prefix))
        require(len(checkpoint_names) == 3, "Missing region journals")
        seen_windows = set()
        points = requests = 0
        for checkpoint_name in checkpoint_names:
            used_checkpoints.add(checkpoint_name)
            checkpoint = json.loads(data[checkpoint_name])
            identity = checkpoint["identity"]
            require(identity == dict(TEST_ONLY=True, binary_sha256=report["binary_sha256"],
                                     source_identity=report["planner_source_identity"], trial=trial_name),
                    "Journal identity changed")
            raw = data[checkpoint_name.replace("checkpoint.json", "coverage.jsonl")]
            require(len(raw) == checkpoint["journal_offset"] and raw.endswith(b"\n"),
                    "Durable offset or newline mismatch")
            previous = "0" * 64
            cursor = checkpoint["window"]["first"]
            journal_points = physical_tasks = chunks = 0
            for line in raw.splitlines():
                record = json.loads(line)
                record_hash = record.pop("sha256")
                chunks += 1
                require(record["previous_sha256"] == previous and record["sequence"] == chunks
                        and sha(canonical(record)) == record_hash, "Invalid journal hash chain")
                previous = record_hash
                window = record["window"]
                key = window_key(window)
                require(key in expected_windows and key not in seen_windows and window["first"] == cursor,
                        "Missing, duplicated or reordered window")
                seen_windows.add(key)
                cursor = window["last"]
                expected = expected_windows[key]
                tasks = [task for row in expected for task in row["tasks"]]
                tokens = [sha(canonical(task)) for task in tasks]
                require(record["patches"] == [[task["id"], token, task["points"]]
                                               for task, token in zip(tasks, tokens)],
                        "Per-task certificate manifest differs from oracle")
                require(record["certificate_sha256"] == sha(("\n".join(tokens) + "\n").encode())
                        == expected[0]["window_certificate_sha256"], "Window certificate differs")
                geometry = b"".join(canonical(task) + b"\n" for task in tasks)
                require(record["geometry_sha256"] == sha(geometry), "Geometry digest differs")
                require(record["coverage_schema"] == "logical-width8-physical-groups-v1"
                        and record["group_limit"] == 2 and record["complete"] is True,
                        "Logical coverage schema changed")
                require(record["logical_spans"] == expected[0]["original_cell_spans"], "Physical spans differ")
                require(record["physical_specifications"] == [
                    [task["id"], task["cmin"], task["cmax"], task["left"], task["right"], task["cap"], task["bits"]]
                    for task in tasks], "Physical specification differs")
                require(record["precision_bits"] == [[task["id"], task["bits"]] for task in tasks],
                        "Precision manifest changed")
                require(record["points"] == sum(task["points"] for task in tasks), "Window point total changed")
                require(len(record["batches"]) == len(expected), "Window packet count changed")
                for index, (batch, row) in enumerate(zip(record["batches"], expected)):
                    require(batch["identity"] == dict(batch=index, coordinator=0, packet_sha256=row["packet_sha256"],
                                                       trial=trial_name, window=window), "Native request identity differs")
                    require(batch["backend"] == "gpu" and batch["points"] == row["points"]
                            and batch["patch_ids"] == [task["id"] for task in row["tasks"]], "Packet task layout changed")
                    expected_counts = [[task["id"], count["expected"], count["visited"]]
                                       for task, count in zip(row["tasks"], row["expected"]["counts"])]
                    expected_hits = sorted([row["tasks"][hit["task"]]["id"], hit["linear"], hit["a"], hit["b"], hit["c"]]
                                           for hit in row["expected"]["hits"])
                    require(batch["native_counts"] == expected_counts and batch["native_hit_records"] == expected_hits,
                            "Timed native counts/hits differ from independent GMP")
                    # The realistic oracle has no hits; nonempty controls are checked in preflight.
                    require(not expected_hits and not record["hits"], "Unexpected realistic-window hit")
                    batch_total += 1
                journal_points += record["points"]
                physical_tasks += len(tasks)
                requests += len(record["batches"])
                record_total += 1
            require(previous == checkpoint["journal_sha256"] and cursor == checkpoint["next_patch"]
                    == checkpoint["window"]["last"] and chunks == checkpoint["chunks"], "Durable cursor mismatch")
            require(checkpoint["points"] == journal_points and checkpoint["physical_tasks"] == physical_tasks
                    and checkpoint["patches"] == cursor - checkpoint["window"]["first"]
                    and checkpoint["completed_bound"] is None and checkpoint["hits"] == [],
                    "Durable checkpoint totals/coverage differ")
            points += journal_points
            journal_total += 1
        require(seen_windows == set(expected_windows) and points == trial["verified_positions"]
                and requests == trial["requests"], "Incomplete trial journal set")
    require(used_checkpoints == all_checkpoint_names and journal_total == 36 and record_total == 108
            and batch_total == 276, "Unexpected durable receipt count")
    metrics = {}
    for workers in report["worker_counts"]:
        selected = [trial for trial in trials if trial["workers"] == workers]
        median = lambda function: statistics.median(function(trial) for trial in selected)
        metrics[str(workers)] = dict(
            pipeline_seconds=median(lambda t: t["pipeline_seconds"]),
            cells_per_second=median(lambda t: t["cells_per_second"]),
            wait_for_preparation_seconds=median(lambda t: t["queue"]["consumer_wait_empty_seconds"]),
            kernel_seconds=median(lambda t: t["stages"]["kernel_seconds"]),
            engine_rpc_seconds=median(lambda t: t["stages"]["engine_rpc_seconds"]),
            prepared_consistency_seconds=median(lambda t: t["stages"]["prepared_consistency_seconds"]),
            journal_flush_seconds=median(lambda t: t["journal_flush_seconds"]),
            mean_ready_depth=median(lambda t: t["queue"]["mean_ready_depth"]),
            worker_prepare_and_certify_cpu_seconds=median(lambda t: t["stages"]["prepare_worker_cpu_seconds"]
                                                         + t["stages"]["certify_worker_cpu_seconds"]))
        require(math.isclose(metrics[str(workers)]["pipeline_seconds"],
                             report["summary"]["median_pipeline_seconds"][str(workers)], rel_tol=1e-12),
                "Reported pipeline median differs")
    for workers, value in metrics.items():
        value["speedup_vs_one_worker"] = metrics["1"]["pipeline_seconds"] / value["pipeline_seconds"]
        require(math.isclose(value["speedup_vs_one_worker"],
                             report["summary"]["speedup_vs_one_worker"][workers], rel_tol=1e-12), "Speedup differs")
    return dict(status="passed", original_zip_sha256=sha(Path(archive_path).read_bytes()),
                original_zip_bytes=Path(archive_path).stat().st_size, result_members=len(names),
                all_export_checksums_verified=True, source_and_input_identities_verified=True,
                native_binary_identity_matches_build=True, preflight_reported_passed=report["preflight"],
                journal_hash_chains_and_cursors_independently_verified=journal_total,
                exact_window_records_verified=record_total, native_packet_receipts_matched_to_gmp_oracle=batch_total,
                certificate_identities_and_packet_identities_verified=True,
                gpu="NVIDIA L4", worker_medians=metrics,
                eight_vs_four_throughput_ratio=metrics["4"]["pipeline_seconds"] / metrics["8"]["pipeline_seconds"],
                compute_unit_cost_available=report["compute_units_per_hour_observed_by_user"] is not None,
                production_changes=False, new_scientific_coverage=False,
                limitations=report["limitations"] + " One short Colab session with three repetitions per worker count. Worker/stage times overlap; queue wait is not GPU utilization. No local GPU rerun.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = review(args.archive, args.bundle, args.sources)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
