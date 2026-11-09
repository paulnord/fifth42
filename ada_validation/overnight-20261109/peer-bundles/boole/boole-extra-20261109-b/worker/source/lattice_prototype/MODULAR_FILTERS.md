# Optional target-specific modular filtering

## Scope and use

`modular_filters.py` is a standalone experimental extension. It does not change
`lattice5.py`, its default search, or its coverage claim. `search_patch` takes an
explicit finite set of exact residual targets within a patch's residual cap and
supports `none`, `post`, and `prune`. It uses any existing certified LLL backend (reference, SymPy, or fpylll).
No production search, ADA run, or external publication was performed.

Run:

```
python -m unittest test_modular_filters -v
python benchmark_modular_filters.py > results/modular_filters_benchmark.json
```

All nine tests pass with the optional fpylll dependencies available. Nonempty controls recover both `(13,16,17,12)` and
`(26,32,34,384)`, including denominator and ratio boundaries, with every individual
modulus and the combined filter. An independent finite sphere set comparison,
negative coefficient checks, and fail-closed budget checks also pass. The suite
also checks full positive-domain nonempty targets 12/384, signed42 dictionary
equality through bound40, identical shell plans, and fpylll exact transform
certification. Empty
42 results are not used as the sole correctness test.

## Derivation and coverage

The original row basis is A and the reduced basis satisfies B=U A, with integer
unimodular U. Thus n B = (n U) A and the original coordinates are exactly

```
(c,a,b)_j = sum_i n_i U_ij.
```

For each modulus m, precompute fifth powers P_m(x). A target residual t requires

```
P_m(a) + P_m(b) - P_m(c) = t (mod m).
```

Because det(U)=+/-1, U is invertible modulo every m, including composite 25.
Consequently this change of coordinates loses no residue class. At the final
sphere-recursion level, n1 and n2 are fixed. The implementation computes all
allowed n0 residues by checking each integer 0 through m-1 after applying nU.
It rejects only coefficients outside that set. The exact Gram-Schmidt norm test
is unchanged for surviving coefficients, and exact residual equality remains
the final acceptance test. Therefore every original target hit survives.

With several targets the current implementation independently allows any target
residue at each modulus. Different moduli can match different targets, which
only admits extra false candidates. It cannot drop a true target hit. A future
shared-target bitmask could strengthen this without changing the argument.

`post` checks residues only after canonical-domain and patch membership checks,
before evaluating the full fifth powers. `prune` checks the last coefficient
before its rational norm test and before reconstruction/domain filtering. It
still iterates every outward-bound coefficient. Its `enumeration_nodes` retains
the reference accounting, including modular rejects, so the same resource guard
is conservative. `sphere_points` means emitted, residue-admissible points in
prune mode, not the whole sphere. `norm_tests` explicitly measures rational norm
work in prune mode (zero means uninstrumented in other modes).

`search_targets_positive` additionally covers the entire bounded positive
canonical domain, copying the reference constant-cap shell plan and exact
small-shell fallback. It accumulates counts and enforces global resource budgets;
a failed patch or exhausted budget cannot return a completed search.
`signed42_filtered` adds only the existing proved target42 signed reduction.
For target42,
search both residuals -42 and +42 and keep the existing finite signed exceptions
and proved reduction in COVERAGE.md. Do not infer a general full-signed reduction
for another target from this filter or these tests.

## Bounded measurements

`results/modular_filters_benchmark.json` records five repetitions per variant,
all results compared with the unfiltered reference patch oracle. Times include
basis reduction and cache construction; they are machine-local small-sample
measurements, not asymptotic estimates. Representative medians (milliseconds):

| Patch | None | Post 25/31/61 | Prune 25/31/61 |
|---|---:|---:|---:|
| Nonempty boundary, c=17..34 | 27.32 | 25.88 | 29.67 |
| Targets +/-42, c=64..127, a/c=0.7..0.8 | 1360.33 | 1492.23 | 124.12 |
| Targets +/-42, c=64..127, a/c=0.75..0.775 | 37.84 | 38.64 | 28.21 |

The medium patch visits 12,753 nodes in every mode. The combined prune variant
performs only 568 rational norm tests, rejects 12,185 final-coordinate choices,
and emits no points, versus 11,663 sphere points and 825 full-power tests in the
unfiltered run. Post-filtering also reduces full-power tests to zero, but does
not save expensive rational enumeration or reconstruction. The nonempty patch
has only 23 nodes and two accepted candidates, so filtering has little to save.
The apparent small timing differences in that patch should not be interpreted
as speedups. Individual prune medians on the medium patch are 287.45 ms (25),
200.72 ms (31), and 163.96 ms (61).

