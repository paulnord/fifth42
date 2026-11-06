# Additional exact filters for fifth42, 2026-11-06

## Result

The strongest measured new candidate is a low-word residual precheck, not another prime table. On the private high32 packet at c = 100,000,000,001 through 200,000,000,000, unsigned modulo-2^64 arithmetic reduced all-near-miss evaluation from 57.335 ms to 39.808 ms (1.44x) and target-only evaluation from 58.153 ms to 40.690 ms (1.43x). It preserves every |a^5+b^5-c^5| <= 42 result, not just +/-42. These are single-core CPU box-traversal measurements; they do not establish CUDA speedup or end-to-end job speedup. No live process or production source was changed.

The inspected checkout is `fifth42-coordinator-20261105` at 8e34d94dab4b3741392d73bed40ea51c365cc3bd; the private benchmark includes its 2e11 overlay's kernel/io headers. Both inspected kernel copies perform domain rejection and then full 192-bit fifth powers. Neither contains this precheck. Current remote or live source may differ.

## Low-word filter and completeness

For a positive reconstructed base x, compute x2=x*x; x5=x2*x2*x using unsigned 64-bit operations. Overflow is defined modulo 2^64. Then r = a5+b5-c5 is exactly the true integer residual modulo 2^64. This costs nine ordinary low-word multiplications for three bases.

For target +/-42 retain only r == 42 or r == uint64(-42). For a fixed cap C < 2^63 retain r <= C or r >= uint64(-C). An equivalent compact test is unsigned(r+C) <= 2*C, with the stated bound on C. Keep the existing full-width residual check for every survivor: the precheck is necessary, not sufficient, and values separated by 2^64 can alias. For a larger c-dependent Healy cap, do not silently reuse this fixed-cap test; once the permitted residual interval covers all low-word residues, this modulus cannot reject anything.

Modulo 2^32 and 2^16 variants are also exact with the analogous mask. The 2^64 version costs no table or integer division. A CUDA implementation needs its own benchmarking, where low 32-bit operations could cost less. All domain, overflow, root-precision and coverage checks remain necessary.

Uniform residue triple densities are not live candidate probabilities. For +/-42 modulo 2^k, k>=3, the exact density is 3/(2*2^k). This follows from exactly two odd bases and one even base, and bijectivity of the fifth-power map on odd residues. It is about 8.13e-20 at k=64. For the full residual interval [-42,42], highly divisible triples can produce zero modulo 2^k; density is higher than 85/2^k. Exact interval densities are 0.0024604797 at 2^16, 1.44942896e-6 at 2^32 and 2.72848851e-12 at 2^64. The recurrence used to obtain these was independently exhaustively checked for every residue through modulus128.

## Private bounded measurements

Packet inputs were reused read-only from the previous private primitivity experiment. Input/certificate hashes and construction context remain in `../fifth42-primitivity-20261106/manifest.json` and its preparation files. high8 has 256 patches, high32 has 64 patches in the stated large-c range. Small/control packets retain their original patch geometry. Timing excludes packet generation and I/O. Eleven rotated-order repetitions follow a warm-up; one allowed CPU was pinned. Every variant's complete (task,index,a,b,c) hit set is checked against the unfiltered baseline.

| Packet/mode | Box points | Pass domain | Baseline ms | Low64 ms | Exact tests after low64 | Hit records |
|---|---:|---:|---:|---:|---:|---:|
| small1000, targets +/-42 | 4,483,388 | 261,114 | 35.348 | 29.927 | 0 | 0 |
| high8, targets +/-42 | 560,484 | 70,445 | 5.802 | 4.366 | 0 | 0 |
| high32, targets +/-42 | 5,885,988 | 836,817 | 58.153 | 40.690 | 0 | 0 |
| controls100, four targets | 589,483 | 20,080 | 4.197 | 3.753 | 6 | 6 |
| small1000, interval +/-42 | 4,483,388 | 261,114 | 34.751 | 29.390 | 2 | 2 |
| high8, interval +/-42 | 560,484 | 70,445 | 5.893 | 4.217 | 0 | 0 |
| high32, interval +/-42 | 5,885,988 | 836,817 | 57.335 | 39.808 | 0 | 0 |
| controls100, interval +/-2951 | 589,483 | 20,080 | 4.154 | 3.747 | 10 | 10 |

