# ADA further CPU doublings — 2026-11-05

The requested continuation started at 64,000 under one new **600-second total
allowance**, one logical CPU, nice 19, one numerical-library thread, and
2 GiB address space per process. Actual elapsed time was
**579.460 seconds**. Raw coordinator status:
`stopped_at_guard`; worker status: `stopped_at_guard`.

## Completed five-pair comparisons

All values are seconds, using five alternating paired repeats per completed
point. Lattice means fpylll plus exact modular pruning and isolated GMP mpq.
Direct means the unchanged native 128-bit production solver, rebuilt in scratch
with its production flags and modulo-11 filter. Medians exclude independent
oracles, geometry checks, imports, and serialization. Direct process wall time
is retained separately from its setup/search clocks.

| Bound | Lattice preparation + search | Direct setup + search | Direct process wall | Warm-time gap |
|---:|---:|---:|---:|---:|
| 64,000 | 58.983684 | 0.713863 | 0.720305 | 82.63x |

Each recorded completed trial matched an independent full signed-box exact
oracle, modulo permutations. No crossover is inferred beyond measured points.
All samples are in [samples.csv](samples.csv); only steps with five complete
pairs appear in [medians.csv](medians.csv).

## Stopped or unstarted work

- Bound 128,000: phase `paired_repeats`, 0 completed lattice trials and 0 completed direct trials.

Configured bounds not started: 256,000.
Partial points have no five-pair median and are not reported as completed
benchmark levels. The final guard/error is recorded verbatim in
[report.json](report.json) and [scaling-results.json](scaling-results.json).
No deadline was renewed, no automatic continuation was installed, and no
production search was started.

## Exact verification and changed harness limits

The previous unfiltered GMP oracle took 78 seconds at 32,000; repeating it
at each larger point would consume the timing allowance. This continuation
uses a separately written, unfiltered signed `__int128` oracle instead.
For every largest coordinate z in [-B,B], it searches x <= y <= z with exact
two-pointer sums. Sorting removes permutations only; every signed solution has
exactly one sorted representative. Powers are formed by five integer
multiplications, with no lattice code, shared production headers, or modular
filters. At the oracle's hard bound of 1,000,000,
3*B^5 + 2^63 < 2^127, so signed 128-bit intermediates cannot overflow.

The independent oracle passed 44 Python dictionary-oracle cases including
zero/negative targets and repeated coordinates. It also matched all five
hash-verified archived unfiltered GMP oracles at 2,000 through 32,000.
Nonempty positive controls 12/384 and 2951 passed with Fraction and GMP lattice
arithmetic and both CPU programs. All patches' exact bases, certified transforms,
and Gram–Schmidt values were compared between Fraction and GMP before each
timed level. Post-run review verified every recorded trial hash, exact result
set, repeated lattice counters, completed-point median, and executed code hash.

Larger boxes explicitly use finite limits of **500 million enumeration nodes**
and **150,000 patches** per lattice call. The per-call time guard remains
120 seconds and all work, including compilation and oracles, shares the
600-second coordinator watchdog. Limits fail closed. No library defaults,
production sources, or original evidence were edited. Production job locks,
the GPU validator lock, CPU load, and memory were monitored throughout.

The lattice package remains pinned to
`91bb89b0ff49974e9458faf19015908e44b85cb8`; production native source is
`853fd98fc91968987fcb3e9e4c43b4fe880c8246`. The package hashes, production CPU
sources, and production working-tree status were preserved. This experiment
uses the same Python/package pins as the preceding scaling report, recorded
in [pip-freeze.txt](pip-freeze.txt). These domains are within previously
completed production coverage; they add timing evidence only.

## Artifacts

Raw results, successful trial files, exact oracles, commands, guard outcomes,
and original code hashes are retained. Executed code is included as text
transcripts under [executed-code](executed-code/). Absolute local paths are
replaced by `${RUN_DIR}`, `${VALIDATION_WORKSPACE}`, `${VALIDATION_PYTHON}`,
`${EVIDENCE_CHECKOUT}`, `${PRODUCTION_CHECKOUT}`, and `${USER_HOME}` aliases.
Original hashes refer to unredacted local bytes; [SHA256SUMS](SHA256SUMS) checks
the published bytes. Substitute actual paths before reusing a code transcript.
