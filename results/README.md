# Compact results

[`gpu-B70000000.json`](gpu-B70000000.json) summarizes the completed overnight
192-bit GPU search: no solutions in the full signed box with bound 70,000,000.
It records row/step counts, completion and exit status, timestamps, separate GPU,
engine and job timings, ADA's CPU/core/RAM/GPU specifications, and verification
evidence with source/binary and checkpoint hashes. See [coverage](../COVERAGE.md).

`coverage.json` contains independently checked summaries of earlier baseline
run states: exact bounds, completed row prefix, step counts, timings, candidate lists and
relative-path source/binary SHA-256 fingerprints. Full boxes and partial prefixes
are explicitly distinguished. An empty solution list for a partial prefix is
not a statement about the whole configured box.

`optimization-validation.json` describes the isolated candidates' validation.
CPU emulation is not GPU validation, and no candidate speedup is claimed until
device benchmarking has passed.

The raw atomic checkpoints, generated binaries, local machine/driver identifiers,
large archives and profiler captures remain local and are ignored by Git. This
keeps the repository small. The summaries do not replace raw checkpoints for
resuming a run. On the original machine, refresh them without touching a running
job with `python3 scripts/export_results.py` (baseline summaries only).

## Cabbage saved-root test

The [2026-11-08 Cabbage report](cabbage-exact-root-reuse-20261108/README.md) records the pinned CPU reproduction, all 30 bounded CPU timing trials, and baseline CUDA controls. The [follow-up](cabbage-exact-root-reuse-20261108/followup/README.md) corrected the scratch range setup and passed baseline/candidate CUDA correctness plus 10 timing pairs, then stopped on an unrelated CPU resource conflict; the higher-cost timing window remains incomplete. This adds no production coverage and does not deploy the patch.

The [Cabbage admission preparation](cabbage-exact-root-reuse-20261108/readiness/README.md) completes the missing timing pairs and records actual NFS and 16-worker stop/cleanup checks. Production admission remains pending after an unrelated CPU conflict interrupted the coordinated cross-host probe.
