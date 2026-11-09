# Current bounded adaptation results

This is an experimental cloud result, not an ADA benchmark or a production-search
recommendation. No ADA, GPU, production job, remote branch or main branch was
modified. See ADAPTATION.md for the exact baseline source identity.

## Published LLL integration

Three warm trials per row, same original exact patch covering and exhaustive
rational enumerator; medians in seconds. Every run matches an independent exact
oracle. Healy bound 1000 recovers all ten expected near misses.

| Domain | Bound | Original LLL | SymPy | fpylll |
|---|---:|---:|---:|---:|
| healy | 100 | 3.698 | 2.998 | 2.601 |
| healy | 1000 | 64.638 | 56.828 | 51.791 |
| signed 42 | 100 | 2.959 | 2.094 | 1.971 |
| signed 42 | 1000 | 32.557 | 22.668 | 20.798 |

The backend adapters clear one common denominator and independently certify the
integer unimodular transform before using the exact enumerator. Both selected
large fixture patches pass all three backends; these are not full-shell searches.

## Enumeration and compiled arithmetic

- Complete signed box through +/-1000, same fpylll reducer: original modular
  comparison unfiltered 22.463 s, post-filter 24.223 s, prune 2.932 s (one trial each).
  Every 463 patches and 198033 conservative enumeration nodes were accounted for.
- A later three-trial paired comparison: prune 2.361 s, progression 2.276 s,
  exact-integer-interval 3.082 s. Progression's modest difference is not sufficient
  evidence for a default change. Exact interval is correct but slower than
  modular prune here; without modular filters it took 3.154 s.
- Paired compiled-rational experiment, five trials: prune Fraction 2.413 s to
  GMP mpq 1.286 s; interval Fraction 3.123 s to mpq 1.826 s. Exact geometry, counters,
  result sets and independent signed oracles match. Nonempty 12/384/2951
  controls pass. This is isolated snapshot code, not a global/default switch.
- Certified uniform patch widths 1/2/4/8 with interval mode:2.540/2.932/5.250/9.565 s.
  Wider patches have fewer reductions but more enumeration work. All exact
  oracles and nonempty 2951 controls pass. These do not establish an optimal
  large-range patch width.

## Validation and limits

31 current-core tests pass;14 optional-backend/modular tests also pass under
python -O. Frozen upstream GMP CPU and GPU-row CPU emulation comparison passes
all 20 runs. Compiled arithmetic has its own additional test/evidence record.
Negative coefficients, inclusive rational boundaries, nonempty hits, invalid
transforms and exhausted budgets are tested. Original complete coverage and
selected large-patch coverage are deliberately distinguished.

Times are exploratory cloud measurements, not dedicated-host performance
claims; some validation work ran concurrently. Separate experiments have their
own baselines, so ratios should be taken from paired rows, not multiplied into
a promised production speedup. Native reduction timeouts remain cooperative.
No inference is made about the unsearched large-denominator domain.

The preferred next engineering candidate is fpylll reduction plus exact modular
pruning, with compiled rational arithmetic evaluated separately. Preserve the
reference path and conservative guards. Do not replace the existing production
search or materialize the billions of nonlinear CRT cosets.
