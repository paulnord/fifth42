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

The [2026-11-08 Cabbage report](cabbage-exact-root-reuse-20261108/README.md) records the pinned CPU reproduction, all 30 bounded CPU timing trials, and baseline CUDA controls. GPU testing stopped at the supplied engine's base-range guard before candidate comparison or paired GPU timing. This adds no production coverage and does not deploy the patch.
