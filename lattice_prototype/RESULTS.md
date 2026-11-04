# Results and interpretation

Recorded 2026-11-04 in the x86_64 cloud execution environment, Python 3.12.14, g++ 14.2.0. These are small correctness runs, not resource estimates for ADA or for ranges beyond 10^11. Exact source and output files accompany this report.

## Complete bounded runs

| Work | Results | Patches | Lattice enumeration nodes | Elapsed |
|---|---:|---:|---:|---:|
| Positive domain c<=1,000, absolute residual<=5c^2 | 10 exact hits | 461 | 486,167 | 67.13 s |
| Signed target42 box +/-1,000 | 0 solutions | 463 | 198,033 | 33.00 s |

Every one of the 10 positive results matches the published Healy table and an independent exhaustive integer fifth-root oracle. That oracle took 1.93 s at c<=1,000. The constant-cap42 positive superset is also independently checked: its only canonical triples are (1,1,2), residual -30, and (13,16,17), residual +12. Neither yields signed target42.

These ten positive hits have residuals under our a^5+b^5-c^5 convention:

- (13, 16, 17): +12
- (26, 32, 34): +384
- (39, 48, 51): +2916
- (42, 71, 72): +2951
- (52, 64, 68): +12288
- (84, 142, 144): +94432
- (104, 133, 140): -75083
- (133, 228, 231): -87890
- (262, 328, 347): +96693
- (494, 954, 961): -2431553

## Existing exact-search comparison

Twenty actual compiled upstream runs pass: GMP CPU reference and four 192-bit row-search variants (baseline, cached, pruned, highword) in CPU emulation, across four comparison cases. The cases are target12 and target2951 at bound100, plus target42 at bound1,000 with modulo11 filtering and without filtering. Results are normalized by sorted integer triples and compared against both the prototype and a separate signed dictionary oracle. Nonempty controls prevent an empty-output comparison from being the only check.

All seven vendored source files match recorded original Git blob SHA-1 hashes. This does not run or validate GPU hardware; the emulation executes the same row routines on CPU. No current ADA run or prior 70-million-bound coverage was independently repeated here.

## Selected large-number controls

- (13,852,184, 27,401,825, 27,580,409), residual -359,711,619,643,000. One selected patch, 63 enumeration nodes, 0.83 s.
- (21,137,517,920, 21,483,066,250, 24,482,314,857), residual -75,381,811,685,198,766,057. One selected patch, 881 enumeration nodes, 1.66 s.

These are explicitly fixture-selected grid patches, using 160-bit dyadic root enclosures. Each known point is recovered by the lattice search rather than inserted into the hit set. They do not constitute blind discovery or complete coverage of those shells. The second example's fifth powers exceed 128-bit range, exercising the arbitrary-precision path.

## Verification

All 17 implementation and independently written audit tests pass. Boundary tests cover residual equality, shell endpoints, patch edges, u=9/10, repeated a=b, exact sphere corners, rational-root enclosures, zero-residual cases, and fail-closed guards. The direct fallback budget omission found during review was fixed and regression-tested. CLI guard exhaustion emits complete:false and exits 2. Python syntax compilation and shell syntax checks pass.

## What this does not establish

This prototype has **not demonstrated a speedup**. Its Python rational-arithmetic search is much slower than the existing compiled search at these small bounds; the filtered upstream GMP target42 comparison takes about 0.0056 seconds. This is not a fair language-independent algorithm benchmark: the prototype includes rational patch construction, LLL, complete sphere enumeration, and a wider residual band, while the upstream program solves just one target. The practical conclusion is that the coverage machinery works on tests, not that it is ready to replace the GPU code.

The next useful step is an optimized implementation of this same checked enumeration, preserving exact outward bounds and exhaustive enumeration, then moderate identical-workload benchmarks at increasing bounds. Adaptive patches and earlier domain pruning are plausible performance improvements but remain unimplemented. A large search or a claimed time-to-10^11 needs separate evidence and explicit approval.
