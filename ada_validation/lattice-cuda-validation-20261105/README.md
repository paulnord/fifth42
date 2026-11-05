# ADA CUDA lattice validation — 2026-11-05

**PASS:** the user ran `python3 ~/fifth-lattice-gpu/validate.py` in an ADA
terminal with CUDA device access after reboot. The saved run completed in
35.093 seconds. Eight host tests, the serial build,
and device correctness checks passed. This is bounded correctness evidence;
`speedup_demonstrated` remains false.

The checks covered 272 signed/cross-limb arithmetic pairs on each of CUDA,
ordinary CPU emulation, and sanitized CPU emulation; eight complete positive
domains through bound 1,000; nonempty controls; and two selected large fixture
patches. The large fixture checks do not establish complete shell coverage.
All backend coefficient counts match the certified boxes. There were
42 engine invocations, including 9 expected
nonzero exits for capacity and malformed-input checks.

## Bound-1,000 timing observations

All times are seconds. These are single validation observations, not medians.
CPU here means ordinary coefficient-box emulation, not the optimized direct
CPU solver used in the separate scaling comparison.

| Mode | Shared CPU preparation | CPU engine | CUDA engine | CUDA kernel | CPU total | CUDA total |
|---|---:|---:|---:|---:|---:|---:|
| constant | 8.657526 | 0.00476994 | 0.00156815 | 0.000252928 | 8.988329 | 9.302751 |
| healy | 8.535082 | 0.01021030 | 0.00153262 | 0.000262112 | 8.874239 | 9.153268 |

Total time includes shared preparation, the engine process, and exact host
verification. CUDA engine timing excludes process startup/context overhead;
kernel timing excludes host transfers and other engine work. The CUDA engine
was faster on these two samples, while total time was higher. The roughly
8.5–8.7 second host preparation dominates both backends. All samples, including
the sanitized backend, are in [timings.csv](timings.csv).

## Scope and next experiment

The tested GPU prototype is separate from the fpylll/pruning/GMP CPU experiment.
Its reference is pinned to `ddf28f04725b29b2f1d53b5d33c16379b0f66a20`.
The validator reused the saved CPU reproduction after verifying its freshness
receipt and regenerated output hashes. See [CPU_BASELINE.json](CPU_BASELINE.json).
This review checked all 16 executed source hashes against the saved workspace
and current source, plus report case counts and coefficient counts.

A suggested later timing experiment is complete domains at 2,000, 4,000, and
8,000 with one GPU, one host CPU, a ten-minute overall cap, and five paired
CUDA/emulation repeats where the cap permits. Prepare and certify each packet
once; retain preparation, kernel, process, and end-to-end measurements
separately, and independently verify exact hits and complete point counts.
This needs a separate guarded runner: the validated host planner currently
rejects full domains above 1,000 and limits packets to 4,096 tasks and
50 million coefficient points. Keep finite limits and record any explicit
changes. No larger CUDA run or automatic continuation was started here.

## Artifacts

The validator and device reports, build/test logs, source identities, and all
executed source files are retained here. The GPU model/driver was not captured
in this validator's report. GPU device access is unavailable to the Codex
sandbox; successful execution was performed in the user's ADA terminal.
Absolute local paths are replaced with `${GPU_WORKSPACE}`, `${GPU_RUN_DIR}`,
`${CPU_BASELINE_WORKSPACE}`, and related aliases. Original executed-source
hashes apply to local unredacted bytes; [SHA256SUMS](SHA256SUMS) checks the
published artifact bytes. Substitute actual paths before reusing a source copy.