Control targets are 12,384,2951,-960; their nonempty hits and all nonempty interval hits were independently verified with Python big integers. The target controls include scaled, nonprimitive hits. A further 10,000 random signed triples with magnitude up to 2e11 checked low-word arithmetic against exact Python integer residuals and checked the factorization identities. Additional compiled checks preserve the exact residual-cap boundary at 12 and reject at 11 for (13,16,17). They deliberately exercise positive and negative aliases: scaling that triple by 8192 makes the residual a multiple of 2^64, so the low-word filter passes it but the full-width test correctly rejects it. These tests do not by themselves certify a future production implementation.

For high32 target-only comparison:

| Exact precheck | Survivors/exact tests | Median ms |
|---|---:|---:|
| none | 836,817 | 58.153 |
| low16 | 15 | 40.600 |
| low32 | 0 | 41.036 |
| low64 | 0 | 40.690 |
| 25/31/61, independently either sign | 149 | 44.133 |
| 25/31/61, same target across moduli | 27 | 43.553 |
| 11/25/31/61, same target across moduli | 0 | 43.471 |
| divisibility by a+b | 0 | 52.121 |

The small differences between low-word widths are not meaningful evidence for their ranking. The repeat ranges overlap. The much larger reduction in exact-test counts does not translate to comparable total speedup because decoding, coordinate reconstruction and domain rejection still run for every box point. Pipeline preparation can dominate total run time further.

## Primes and prime powers

All tests are necessary congruences for the explicit target. They become legitimate pruning only when the target set is fixed. For the live interval [-42,42], each modulus <=85 sees every possible residual residue, so an independent target-membership check at 11,25,31 or 61 rejects nothing.

For prime p with p not congruent to 1 modulo 5, fifth powers permute F_p. Thus there are exactly p^2 triples for one residual, with density 1/p; such primes are not intrinsically useless, but their filters have no special fifth-power compression. Primes1 modulo 5 have only 1+(p-1)/5 fifth-power values. Target-specific finite counts matter more than that condition alone: modulo 41 the +42 density is4.556%, worse than modulo 31 at3.021%. No tested modulus was a local impossibility for42.

Selected exact +42 densities (the two signs double them when distinct):

| Modulus | +42 admissible triples | +42 density |
|---|---:|---:|
| 11 | 75 / 1331 | 5.634861% |
| 25 | 750 / 15625 | 4.8% |
| 31 | 900 / 29791 | 3.021047% |
| 61 | 3725 / 226981 | 1.641107% |
| 121 | 9075 / 1771561 | 0.512260% |
| 125 | 18750 / 1953125 | 0.96% |
| 625 | 468750 / 244140625 | 0.192% |
| 961 | 864900 / 887503681 | 0.097453% |
| 3721 | 13860725 / 51520374361 | 0.026903% |

For p!=5 and nonsingular solutions, each lift from p^k to p^(k+1) adds p^2 lifts out of p^3 possible lifts, so survival density falls by 1/p. For42 at p = 2,3,7, singular all-zero classes need separate treatment because p divides42. For example, modulo 9 there are 72 +42 triples, not 81. Prime-power tables therefore offer stronger rejection but larger tables/cache/last-coordinate scans. They are not new geometric constraints, and a low-word postcheck is cheaper in the measured native kernel. If integrated into enumeration, extra setup and skipped coefficient work must be measured separately.

Modulo 11 gives a useful exact structural statement: exactly one of a,b,c is divisible by 11 for either target. The two nonzero fifth-power residues must have the required signs. It is safe to use this before exact arithmetic, but it cannot replace checking all three possible positions of the divisible coordinate in the positive canonical domain.

### Keep one target consistent across moduli

