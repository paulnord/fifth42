# ADA larger CUDA benchmark — 2026-11-05

**PASS:** all 30 timed trials completed: five alternating CUDA/CPU-emulation
pairs at 2,000, 4,000, and 8,000. Every decoded exact result matched an
independent unfiltered positive-domain oracle, and every task's complete
coefficient count matched its certified packet. Both nonempty controls passed
on CUDA, ordinary CPU emulation, and sanitized CPU emulation before timing.

The run took **248.407 seconds** of its ten-minute
allowance. CUDA subprocesses used 6.228
seconds of their separate cumulative 120-second allowance. The GPU was an
NVIDIA GeForce RTX 3080 Ti with 12,288 MiB and driver 595.99.02. The run used
one host CPU and one GPU after the CPU scaling benchmark released its lock.

## Median timings

Engine columns are milliseconds; total columns are seconds. Each median
uses five repeats. CPU here means ordinary coefficient-box emulation, a
different comparator from the optimized direct CPU solver in the scaling
reports.

| Bound | CPU engine (ms) | CUDA engine (ms) | CPU total (s) | CUDA total (s) |
|---:|---:|---:|---:|---:|
| 2,000 | 9.570 | 2.743 | 26.044 | 26.360 |
| 4,000 | 23.056 | 8.284 | 50.798 | 51.128 |
| 8,000 | 41.694 | 10.720 | 103.404 | 103.759 |

At 8,000, the CUDA engine was about 3.89 times faster than emulation. Total
CUDA time remained slightly higher. Host plan preparation and packet
certification took 100.048 seconds, and exact host verification took about
3.3 seconds per trial; those stages dominate the total. A CUDA process took
about 0.382 seconds including process/context startup, versus a 0.01072-second
engine time and a 0.000332-second kernel time. These measurements support
faster device enumeration, without an end-to-end speedup for this pipeline.

Each domain was prepared once. Total time charges its preparation cost once
to each trial's process-plus-verification time. Cached-packet timing excludes
that preparation. Every engine invocation starts a new process; kernel and
engine timing exclude process/context startup. All individual metrics are in
[samples.csv](samples.csv) and [results.json](results.json). Independent oracle
work is excluded from medians and included in the overall resource allowance.

## Coverage and verification

The domain was `1 <= a <= b < c <= bound` with
`abs(a^5+b^5-c^5) <= 42`. This is the earlier coefficient-box prototype,
separate from the newer fpylll/pruning/GMP lattice experiment. Patch counts
were 924, 1,846, and 3,690; coefficient counts were 1,519,384, 3,056,728, and
6,643,828. All three bounds found the same exact positive residual tuples:
`(1,1,2,-30)` and `(13,16,17,12)`. Neither is a signed target-42 solution.

The isolated benchmark planner extended the full-domain bound to 8,000.
The validated default planner and all 16 original validated source files
remain unchanged. Task, point, integer, exact-certificate, output, and coverage
guards were retained. Eleven host tests and the serial build passed.

Post-run review verified all 19 executed source identities, all binary hashes,
the isolated model and packet hashes, every raw trial hash, exact candidate
reconstruction and patch membership, every task count, repeated raw candidates,
all decoded hits against the independent oracle, and all reported medians.
The ordinary CPU and CUDA raw candidate sets were identical across all five
pairs at each bound. See [post-run-review.json](post-run-review.json).

## Artifacts and reproduction

[TERMINAL_INSTRUCTIONS.md](TERMINAL_INSTRUCTIONS.md) documents the installed
`python3 ~/fifth-lattice-gpu/benchmark.py --wait` runner and all limits.
The complete local run, including the large exact plans and every original
trial, remains at `${GPU_RUN_DIR}`. [local-artifact-manifest.json](local-artifact-manifest.json)
records every local file's original SHA-256 and size. Full plan files total
about 33 MB and are retained locally. This publication includes every trial's
timing and hash, the complete per-task counts without repeating identical
tables ten times, exact candidate summaries, independent oracle outputs,
source review transcripts, and build/test logs.

Absolute local paths and the GPU UUID are replaced with documented aliases.
Original hashes refer to local bytes; [SHA256SUMS](SHA256SUMS) verifies the
published artifact bytes. Source transcripts require actual paths and their
ordinary filenames before installation elsewhere. These results do not add
production search coverage or establish a CUDA win over the direct CPU solver.
