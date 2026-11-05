# ADA paired CPU benchmark — 2026-11-05

**PASS:** five paired repetitions at each complete signed bound, 100 and 1,000.
All exact-oracle, geometry, counter, and nonempty-control checks agreed.

The optimized lattice path improved substantially, but the existing native CPU
solver was faster at both measured bounds. These results support retaining the
direct solver while investigating the remaining lattice implementation costs.
No crossover or larger-bound performance has been established.

## Medians

Warm computation time includes preparation and search, with imports and the
independent correctness oracle recorded separately. Every raw sample is in
[samples.csv](samples.csv); all medians are in [medians.csv](medians.csv).

| Implementation | Bound 100 | Bound 1,000 |
|---|---:|---:|
| fpylll, Fraction, unfiltered | 1.326475 s | 13.811528 s |
| fpylll, Fraction, modular pruning | 0.189921 s | 1.599154 s |
| fpylll, GMP mpq, modular pruning | 0.109222 s | 0.918120 s |
| Production native 128-bit CPU, setup + search | 0.000006312 s | 0.000228759 s |
| Native CPU including process launch and output capture | 0.004516 s | 0.006862 s |

At bound 1,000, pruning improved the Fraction lattice path by 8.64x, and GMP
improved the pruned path by a further 1.74x. The directly measured combined
comparison was 13.811528/0.918120 = 15.04x. These are ratios from this same paired
experiment, not products of historical benchmark ratios.

The direct solver remained about 4,013x faster in warm setup-plus-search time,
and about 134x faster even when its process-launch/output overhead is included.
Its native setup/search timings are very short; all five samples and the
complete process times are retained. Python startup is excluded from the
lattice timings. The comparison measures the current implementations, including
language differences, and does not establish asymptotic scaling.

## Work and correctness

Every timed call searched the full signed target-42 box at the stated bound,
modulo permutations. No target-42 solutions were found. The direct solver used
its proven modulo-11 filter. All lattice variants used fpylll 0.6.4 and the
same exact covering, with conservative node budgets preserved.

For every paired round, pruned Fraction and GMP outputs and all counters matched
exactly after removing elapsed time. Unfiltered and pruned variants had the same
shell plans, patch counts, conservative enumeration-node counts, and direct
fallback counts. Exact geometry, reduced bases, unimodular transforms, and
Gram–Schmidt data agreed across Fraction and GMP: 58 patches at bound 100 and
463 at bound 1,000. Their normalized transcript hashes are in the report.

Separate correctness controls recovered positive residuals 12/384 through bound
34 and residual 2951 through bound 100, with all three lattice variants. The
native CPU solver also matched independent, nonempty full-signed oracles for
those three targets. The positive control domains and signed control domains
are labeled separately; they are not mixed into the target-42 timing table.
The default lattice modules remained unchanged in the GMP experiment.

## Setup, limits, and provenance

ADA, one logical CPU, nice 19, numerical libraries limited to one thread,
2 GiB address-space limit per process. The original ten-minute deadline was
preserved across a harness correction. An initial check assumed an optional
metadata field in the native CPU output and stopped before timed trials.
The corrected attempt completed in 95.299 s; total time from the original budget
start, including diagnosis and restart, was 178.289 s. No deadline was renewed.
The initial attempt and explanation are retained under [initial-attempt](initial-attempt/).

Python/native imports and private engine construction took 0.074296 s; reducer
warmup took 0.000288 s. Native compilation took 0.507 s wall / 0.473 s CPU.
Geometry verification and oracle timings are recorded separately per case.
No profiling run was added.

Python 3.12.4; SymPy 1.14.0; fpylll 0.6.4; cysignals 1.12.5;
NumPy 2.3.5; gmpy2 2.2.2. Native libraries: fplll 5.5.0, GMP 6.3.0,
MPFR 4.2.1, MPC 1.3.1. See [pip-freeze.txt](pip-freeze.txt).

Lattice source commit: `91bb89b0ff49974e9458faf19015908e44b85cb8`.
Native CPU source commit: `853fd98fc91968987fcb3e9e4c43b4fe880c8246`.
The direct baseline was copied from production `src/search_cpu.cpp`,
`src/search_common.hpp`, and `src/exact.hpp`, then built in scratch with
`g++-13 13.4.0 -O3 -std=c++17 -Wall -Wextra -Wconversion`, matching its Makefile.
It uses native signed 128-bit arithmetic; it is distinct from the GMP CPU oracle
used in the earlier 20-run validation comparison. These bounds are safely within
its established arithmetic range.

## Evidence

[report.json](report.json) contains commands, limits, environment, source hashes,
all 40 timing samples, all medians, geometry hashes, controls, and preservation
checks. [trials](trials/) retains each complete raw trial result.
[executed-harness.txt](executed-harness.txt) contains the executed harness for
review, with absolute host paths replaced by the aliases documented in the
report. It is a transcript; substitute real paths before executing a copy.
The original executed-file hash is retained in the report.
Run `sha256sum -c SHA256SUMS` in this directory to verify the report artifacts.

All 110 tested package files, production CPU sources, and production working-tree
status were preserved. No GPU workload or search above bound 1,000 was launched
by this benchmark. A larger search requires separate measurements and budgeting.
