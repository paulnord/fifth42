# Exact cube coefficient pruning: isolated candidate

Status: passed bounded cloud tests on 2026-11-07. No ADA machine, active search,
GPU, remote branch, or production file was accessed or changed by this experiment.
This package proposes one host-side change to the published optimization code
at commit `9a1ccf86eb8c8adae2e00e3cecbbb358345a0a45`.

## Proposed change and proof

Apply `scaling_core_cube.patch` only in a new scratch checkout. It replaces the
sphere-derived symmetric coefficient bound in `coefficient_bounds` by the
smaller cube-derived bound. Preparation and certification both use that same
function. The kernel and packet format are unchanged.

Every valid original triple maps to a physical row vector x in [-1,1]^3.
For the exactly certified reduced row basis B=U*A, n=x*B^-1. Therefore

    |n_j| <= sum_i |(B^-1)_ij|,
    J_j = floor(sum_i |(B^-1)_ij|).

Floor is safe because n_j is an integer. Exact rational arithmetic is used.
By Cauchy-Schwarz, the cube bound cannot exceed the previous
ceil(sqrt(3*sum_i (B^-1)_ij^2)) bound. It may equal it on some patches.
It intentionally drops some points in the enclosing sphere that are outside
the original cube; preserving every sphere point is not a coverage requirement.
A simple identity basis changes the box from 125 points to its exact 27 cube
points, retaining all eight boundary corners.

All original basis, transform, integer overflow, point allowance, packet,
per-task enumeration count, exact residual and patch-membership checks remain.
Task hashes/counts naturally change because J and points are in the certificate.
Old and new raw candidate lists need not match: compare accepted exact hits for
the requested domain. Use a new source identity and run; do not resume a frozen
run with changed geometry/certificates.

## Reproducible tests

Run `./reproduce.sh` with an existing Python 3 and g++ installation. No package
installation is needed. `src/`, `vendor/`, `reference/`, and the original core
are the exact published bytes; `provenance.json` records hashes.

The actual patched core is tested through prepare, certify, assemble, packet,
unchanged native CPU emulation, and exact decode. Its dependency facade uses
the original exact Fraction LLL instead of unavailable GMP/fpylll. This does
not test the production GMP/fpylll environment or CUDA hardware.

Passed checks:

- 32 seeded rational bases, exhaustive preservation of 652 integer cube points.
- All eight cube corners, identity bound equality, singular/invalid matrices.
- Missing tasks and tampered J, point counts, precision, and certificate hashes
  fail closed in the actual patched core.
- Complete canonical positive domains at bound34/cap384, bound100/cap2951,
  bound1000/cap42, and Healy bound1000. Both old/new results match an independent
  exact fifth-power-table/bisect oracle, including nonempty controls and all ten
  Healy hits. This cap42 domain includes both signs needed by the unchanged
  target42 signed reduction; no new large signed-box coverage is claimed.
- Boundary fixture (9,9,10) and both published large fixtures are recovered.
  These are selected patches, not complete large-shell searches.
- Every bounded/native fixture test also passes UBSan; every task's actual count
  equals its own expected count and every returned coefficient is reconstructed.
- Python syntax compilation passes.

## Measurements and limits

Five alternating old/new engine-only trials, fixed width8, identical prepared
bases, exact original Fraction LLL, and the same unmodified CPU-emulation kernel.
These are small cloud measurements, not production-pipeline or ADA speedups.
Preparation, Python decoding, process startup and oracle work are not included
in the recorded native engine clocks. All samples are in `results.json`.

| Complete domain | Old box points | Cube box points | Reduction | Old engine median | New engine median |
|---|---:|---:|---:|---:|---:|
| bound34, cap384 | 275699 | 103901 | 62.3% | 0.001939 s | 0.000821 s |
| bound100, cap2951 | 589483 | 264247 | 55.2% | 0.004212 s | 0.002143 s |
| bound1000, cap42 | 4483388 | 1887678 | 57.9% | 0.035799 s | 0.016914 s |
| bound1000, Healy | 4835479 | 1930335 | 60.1% | 0.038957 s | 0.017376 s |

The two larger cases show 2.12x and 2.24x engine-only improvements in this final
run. First-run raw outputs are preserved separately and show timing variation.
The two selected large fixtures' points fall 10143 to 2535 and 105875 to 59409.
These ratios depend on the reduced basis and are not promises for fpylll/ADA.

## Recommended next checks, in order

1. Test this exact patch using the pinned GMP/fpylll stack on a separate,
   bounded work area. Compare old/new certificates and independently verified
   mathematical hit sets, not identical J/point counts.
2. Pair it with the separately tested outward-root precision policy. Recompute
   exact certificates from each variant's actual geometry. Test complete small
   domains, seeded high patches, boundary and large known-point controls.
3. Measure fresh-preparation end-to-end throughput, including certification,
   packing, engine, decoding and checkpoint cost. Use five alternating repeats
   and separate cold versus persistent timings. Report point counts alongside
   time. Do not multiply unrelated stage speedups.
4. Only after host/native tests pass, test CUDA and compare CPU/CUDA exact hits,
   every task's count, candidate reconstruction and overflow/output guards.
   Do not interrupt or compete with the currently running ADA search.

A later, more invasive candidate is asymmetric coefficient bounds exploiting
c/D in [C/D,1]. It requires a new packet/certificate version and is not included
or tested here. Wider/adaptive patches should be selected by fresh full-pipeline
measurements; width8 is already the published measured choice.