The existing optional Python filter permits +42 at one modulus and -42 at another. This is safe but loose. Carry a two-bit surviving-target mask and intersect it across moduli. By CRT, for 25/31/61 the relaxed uniform triple density is 0.01903818%; consistent either-sign density is 0.004759545%, exactly four times smaller. With 11 added, consistent either-sign density is 0.0002681937%. This improved actual high32 post-domain survivors 149→27, but timing changed little. It may matter more if applied before expensive sphere norm tests.

No single-coordinate exclusion exists for either target individually at moduli 11,25,31,61: each c residue completes to at least one sign. However, maintaining the same target sign across these moduli does give a combined c-only restriction. Its exact CRT density is7621/20801 = 36.6377%. This can help a c-row-based algorithm; it does not remove a comparable fraction of broad lattice patches automatically.

Do not materialize every admissible CRT triple coset: the existing25/31/61 +42 union already contains 2,514,375,000 coefficient classes. Use cached reached suffixes, residue masks or exact progression enumeration instead.

## x+y divides 42-z^5

For signed x,y,z, define N=T-z^5, s=x+y and p=xy. Any solution has s|N and

N/s = s^4 - 5*s^2*p + 5*p^2.

For T=42, s cannot be zero, because 42 is not an integer fifth power. A complete divisor method can enumerate each signed z in its prescribed range and each signed divisor s of N, then test:

1. n=N/s is positive.
2. Q=(s^4+4*n)/5 is a nonnegative integer square, say q^2.
3. 2*q-s^2 is a nonnegative integer square, say d^2.
4. s and d have equal parity; x=(s+d)/2, y=(s-d)/2 lie in the required range.
5. Verify the original equation exactly.

This reconstructs every signed pair up to swapping x,y, since q=x^2+y^2 and d=|x-y|. Equivalently, the quadratic-in-p discriminant 5*s^4+20*n must be a square. This is a valid complete algorithm when all required z values/divisors are covered, not an efficient shortcut by itself.

For positive-canonical residual T, the simplest candidate precheck is (a+b)|(c^5+T). It needs only modular exponentiation of c modulo a+b, without factoring N. The private benchmark uses three unsigned 128-bit modular multiplications. It rejected every high32 target candidate, but at 52.1 ms was slower than low64 at 40.7 ms and the small-prime filters at 43.5–44.1 ms. Small/control cases retain many false divisors. Using other signed pair sums a-c or b-c provides equivalent valid prechecks, but needs additional divisions and has no demonstrated benefit after low64 rejection.

Full divisor generation would require factoring roughly 183–188-bit N for each large z, across a range with 10^11 entries. There is no measured case that this beats the existing geometric search, and naive scanning of pair sums reintroduces a very large two-dimensional search.

A useful factor consequence is: if q is a prime congruent to 1 modulo 5 and 42 is not a fifth-power residue modulo q, q cannot divide any signed pair sum. Initial such primes are 11,31,61,71,101,131,151,181,191,211,241,251. This restriction is already implied by the full residual congruence modulo q; it cannot add rejection after that congruence has been checked. It could only be a cheaper partial precheck before it.

## Recommendation

1. Preserve the current run unchanged.
2. For a next native-kernel experiment, prioritize the low-word filter, compare both 32 and64 bits on CUDA, and retain the exact full-width check. Test nonempty controls, near-overflow arithmetic and all target/interval modes.
3. For target-specific sphere enumeration, first use consistent target masks and include the cheap mod 11 restriction; then benchmark prime powers versus table/cache construction. Do not infer native-kernel gains from Python rational-enumeration gains.
4. Keep full divisor factoring as an alternative research direction rather than a proposed large-run replacement. The bounded variable-modulus test was slower than low-word filtering.

## Files

`bench.cpp`, `run.py`, `bench.log` and per-case JSON contain the isolated C++ test and 11-repeat results. `densities.py` and `densities.json` contain exact finite congruence counts through the selected primes/powers. `checks.py` and `checks.json` contain independent bigint/control and 2-adic-count checks. `machine.json` identifies the local timing environment.
