# ADA lattice optimization validation — 2026-11-05

**PASS:** all bounded checks required by `ADA_OPTIMIZATION_HANDOFF.md` completed
with no failures, errors, skips, or timeouts.

Tested branch: `handoff/fifth-lattice-optimizations-20261105`.
Tested commit: `91bb89b0ff49974e9458faf19015908e44b85cb8`.
Run: `20261105T162350Z-n6kfxlij`, on ADA.

## Test results

| Suite | Passed | Time reported by unittest | Complete process wall time |
|---|---:|---:|---:|
| Core, audit, backends, and modular filters | 31/31 | 35.098 s | 35.333 s |
| Backend and modular tests under `python -O` | 14/14 | 16.688 s | 17.043 s |
| Isolated GMP mpq experiment | 5/5 | 0.044 s | 0.253 s |
| GMP tests under `python -O` | 5/5 | 0.043 s | 0.504 s |

All 20 upstream CPU/emulation runs across four comparison cases matched their
independent exact canonical hit sets. Compilation plus comparison took 2.259 s.
These comparisons used the retained published bound-1000 lattice results and
a fresh signed dictionary oracle; the bound-1000 lattice search was not rerun.

## Bounded smoke results

Each row below is one search sample, excluding interpreter startup and the
separate independent oracle. These are correctness smoke timings, not medians
or a production performance benchmark.

| Search | Search time | Result |
|---|---:|---|
| Reference signed bound 100 | 1.998313 s | Complete; no target-42 hits |
| SymPy signed bound 100 | 1.515214 s | Complete; no target-42 hits |
| fpylll signed bound 100 | 1.365063 s | Complete; no target-42 hits |
| fpylll modular extension, no filter, signed bound 100 | 1.368576 s | Complete; no target-42 hits |
| fpylll modular pruning, signed bound 100 | 0.190416 s | Complete; no target-42 hits |
| fpylll pruning, positive bound 34, residuals 12/384 | 0.078643 s | Both expected control hits |

The nonempty control recovered `(13,16,17,12)` and `(26,32,34,384)` under the
`a^5+b^5-c^5` residual convention. Independent exact oracles agreed with all
smokes. Reference, fpylll, modular smoke, and all upstream result semantics
matched the archived evidence after excluding timing fields.

## Environment and execution

ADA: Linux x86_64, kernel 7.0.0-38-generic, glibc 2.43. Python 3.12.4
(Anaconda build), g++ 15.2.0. Checks ran sequentially, with one-CPU affinity,
nice 19, native numerical thread counts set to one, and a 2 GiB address-space
limit per process. Smoke commands had 60-second process limits; test and
comparator commands had 300-second limits, with a five-second termination grace.

Pinned dependencies: SymPy 1.14.0, fpylll 0.6.4, cysignals 1.12.5,
NumPy 2.3.5, and gmpy2 2.2.2; mpmath 1.3.0. Runtime libraries report
fplll 5.5.0, GMP 6.3.0, MPFR 4.2.1, and MPC 1.3.1.
See [pip-freeze.txt](pip-freeze.txt).

## Evidence and scope

[report.json](report.json) contains commands, exit codes, CPU/wall timings,
full smoke results and counters, environment, source hashes, and comparisons.
The [logs](logs/) are fresh outputs of this ADA run.
[upstream-comparison.json](upstream-comparison.json) contains all 20 fresh
compiled CPU/emulation outputs. The report's absolute workspace paths are
replaced with documented aliases; the unrelated local working-tree file list
is omitted. All numerical results and timing records are retained.

All 110 published package files were unchanged before and after validation.
The existing package, original source, and compiled-experiment manifests passed
109, 95, and 12 entries, respectively. Their outputs are in
[package-checksums](package-checksums/); all tested package hashes are in
[tested-package-sha256.json](tested-package-sha256.json). This report directory
is outside `lattice_prototype/`, preserving its existing manifest scope.
Run `sha256sum -c SHA256SUMS` here to verify these report artifacts.

Production code and running jobs were preserved. No GPU execution, full timing
campaign, larger lattice search, or production search was launched. These small
checks add no production search coverage. The GMP checks validate exactness and
isolation; they do not establish a new ADA GMP search speedup.

The next step requires a separately agreed wall-time/resource cap for repeated,
paired timing comparisons at identical domains. Separate historical benchmark
ratios must not be multiplied into a promised production speedup.
