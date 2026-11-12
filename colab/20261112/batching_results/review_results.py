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


def review(archive_path, bundle, sources, batch_sources):
    with zipfile.ZipFile(archive_path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)), "Duplicate result ZIP names")
        require(sum(entry.file_size for entry in entries) <= 64 * 1024**2,
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
    require(data["batching/MANIFEST.json"] == (batch_sources / "MANIFEST.json").read_bytes(), "Batching source manifest differs")
    meta = json.loads(data["data/export.json"])
    packet_bytes = (bundle / "data/packets.jsonl").read_bytes()
    require(sha(packet_bytes) == meta["packet_file_sha256"], "Independent packet data identity differs")
    rows = [json.loads(line) for line in packet_bytes.splitlines()]
    expected_windows = {}
    for row in rows:
        require(sha(row["packet"].encode()) == row["packet_sha256"], "Oracle packet changed")
        if row["group"] == "realistic":
            expected_windows.setdefault(window_key(row["window"]), []).append(row)
    report = json.loads(data["results/batching-benchmark.json"])
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
    require(report["base_pipeline_runner_sha256"] == sha((sources / "pipeline_bench.py").read_bytes())
            and report["batching_runner_sha256"] == sha((batch_sources / "batch_bench.py").read_bytes()),
            "Executed benchmark source identities differ")
    combined = sha(json.dumps({key: report[key] for key in
        ("planner_source_identity", "base_pipeline_runner_sha256", "batching_runner_sha256")}, sort_keys=True).encode())
    require(report["source_identity"] == combined, "Combined source identity differs")

    require(report["dependencies"] == dict(sympy="1.14.0", fpylll="0.6.4", cysignals="1.12.5",
                                          numpy="2.3.5", gmpy2="2.2.2"), "Dependency pins changed")
    require(report["hardware"]["python"].startswith("3.12."), "Wrong planner Python")
    for name in ("all_42_packets_match_gmp", "fresh_gmp_all_42_packets", "incomplete_response_rejected"):
        require(report["preflight"].get(name) is True, "Missing exact preflight: " + name)
    require({window_key(window) for window in report["windows"]} == set(expected_windows)
            and len(report["windows"]) == len(expected_windows) == 9, "Selected windows changed")
    require(report["workers"] == 8 and report["replay_passes"] == 3 and report["repetitions"] == 3,
            "Worker/pass/repetition policy changed")
    expected_variants = {(windows, chunks) for windows in (1, 2, 4, 8) for chunks in (8, 32)}
    require(len(report["variants"]) == 8 and
            {(v["preparation_batch_windows"], v["map_chunksize"]) for v in report["variants"]} == expected_variants,
            "Variant set changed")
    require(report["policy"] == dict(group_limit=2, logical_window_cells=256, workers=8,
        journal_buffer_records=8, journal_max_age_seconds=.25, ready_limit_single_window=2,
        ready_limit_multiwindow=1, prepared_item_max_bytes=12 * 1024**2,
        prepared_reservation_ceiling_bytes=48 * 1024**2,
        native_max_packet_positions=50000000, native_max_task_positions=10000000), "Pipeline policy changed")
    trials = report["trials"]
    require(len(trials) == 24 and
            {(t["preparation_batch_windows"], t["map_chunksize"], t["repeat"]) for t in trials} ==
            {(windows, chunks, repeat) for windows, chunks in expected_variants for repeat in range(3)},
            "Missing or duplicated matched trial")
    journal_total = record_total = batch_total = 0
    all_checkpoint_names = {name for name in names if name.endswith("/checkpoint.json")}
    used_checkpoints = set()
    for trial in trials:
        windows, chunksize = trial["preparation_batch_windows"], trial["map_chunksize"]
        require(trial["workers"] == 8 and trial["replay_passes"] == 3 and trial["unique_windows"] == 9
                and trial["window_visits"] == 27 and trial["requests"] == 69
                and trial["unique_logical_cells"] == 2304 and trial["logical_cell_visits"] == 6912
                and trial["verified_positions"] == 2327061582 and trial["regenerated_packet_bytes_match"]
                and trial["durable_recovery_passed"], "Incomplete repeated-input workload")
        require(math.isclose(trial["logical_cell_visits_per_second"], 6912 / trial["pipeline_seconds"], rel_tol=1e-12),
                "Trial throughput differs")
        require(trial["dispatch"]["calls"] == math.ceil(27 / windows)
                and trial["dispatch"]["submitted_segments"] == 3456, "CPU dispatch omitted/duplicated work")
        require(all(trial["queue"][key] == 0 for key in ("ready", "inflight", "active", "outstanding"))
                and trial["queue"]["preparation_batch_windows"] == windows
                and trial["queue"]["peak_reserved_bytes"] <= 48 * 1024**2
                and trial["queue"]["maximum_prepared_payload_bytes"] <= 12 * 1024**2,
                "Preparation queue did not drain within bounds")
        require(trial["queue"]["ready_limit"] == (2 if windows == 1 else 1), "Derived ready policy changed")
        tag = f"windows-{windows}-chunks-{chunksize}-repeat-{trial['repeat']}"
        require(trial["variant"] == f"windows-{windows}-chunks-{chunksize}", "Variant label differs")
        trial_points = trial_requests = 0
        for pass_index in range(3):
            trial_name = f"{tag}-pass-{pass_index}"
            prefix = f"results/{report['journal_directory']}/{tag}/pass-{pass_index}/"
            checkpoint_names = sorted(name for name in all_checkpoint_names if name.startswith(prefix))
            require(len(checkpoint_names) == 3, "Missing pass-specific region journals")
            seen_windows = set()
            points = requests = 0
            for checkpoint_name in checkpoint_names:
                used_checkpoints.add(checkpoint_name)
                checkpoint = json.loads(data[checkpoint_name])
                identity = checkpoint["identity"]
                require(identity == dict(TEST_ONLY=True, binary_sha256=report["binary_sha256"],
                    source_identity=report["source_identity"], trial=trial_name, workers=8,
                    preparation_batch_windows=windows, map_chunksize=chunksize, replay_pass=pass_index),
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
            require(seen_windows == set(expected_windows) and points == 775687194
                    and requests == 23, "Incomplete replay pass")
            trial_points += points
            trial_requests += requests
        require(trial_points == trial["verified_positions"] and trial_requests == trial["requests"],
                "Incomplete trial journal set")
    require(used_checkpoints == all_checkpoint_names and journal_total == 216 and record_total == 648
            and batch_total == 1656, "Unexpected durable receipt count")
    metrics = {}
    for windows, chunksize in sorted(expected_variants):
        key = f"windows-{windows}-chunks-{chunksize}"
        selected = [trial for trial in trials if trial["variant"] == key]
        median = lambda function: statistics.median(function(trial) for trial in selected)
        metrics[key] = dict(pipeline_seconds=median(lambda t: t["pipeline_seconds"]),
            logical_cell_visits_per_second=median(lambda t: t["logical_cell_visits_per_second"]),
            wait_for_preparation_seconds=median(lambda t: t["queue"]["consumer_wait_empty_seconds"]),
            kernel_seconds=median(lambda t: t["stages"]["kernel_seconds"]),
            map_calls=selected[0]["dispatch"]["calls"],
            map_wall_seconds=median(lambda t: t["dispatch"]["map_wall_seconds"]),
            prepared_consistency_seconds=median(lambda t: t["stages"]["prepared_consistency_seconds"]),
            journal_flush_seconds=median(lambda t: t["journal_flush_seconds"]),
            maximum_prepared_payload_bytes=max(t["queue"]["maximum_prepared_payload_bytes"] for t in selected),
            observed_pipeline_seconds=[t["pipeline_seconds"] for t in selected])
        require(math.isclose(metrics[key]["pipeline_seconds"], report["summary"]["median_pipeline_seconds"][key],
                             rel_tol=1e-12), "Reported median differs")
    baseline = metrics["windows-1-chunks-8"]["pipeline_seconds"]
    for key, values in metrics.items():
        values["speedup_vs_matched_baseline"] = baseline / values["pipeline_seconds"]
        require(math.isclose(values["speedup_vs_matched_baseline"],
                report["summary"]["speedup_vs_matched_baseline"][key], rel_tol=1e-12), "Speedup differs")
    fastest = min(metrics, key=lambda key: metrics[key]["pipeline_seconds"])
    require(report["summary"]["fastest_tested_variant"] == fastest, "Fastest label differs")
    return dict(status="passed", original_zip_sha256=sha(Path(archive_path).read_bytes()),
        original_zip_bytes=Path(archive_path).stat().st_size, result_members=len(names),
        all_export_checksums_verified=True, source_and_input_identities_verified=True,
        native_binary_identity_matches_build=True, preflight_reported_passed=report["preflight"],
        journal_hash_chains_and_cursors_independently_verified=journal_total,
        original_window_visit_records_verified=record_total, native_receipts_matched_to_gmp_oracle=batch_total,
        certificate_identities_and_packet_identities_verified=True, gpu="NVIDIA L4", workers=8,
        variant_medians=metrics, fastest_tested_variant=fastest,
        practical_colab_followup="windows-4-chunks-8: nearly tied with eight windows, smaller prepared groups",
        eight_vs_four_throughput_ratio=metrics["windows-4-chunks-8"]["pipeline_seconds"] /
                                      metrics["windows-8-chunks-8"]["pipeline_seconds"],
        compute_unit_cost_available=report["compute_units_per_hour_observed_by_user"] is not None,
        production_changes=False, new_scientific_coverage=False,
        limitations=report["limitations"] + " One short Colab L4 session, three repetitions per policy. Batch four/eight sample ranges overlap; no global optimum or production speedup is established. No local GPU rerun.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-sources", type=Path, required=True)
    args = parser.parse_args()
    result = review(args.archive, args.bundle, args.sources, args.batch_sources)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
