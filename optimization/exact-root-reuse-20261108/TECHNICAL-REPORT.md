# Fifth42: reuse an exact root already calculated

**Reviewable patch, tested in an isolated cloud workspace. Not deployed.**

The patch reuses one lower fifth-root bound inside `make_patch` when an exact
comparison proves that the second root would have the same value. Otherwise it
runs the original calculation. It changes two matching source/snapshot files,
with no floating-point approximation, cross-patch cache, skipped certificate,
or change to the mathematical search domain.

## Measured result

Five alternating baseline/candidate pairs used the deployed pinned GMP/fpylll
stack, fresh preparation, four allowed cloud CPUs, one persistent native CPU
engine, bounded prefetch, exact output verification, a first-chunk independent
GMP audit, and the existing durable journal/checkpoint plus recovery checks.

| Selected ratio window | Patches per trial | Baseline median | Patched median | Throughput ratio |
|---|---:|---:|---:|---:|
| Boole's initial ratio | 4,096 | 3.0284 s | 2.8242 s | 1.072x |
| Ada's initial ratio | 4,096 | 3.0069 s | 2.8381 s | 1.059x |
| Higher enumeration cost | 1,024 | 2.4370 s | 2.4150 s | 1.009x |

Every paired task/certificate/geometry/packet signature, coefficient count and
exact hit set matched. All five Ada-ratio pairs favored the patch by 4.6–6.3%.
One Boole baseline trial had a scheduling outlier; all raw samples are retained.
The ~1% high-cost result is small and should not be treated as a reliable GPU
gain. Earlier geometry-only results are not the full-pipeline result above.

**These are cloud CPU measurements, not Ada/Boole CUDA or NFS measurements.**
Startup and shutdown are recorded separately. No services, publishers, shared
allocator, storage limit, live journal or active search was changed. No new
production coverage is claimed. Do not multiply these ratios by earlier gains.

## Exact argument

Let d=2^bits, x=1-right^5, eta=cap/cmin^5, and L=n/d be the existing lower root
of x. The original routine guarantees L^5 <= x < ((n+1)/d)^5. Domain guards
give eta>=0 and y=x-eta>0. If L^5<=y, then

    L^5 <= y <= x < ((n+1)/d)^5,

so the exact dyadic floor fifth root of y is also L. Equality is deliberately
included. If the comparison fails, the unchanged root routine handles y.
Fraction and GMP rational arithmetic both evaluate the comparison exactly.
The discarded upper root is never used by `make_patch`.

This is reuse within a single patch construction. Preparation and independent
certification still each construct their own patch; nothing is trusted from an
earlier certificate or task. The same immutable fields, basis, coefficients,
canonical hashes and packets result. The fallback branch adds a comparison,
so a fallback-only workload may be slightly slower.

## Validation

- 142 tests passed: six new exact-reuse tests, 107 coordinator/native-package
  regressions, 24 lattice/backend/filter tests, and five compiled-GMP tests.
- New tests cover Fraction and GMP, 4,000 seeded random rational root pairs,
  exact dyadic boundaries and one-sided crossings, zero cap, both branches,
  invalid inputs, low precision, native guard parity, exact task/certificate/
  packet identity and tampering rejection. A source-diff allowlist checks that
  only the intended two identical edits exist and match the supplied patch.
- Baseline and candidate have 16 identical native validation case records:
  full positive domains at bound34/cap384, bound100/cap2951, bound1000/cap42,
  and five selected high-shell windows, each under CPU and UBSan.
- Nonempty small-domain results match an independent fifth-power-table oracle.
  Native counts and full candidate records also match the independent GMP
  implementation. Larger-window tests are not a full-shell oracle.
- All 30 measured pipeline trials passed exact comparison and durable-prefix
  recovery. Independent review found no correctness defect.

## Reproduce without touching production

Requirements: an existing Python3.12 environment with sympy1.14.0,
fpylll0.6.4, cysignals1.12.5, numpy2.3.5 and gmpy2 2.2.2; g++, make, patch,
sha256sum and GMP C++ development headers/libraries. No CUDA is required.
The reproduction script does not install anything or start services.

From the extracted package, choose a **new, nonexistent** scratch directory:

    sh reproduce.sh /absolute/new/scratch /absolute/pinned/python

To additionally repeat the 30 bounded timing trials:

    sh reproduce.sh /absolute/other/new/scratch /absolute/pinned/python --benchmark

The script verifies package hashes, reconstructs a candidate from the exact
baseline, applies the patch, rebuilds CPU/UBSan/GMP tools, and runs the tests.
No compiled binaries or virtual environment are distributed. Archived results
are in `results/`; new results are written only in the chosen scratch directory.

## Integration boundaries

Base: commit `da4e1e312ce1558c9d8cf027c009f8b400f22b83`, directory
`deployment_snapshots/weekend-20261107/ada/worker` in paulnord/fifth42.
The same root source was deployed on Ada and Boole. `upstream-files.json` and
`source-verification.json` document retrieved source identities.

Apply `reuse-exact-lower-root.patch` from the root of a **new worker copy**,
not the repository root and not a running source tree. The patch paths are:

- source/lattice_prototype/lattice5.py
- source/lattice_prototype/compiled_experiment/lattice5_snapshot.py

The normal initializer loads the compiled-experiment snapshot, which is why
both copies are patched. Existing processes cache their engine and must not be
hot-patched. `CANDIDATE-SOURCE-MANIFEST.json` identifies the tested candidate
source subset, not a deployable release. Historical manifest/hash files in the
reference tree remain historical evidence; do not use them to authenticate a
modified runtime. A production release needs refreshed source/binary identities,
bounded CUDA and NFS/ledger acceptance tests, and an authorized fresh run.
Do not resume the frozen active journal under a silently changed identity.

Pinned source:
https://github.com/paulnord/fifth42/tree/da4e1e312ce1558c9d8cf027c009f8b400f22b83/deployment_snapshots/weekend-20261107/ada/worker

Suggested next step: an idle-machine bounded comparison of the exact patch on
the current GPU/NFS pipeline, with the same selected windows and nonempty
controls. Adoption remains a separate decision. There is no automatic launch,
installation, remote push, production change or new search allocation here.
