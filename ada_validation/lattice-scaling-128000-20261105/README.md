# ADA CPU comparison at bound 128,000 — 2026-11-05

**PASS:** five alternating paired repeats completed. Every lattice and direct
CPU result matched the independent complete signed-box oracle for
`x^5+y^5+z^5=42`, modulo permutations. The reported signed solution set is
[].

The user's requested limit extension raised the lattice trial allowance from
120 seconds to **300 seconds**, and the overall run allowance from 600 seconds
to **1,200 seconds**, so the five pairs could finish. This run requested only
128,000; it did not redo the completed 64,000 step or start 256,000. Actual
coordinator elapsed time was **849.121 seconds**.

## Median timings

All values are seconds. Medians summarize five paired repeats, alternating
the order of the two methods.

| Bound | Lattice preparation + search | Direct CPU setup + search | Direct CPU full process wall | Warm-time gap |
|---:|---:|---:|---:|---:|
| 128,000 | 144.603112 | 2.814974 | 2.821479 | 51.37x |

Lattice uses the same isolated GMP mpq arithmetic, fpylll reduction, and exact
modular pruning as the previous scaling reports. Direct CPU uses the unchanged
native 128-bit production solver with its modulo-11 filter and production
compiler flags, rebuilt in scratch. Independent oracles, imports, separate
geometry checks, and result serialization are excluded from these medians.
Direct process wall time is recorded separately from its internal setup/search
clocks. All trials are retained in [samples.csv](samples.csv).

## Exact checks, limits, and provenance

The independent signed native 128-bit oracle enumerates sorted x <= y <= z
over the entire signed box without modular filters or shared lattice code.
It passed 44 Python oracle controls and matched all five hash-verified archived
unfiltered GMP oracle results at 2,000 through 32,000. Separate nonempty
controls for residuals 12/384 and 2951 passed with both arithmetic paths and
both CPU binaries before the larger comparison.

All 58,988 patch enclosures, bases, exact reduction
transforms, and Gram–Schmidt values matched between Fraction and GMP. The
geometry transcript hash also matches the previous 128,000 attempt that
stopped at 120 seconds. Post-run review rechecked every trial hash and result,
recomputed the medians, and verified repeated lattice outputs and counters.

The finite 500-million-node and 150,000-patch allowances are unchanged from
the preceding continuation. The run used one logical CPU, nice 19, one
numerical-library thread, and a 2 GiB address-space cap per process. Active
production state, job locks, memory, CPU load, and the GPU validator lock were
monitored. The source package, production CPU sources, and production checkout
status were preserved. No GPU workload or production search was launched.

The lattice source remains pinned to
`91bb89b0ff49974e9458faf19015908e44b85cb8`, and production native source to
`853fd98fc91968987fcb3e9e4c43b4fe880c8246`. This bound is within previously
completed production coverage and adds performance evidence only. The direct
CPU solver remains faster at this measured point; no crossover is projected.

Commands, environment, source/binary identities, and all repeats are in
[report.json](report.json). Executed sources are review transcripts under
[executed-code](executed-code/). Absolute local paths are replaced with
`${RUN_DIR}`, `${CPU_BENCHMARK_WORKSPACE}`, `${EVIDENCE_CHECKOUT}`, and related
aliases. Original source/result hashes refer to local unredacted bytes;
[SHA256SUMS](SHA256SUMS) checks the published artifact bytes.
