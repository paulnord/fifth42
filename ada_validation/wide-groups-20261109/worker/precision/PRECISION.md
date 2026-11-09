# Adaptive geometry precision: isolated high-range experiment

## Result

Six selected patches in the actual denominator shell
`100000000001 <= c <= 200000000000`, width 8, passed three alternating
baseline/candidate preparation trials each. This is not a whole-shell search.

The four cap-42 patches at ratios approximately 0.3000, 0.3122, 0.5000, and
0.8500 changed root geometry precision from 222 bits to 88–96 bits.
Median preparation time fell by factors of 5.17, 4.60, 5.36, and 5.18.
The coefficient box sizes and exact hit sets were unchanged; no cap-42 hits
were found in those four patches. These are **cloud Python Fraction/exact LLL
microbenchmarks**, not ADA mpq/fpylll, CUDA, or end-to-end throughput results.

Two nonempty controls use scaled published Healy triples, with largest bases
122411574285 and 110321636000. Both were recovered; the entire enlarged-cap
hit sets (1 and 375 rows) matched. A separate monotonic integer-fifth-root
oracle checked a 5-by-5 neighborhood of each planted control. These controls
deliberately use residual caps larger than 42. They are not solutions to 42,
and their large constant caps are not dispatchable through the current
native packet's 64-bit cap field. They test host geometry and exact enumeration.

The controls showed 5.28x and 3.98x preparation ratios. Do not extrapolate any
of these ratios to the live search. Raw timings and all exact hits are in
`precision_results.json`; a preliminary single-pass sweep is in `probe.json`.

## What changes

The selected-high-range runner currently chooses
`max(48, 5*cmax.bit_length()+32)`, hence 222 bits. Its full-prefix path already
uses the much smaller `max(48, 2*cmax.bit_length()+16)`.

`precision_policy.py` chooses precision from the actual patch width and ratio,
then calls the original exact, outward-enclosing `make_patch`. It changes
neither fifth-power residual arithmetic nor the integer reduction certificate.
The original high precision remains the fallback outside the proved ratio
domain. No production file or active job was changed.

Do not use a fixed low precision everywhere: the curve is exceptionally flat
near ratio zero. This policy automatically uses 184 bits at the first patch
of the current high shell, 104 near ratio 0.01, 96 near ratio 0.3, and 88 near
ratio 0.85. The policy has no dependence on observed hits.

## Exact rounding-budget argument

Write `h=(right-left)/2`, `eta=cap/cmin^5`, and `p=(left+right)/2`.
For the current ratio domain `right<=9/10`, the center fifth root and its
lower dyadic bound are at least 1/2. A bits-bit root bracket has width at
most `2^-bits`. On `[1/2,1]`, the derivative magnitude of `t^-4` is at most
128. Therefore the two rounding contributions already included in make_patch
(center-root error and slope error) total at most

    (1/2 + 64*h) * 2^-bits.

The curvature-plus-residual thickness is at least

    lower = 2*right^3*h^2 + eta/5,

because the positive lower root bounds used in their denominators are at
most one. The policy selects a multiple of eight bits, at least 48, sufficient
to make the above rounding upper bound at most `lower/2^16`, unless the old
high precision is reached first. All comparisons are exact rational/integer
comparisons, not floating-point heuristics.

This margin controls extra enumeration, not correctness. Correctness still
comes from the original outward enclosure, exact `det(U)=±1`, exact `B=UA`,
the coefficient bounds, and exact residual arithmetic. Every alternative
precision must keep all certificate, work, and overflow guards. Tiny changes
to the enclosing region may change transforms and coefficient counts on other
patches. Do not require byte-identical certificates as a correctness test.

## Reproduce in this package

    python -m unittest -v test_precision_policy.py
    python precision_validate.py --repeats 3 --output precision_results.json

Use ordinary Python, not `python -O`: the frozen reference and the benchmark
use exact assertions. The test harness explicitly rejects optimized Python.
`reference_geometry.py` is the pinned reference (with one extra trailing newline, no code changes) from commit
`9a1ccf86eb8c8adae2e00e3cecbbb358345a0a45`, path
`lattice_gpu/reference/lattice5.py`. Its source identity is recorded in results.

## Bounded ADA test, before adoption

Run only in a separate worktree after checking available resources, without
changing the active weekend search, checkpoint, stop timer, or publisher.
Under the same pinned Python environment used by the existing implementation:

    python precision_validate.py --ada-source /absolute/path/to/lattice_prototype --repeats 5 --output ada_precision_results.json

This optional mode reuses the adjacent `lattice_gpu/scaling_core.py` initializer
and the pinned gmpy2/fpylll engine. It has not been executed in this cloud test.
It measures preparation and host exact enumeration, not a live CUDA pipeline.

For a native coordinator benchmark, retain the four production cap-42 patch
positions and add several actual 256-patch chunks around the current cursor.
Construct the candidate specification with the selected bits in each spec,
then use the normal `prepare_task`, `certify_task`, packing, independent GMP
checks, native bounds, counts, and source-identity guards unchanged. The
existing certification already reconstructs each task using its own `bits`.
Measure specification generation, geometry/reduction, certification, packing,
IPC, engine time, and total wall time. Compare exact hit sets, not raw work
counts. Wider-cap nonempty host controls above must not be sent as constant-cap
GPU packets; retain the existing supported nonempty device controls too.

Keep the tested candidate opt-in. A changed per-patch precision policy requires
a new source identity and coverage provenance; do not resume the frozen run
under different source files or silently relabel its journal.

## Historical comparison

Elkies's table reports most of a week on 500 MHz, using GP, for exponents
4 through 20 below 2^23, about 8.4 million. His paper separately forecasts
roughly one month for a C implementation on faster hardware reaching 10^9.
Neither is a measured 30-day/500-MHz result through 10^11. Healy's 2023 table
extends through 10^11 but publishes no corresponding CPU-day timing.

- https://people.math.harvard.edu/~elkies/ferm.html
- https://arxiv.org/html/math/0005139v1#S3.SS1
- https://aleph0.blog/2023/02/26/lattices-and-fermat-near-misses/
- https://www.alexhealy.net/papers/fermat/fermat.html
