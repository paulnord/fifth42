# ADA stepped lattice/direct comparison — 2026-11-05

**PASS:** five alternating paired repeats completed at each of 2,000, 4,000,
8,000, 16,000, and 32,000. All 50 timed trials matched an independently executed,
unfiltered exact GMP CPU oracle. All reported domains are complete signed
boxes for `x^5+y^5+z^5=42`, modulo permutations. No solutions were found.

The measured gap narrowed at every doubling. The direct CPU solver remains
faster throughout the measured range; no crossover is inferred or projected.

## Median timings

All values below are seconds. Lattice is fpylll plus modular pruning and the
isolated GMP mpq arithmetic path. Direct is the unchanged production native
128-bit CPU solver, rebuilt in scratch with its production flags and modulo-11
filter. Each row summarizes five paired repeats, alternating which runs first.

| Bound | Lattice preparation + search | Direct setup + search | Direct full process wall | Warm-time gap |
|---:|---:|---:|---:|---:|
| 2,000 | 1.774773 | 0.000787298 | 0.005455 | 2254.26x |
| 4,000 | 3.339916 | 0.002928892 | 0.007877 | 1140.33x |
| 8,000 | 6.400963 | 0.011309106 | 0.017409 | 566.00x |
| 16,000 | 12.671225 | 0.045307141 | 0.051762 | 279.67x |
| 32,000 | 26.525404 | 0.177345518 | 0.182999 | 149.57x |

The lattice time includes rational patch construction, certified LLL, exhaustive
filtered enumeration, and signed-result reconstruction. Imports, independent
oracles, exact geometry comparison, output serialization and validation are
outside those timed calls. Direct setup/search comes from the executable's
own clocks; complete invocation/output wall time is also retained. Python
startup is excluded from the lattice timings.

The observed gap falls from roughly 2,254x to 150x over these steps. This measures
the current implementations and their language/runtime differences. No curve
fit or extrapolated crossover is supplied. All individual samples and medians
are in [samples.csv](samples.csv) and [medians.csv](medians.csv).

## Independent checks and work counts

The oracle is a separately compiled frozen arbitrary-precision GMP direct
search, using `--filter none` and every signed z row at the requested bound.
It is separate from the timed native 128-bit baseline and the lattice's signed
reduction and modular filters. Every reported hit is independently checked
with Python integer fifth powers, and every result set is compared with the
complete oracle. Oracle time is excluded from timing medians.

| Bound | Planned lattice patches | Conservative enumeration nodes | Oracle process wall |
|---:|---:|---:|---:|
| 2,000 | 924 | 397,924 | 0.301 s |
| 4,000 | 1,846 | 796,232 | 1.177 s |
| 8,000 | 3,690 | 1,698,260 | 4.760 s |
| 16,000 | 7,377 | 4,187,553 | 19.279 s |
| 32,000 | 14,750 | 12,803,536 | 78.183 s |

Every planned patch's rational enclosure, original/reduced bases, integer
unimodular transform, and Gram–Schmidt values matched between Fraction and GMP.
The comparison streams normalized records to avoid retaining large transcripts;
the newline-delimited transcript hash and serialization are recorded per step.
Each measured lattice result accounted for the expected patch count. Across
all five repeats, outputs and counters were identical after removing elapsed
time. Raw results and hashes are retained under [trials](trials/) and
[oracles](oracles/); [post-run-review.json](post-run-review.json) records the
independent post-run checks.

Separate nonempty controls recovered positive residuals 12/384 through bound 34
and residual 2951 through bound 100 with Fraction and GMP lattice arithmetic,
including equal exact counters. Both CPU binaries matched independent Python
signed dictionary oracles for those nonempty targets. The default modules
remained unchanged.

## Budget and environment

The same one-CPU, ten-minute resource cap was retained for this stepped run.
Actual coordinator elapsed time was **400.523 seconds**. No deadline was renewed
and no automatic continuation was installed. The largest configured point was
32,000; no work above that bound was launched by this sweep.

Resource limits: one logical CPU, nice 19, numerical-library threads limited to
one, 2 GiB address space per process. For these larger requested boxes, each
lattice call explicitly used a finite 20-million-node allowance and the existing
20,000-patch ceiling, with a 120-second per-call guard. These are explicit
configuration values; the defaults and fail-closed implementation remain
unchanged. Independent oracle processes had a 180-second ceiling, inside the
same 600-second overall watchdog. The run also checked production locks, CPU
load, memory availability, and the GPU validator lock, yielding if existing
work resumed. No GPU workload was launched by this CPU benchmark.

Python 3.12.4; SymPy 1.14.0; fpylll 0.6.4; cysignals 1.12.5;
NumPy 2.3.5; gmpy2 2.2.2. Native libraries: fplll 5.5.0, GMP 6.3.0,
MPFR 4.2.1, MPC 1.3.1. See [pip-freeze.txt](pip-freeze.txt).
Both CPU programs were compiled serially with g++-13 13.4.0 and
`-O3 -std=c++17 -Wall -Wextra -Wconversion`; the oracle also linked GMP.

Lattice source: `91bb89b0ff49974e9458faf19015908e44b85cb8`.
Production native source: `853fd98fc91968987fcb3e9e4c43b4fe880c8246`.
The oracle uses the frozen `lattice_prototype/vendor/` sources. All 110 tested
package files, production CPU sources, and production working-tree status were
preserved. These boxes are within the previously completed 70-million direct
search result; this is performance evidence, not additional production coverage.

## Artifacts

[report.json](report.json) contains all commands, bounds, limits, setup and
verification timings, complete control results, samples, medians, source and
binary hashes, and preservation checks. Executed code is retained as review
transcripts under [executed-code](executed-code/), with absolute host paths
replaced by documented aliases; substitute actual paths before executing a
copy. Original local hashes are retained, with separate artifact checksums for
the published, redacted files.

Run `sha256sum -c SHA256SUMS` in this directory to check these report artifacts.