For target +42 alone the allowed residue triple counts are 750/15,625 (mod25),
900/29,791 (mod31), and 3,725/226,981 (mod61). Both signs double these counts.
These are exact finite counts, not assumed independent real-data rejection
rates. Actual geometry and suffixes determine the measured rejection rate.

## Congruence sublattices versus residue tests

The fifth-power constraint is nonlinear. Its solution set modulo m is a union
of residue classes, not generally one sublattice. For an admissible coefficient
class rho modulo m, all corresponding vectors are the affine lattice

```
(rho + m*z) B = rho*B + z*(m*B), z in Z^3.
```

Enumerating such a coset requires an exactly shifted sphere enumeration, not
simply using mB in the existing origin-centered sphere routine. Omitting the
shift would lose solutions. A CRT modulus M=25*31*61=47,275 is valid because the
moduli are coprime, but naïvely materializing all admissible cosets is costly:
for +42 there are 750*900*3,725 = 2,514,375,000 combined coefficient classes.
For exactly either sign there are twice that many. The current relaxed mixed-
target modular intersection would admit 20,115,000,000 classes. These counts
are invariant under a unimodular U; LLL does not remove the setup cost.

Recommendation: retain no filtering as the transparent default. Offer this
last-coordinate residue pruning as an opt-in for explicit residual targets,
then benchmark it on the actual patch geometry and integer sizes. Cache only
suffixes actually reached. Post-filtering is easy to audit but showed no timing
benefit at these small integer sizes. Do not prebuild the full CRT coset union.
Future optimizations could iterate intersected allowed arithmetic progressions
instead of all n0 values, or add shared-target bitmasks, but require separate
coverage tests and fair accounting. No timing here supports an estimate for
an unsearched large denominator range.

## Fast-reducer patch measurements

`results/modular_filters_fpylll_benchmark.json` uses fpylll with exact certification
of B=UA and det(U)=+/-1 before enumeration. Run with:

```
PYTHONPATH=../fifth_lattice_deps python benchmark_modular_filters.py --backend fpylll
```

Five-repeat medians including reduction and cache setup, in milliseconds:

| Patch | None | Post 25/31/61 | Prune 25/31/61 |
|---|---:|---:|---:|
| Nonempty boundary | 2.08 | 2.42 | 1.74 |
| Medium target42 | 1524.78 | 1385.40 | 108.92 |
| Narrow target42 | 18.10 | 14.88 | 2.53 |

The reduced bases in these cases produce the same node counts as the reference
backend. Exact arithmetic remains the enumeration authority; fpylll is used only
for a candidate basis whose integer transform is independently checked. These
patches show that pruning can complement a fast reducer, but a complete-shell
benchmark is needed to avoid selecting only favorable geometry.

## Complete bounded-domain comparison with fpylll

```
PYTHONPATH=../fifth_lattice_deps python benchmark_modular_full.py
```

Results are saved in `results/modular_filters_full_fpylll.json`. This exercises
all shells and all grid patches, including the direct small-shell fallback and
the finite signed exceptions. Every run equals the independent signed-box
dictionary oracle. Oracle computation time is outside the recorded search time.

| Full signed box | Repetitions | None | Post 25/31/61 | Prune 25/31/61 |
|---|---:|---:|---:|---:|
| [-100,100]^3 | 3 (median) | 2.084 s | 1.994 s | 0.310 s |
| [-1000,1000]^3 | 1 | 22.463 s | 24.223 s | 2.932 s |

The bound1000 result gives about 7.7x end-to-end improvement over the unfiltered
fpylll path in this single run. The bound100 median improves about 6.7x. This is
stronger evidence for practical pruning than the selected-patch timings, but
still says nothing about scaling beyond the recorded bounds. All variants find
no target42 solutions in those bounded boxes, and the separate nonempty controls
remain essential to verify that the filter does not reject everything.

The public entry points normalize iterable moduli once, so generator and tuple
inputs produce identical filters, counters and hit sets; a regression test
covers both patch and full positive-domain APIs. Filter `cache_entries` summed
across a full search is total construction work, not peak retained memory: each
patch releases its own suffix cache after completion.

Additional opt-in progression and exact interval modes are described in ENUMERATION_OPTIMIZATIONS.md; the measurements above retain the original none/post/prune comparison.
