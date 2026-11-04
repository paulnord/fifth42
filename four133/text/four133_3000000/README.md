# Incremental four-term 133rd-power search: 2.1 million to 3 million

This directory contains the new incremental stage. The preceding audited inclusive bound of 2,100,000 and its reproduction bundle remain unchanged in `../four133_extension/`.

**Do not infer completed coverage from this README.** The production run has to finish all configured chunks, reconcile its results, and pass independent audit. The driver deliberately reports `completed_awaiting_independent_audit` and leaves `coverage_claim` false. Test runs are explicitly marked and cannot supply production coverage.

## Search domain and branches

Target: four distinct signed integer bases, each of absolute value at most 3,000,000, whose 133rd powers sum to 42. The new stage handles only the shell where the largest absolute value is strictly greater than 2,100,000. Its union with the preserved earlier search supplies the desired full box if this stage completes and passes audit.

Every solution has ordinary base sum congruent to 42 modulo D = 4,206,930. The preceding sign/magnitude proof gives the interval [-2B, 2B+42]. At B = 3,000,000, only three sums occur:

- 42;
- 4,206,972 = 42 + D;
- -4,206,888 = 42 - D.

The sum-42 branch retains the previous two-positive/two-negative proof and gap bound. The other two sums have absolute value greater than B, so they cannot be realized by two positive and two negative bases. To see this, reflect a negative sum so that the ordinary sum S is positive and the power target T is either 42 or -42. For positive bases a ≤ b and negative magnitudes c ≤ d, if b ≥ d then the positive pair weakly majorizes the negative pair, and g(x) = x^133 - x gives F > S > 42. Thus b < d, so S = (a-c) - (d-b) < a ≤ B, a contradiction.

All-positive/all-negative cases and zero bases are already excluded. Zero is excluded by the unique residue multiset modulo 1597. A three-positive/one-negative configuration with T = ±42 must have positive ordinary sum: otherwise the negative magnitude is at least the sum of all three positive bases, whose 133rd power exceeds their three powers by more than 42. Therefore each additional sum has exactly the sign orientation assigned below.

## Canonical largest magnitude and incremental coverage

For branch `22`, write positives a ≤ b and negative magnitudes c ≤ d. The previous proof forces c < a ≤ b < d. Set h = d-b; then a = c+h+42 and 66 h² < 42B. The unique largest magnitude is d. Generate the full necessary left list (a,-c), but restrict the right list (b,-d) to d > previous_bound. This is exactly b ≥ previous_bound+1-h. All gaps through the new-bound limit are processed, including old gap values; merely adding new h values would be incomplete.

For branch `31pos`, normalize to a^133+b^133+c^133-d^133 = 42 and a+b+c-d = 4,206,972, with a ≤ b ≤ c.

For branch `31neg`, normalize to a^133+b^133+c^133-d^133 = -42 and a+b+c-d = 4,206,888. Output the reflected original bases (-a,-b,-c,d), whose required power sum is 42.

In either three-versus-one branch d > c: if c > d, their power difference alone exceeds 42; if c = d, the other two positive powers sum either to 2 or to more than 42. Put d = c+h with h ≥ 1. Then a+b = S+h. Since a ≤ b ≤ c, both b and c lie in

    ceil((S+h)/2) ≤ b,c ≤ B-h.

The left list contains (a,b); the right list contains (c,-d). Restrict the right list further to c ≥ previous_bound+1-h, and check b ≤ c after joining. Distinctness requires a < b < c; the raw search includes equalities too.

The gap bound is rigorous. For normalized target T = ±42,

    133 h c^132 ≤ (c+h)^133-c^133 = a^133+b^133-T ≤ 2c^133+42.

Here c ≥ 2, so integrality forces 133h ≤ 2c. Combining with c ≤ B-h gives 135h ≤ 2B. The interval endpoints also require 3h ≤ 2B-S. The implementation uses the smaller integer cap. At B = 3,000,000, each three-versus-one branch has h = 1,...,44,444.

## Modular filters and exact checking

For target +42, the unique power-residue multiset modulo 1597 is (1,1,325,1312). For normalized target -42 it is (1596,1596,1272,285), the negation of that multiset. The code reverses labels for the negative-target branch, retaining the same four pair-type/complement rules.

The sieve moduli are 2305843009213693921 and 2305843009213693951. Every equal-key bucket retains full Cartesian multiplicity. Canonical candidates are emitted, including repeated bases with a distinctness flag, and the driver checks every one with arbitrary-precision integer exponentiation. Zero raw matches would exclude repeats too, but the requested result remains the distinct-base problem.

## Running, pausing, and resuming

```
python run_incremental.py
```

The driver compiles the source, verifies the preceding result's hashes, and records the complete configuration and source/binary hashes. Each chunk comprises at most 1,024 gap values. A per-gap checkpoint is written only after the whole gap has been processed. A chunk is written to a `.partial` file, validated, and atomically promoted to `.log`. Only complete validated logs count. Rerunning the same command skips verified completed chunks and reruns an interrupted chunk from its beginning. Changed configuration, source, binary, or recorded completed-log hash is rejected rather than silently mixed.

For a bounded pause after N newly completed chunks:

```
python run_incremental.py --max-new-chunks N
```

Changing chunk size for an existing run is rejected. Use the original chunk size to resume.

The production target is fixed at 3,000,000; this is not authorization to run a later 4,000,000 stage.

## Small collision and resumption tests

```
python run_incremental.py --test --run-dir test_run --chunk-size 7 --max-new-chunks 2
python run_incremental.py --test --run-dir test_run --chunk-size 7
python run_incremental.py --test --run-dir test_run --chunk-size 7
```

Test mode uses bound 1000, previous bound 500, modulus 97, and synthetic normalized sum 1200 for the three-versus-one branches. It creates real modular collisions so matching and multiplicity can be compared with an independent direct enumeration. The final repeated command must perform no new searches. Tests do not establish production coverage.

No formal proof-checker installation or setup is involved. No ada, Valpo, or BNL resource is used.
