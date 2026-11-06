# Target-aware primitivity investigation

## Recommendation

Keep the primitivity observation as a proven target-specific condition, but do not add a per-point gcd to the current overnight engine on this evidence. No production code, overnight process, Ada resources, checkpoint, or launch setting was changed. All experiments ran on one cloud host, using isolated files and pre-existing dependencies. CUDA was not executed. These are screening-kernel and small CPU-sphere timings, not end-to-end throughput claims.

## Proof and exact scope

Let g = gcd(|x|, |y|, |z|). For a nonzero target T, any solution has g > 0 and g^5 divides T. Since 42 has no nontrivial fifth-power divisor, g must equal 1. The same condition applies to both canonical residual targets +42 and -42.

The verified lattice transformation is (c,a,b) = (n0,n1,n2) U with integer unimodular U. Both U and U^-1 are integral, so each coordinate gcd divides the other. Therefore gcd(n0,n1,n2) = gcd(c,a,b). It is safe to test in coefficient space, provided the unimodular certificate remains required. This is a gcd-of-all-three condition, not pairwise coprimality.

For general target sets the safe condition is that g^5 divides at least one allowed target. Requiring g=1 universally is wrong. A known positive canonical control is (26,32,34), whose residual is 384 = 2^5 * 12; it must survive. For target 0, all g are permitted by divisibility, including the zero coefficient vector. Neither condition proves a candidate is a solution: exact residual equality is retained.

The native overnight kernel currently returns all residuals in a cap interval, not only +/-42. An unconditional primitive filter would narrow this general interface. A future implementation needs an explicit target-set contract, or a separate proof preserving the cap search's entire output. The existing generic nonprimitive controls are a useful regression guard.

## Existing code and modular overlap

- `lattice_gpu/src/kernel.hpp`: coefficient decode, unimodular reconstruction, canonical shape checks, exact 192-bit fifth powers, then residual-cap test. No native modular or gcd filter.
- `lattice_prototype/modular_filters.py` and its compiled experiment snapshot: optional target filters with moduli 25,31,61; exact interval and progression modes are already available.
- The older two-pointer search already uses modulo 11. This rules out all coordinates sharing 11.
- The 25/31/61 filters automatically reject common factors 5,31,61 for +/-42, but are not a complete primitive sieve. For example (82,310,924) has gcd=2 and passes the necessary +/-42 residue sets for all three moduli, yet cannot solve +/-42 because its residual is divisible by 32.

## Certified box samples and exact counts

All packets retain their existing certified transforms and coefficient bounds. Every box point was accounted for, including filtered points. All ten variants returned identical target hit records, and all reconstructed points had identical coordinate and coefficient gcds.

| Sample | Patches | Box points | Shape-valid | Nonprimitive after shape | Mod 25/31/61 survivors | Nonprimitive mod survivors |
|---|---:|---:|---:|---:|---:|---:|
| Complete positive B=1,000, width 8 | 118 | 4,483,388 | 261,114 | 42,565 | 36 | 6 |
| Selected high interval, width 8 | 256 | 560,484 | 70,445 | 11,783 | 13 | 0 |
| Same high interval, width 32 | 64 | 5,885,988 | 836,817 | 139,322 | 149 | 22 |

The high interval has c in [100000000001,200000000000] and a/c in [3/10, 3/10 + 2048/100000000001]. It is selected coverage only, not a full shell or an extension of the known full-box exclusion.

## Host screening timings

C++17, g++ 14.2.0, -O3, one pinned CPU, warm-up plus seven rotated-order samples per mode. Exact target equality adapts the existing 192-bit arithmetic to +/-42. Timing excludes packet preparation; suffix-cache setup is separately measured. Numbers below are medians from the cached-variant run, milliseconds:

| Sample | No gcd | Gcd before reconstruction | Gcd after shape | Cached suffix gcd after shape | Cache setup | Modular only |
|---|---:|---:|---:|---:|---:|---:|
| B=1,000 | 35.400 | 87.579 | 38.567 | 35.481 | 0.410 | 30.620 |
| High width 8 | 6.357 | 8.291 | 6.593 | 6.256 | 0.199 | 4.730 |
| High width 32 | 57.787 | 111.707 | 65.562 | 57.423 | 0.878 | 43.190 |

Plain early gcd is consistently worse. Caching gcd(n1,n2) and then only computing gcd(n0,g) when needed makes the shape-stage variant approximately break-even before setup, and slightly slower including its measured setup. A small-prime 2/3/5/7 wheel also failed to produce a reliable net gain. Gcd after the existing modular filter removes too few points to establish a gain: 0 of 13 in the width-8 high sample, 22 of 149 in width 32, and 6 of 36 at B=1,000. Small timing differences are host noise/code-layout scale; no GPU conclusion follows.

The modular-only candidate did better than per-point gcd in these host microbenchmarks, but it changes the same cap-versus-target contract and needs its own CUDA/end-to-end validation before adoption.

## Exact sphere experiment

A private copy of the optional sphere module cached gcd(n1,n2) at each innermost interval. It then checked gcd(n0,g) before the norm test, retaining original budgets, mapping, exact tests, and target semantics. Five alternating-order trials were run.

- At B=100, plain `prune` rejected 5,250 nonprimitive coefficients earlier, but every one was already rejected by the modular filters. Norm tests remained 1,666.
- At B=1,000, `prune` rejected 58,059 earlier, but only two were additional to modular rejection. Norm tests fell from 13,140 to 13,138.
- With the already available `interval` mode, the added primitive check rejected zero candidates at both B=100 and B=1,000, with identical norm-test counts. All innermost surviving suffixes already had gcd=1 in these samples.
- Wall-clock differences changed sign between repeated runs. The first run was approximately +1% for interval at B=1,000, while the persisted rerun was approximately -4.6%, despite zero additional gcd calls or rejections. This is not evidence of a pruning speedup.

The bounded redundancy finding is not a global theorem that all modular survivors are primitive.

## Correctness and nonempty controls

- Independent exact positive-domain oracle through B=100 recovered exactly (2,2,4,-960), (13,16,17,12), (26,32,34,384), and (42,71,72,2951). All target-aware native and sphere variants preserved this set, including nonprimitive cases.
- Independent integer pair-power hash oracle through B=1,000 found no +/-42 positive canonical hit and agreed with the bounded lattice result.
- 13,720 signed/zero coefficient tests under generated unimodular transforms of both determinant signs verified gcd invariance.
- Native gcd invariance was also checked for every box point in all four packets, including the controls packet.
- Undefined-behavior sanitizer execution passed the nonempty controls for all ten native variants.
- No new unbounded theorem, larger full-box exclusion, CUDA performance result, or overnight coverage is claimed.

## Reproduction and artifacts

From the scratch workspace:

    python fifth42-primitivity-20261106/prepare.py
    g++ -O3 -std=c++17 -Wall -Wextra fifth42-primitivity-20261106/bench.cpp -o fifth42-primitivity-20261106/bench
    python fifth42-primitivity-20261106/run_bench.py
    g++ -O3 -std=c++17 -Wall -Wextra fifth42-primitivity-20261106/bench_cached.cpp -o fifth42-primitivity-20261106/bench_cached
    python fifth42-primitivity-20261106/run_cached.py
    python fifth42-primitivity-20261106/sphere_test.py

`manifest.json` records packet and certificate hashes. The `*.results.json`, `sphere-results.json`, `correctness-extra.json`, and `controls100.ubsan.json` files contain measurements and exact test results. All production and overlay source includes are read-only dependencies of this isolated experiment; no changes were made to them.
