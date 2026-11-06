# fifth42: host optimizations, exact sieves and independent audit

Consolidated reproduction bundle, 2026-11-06. All original experiment files,
reports, packets, results, patches and delivery archives are preserved unchanged.
Nothing here was deployed to Ada, and this packaging did not alter a live search,
checkpoint, lease, launch setting or production repository.

## Findings and decisions

- **Prioritize an isolated low-word CUDA experiment next.** Unsigned low-word
  fifth-power arithmetic is a necessary residual test, followed by the existing
  exact 192-bit check. It preserves the whole fixed residual interval, not only
  the two targets. In the selected high32 CPU packet, cap-42 screening took
  57.335 ms without the precheck and 39.808 ms with low64, a 1.44x ratio.
  Low32 was similar. This is CPU screening time, not CUDA or end-to-end speedup.
- **Independent low-word audit passed.** All eight packet/mode combinations
  reproduced exact counts and complete hit records. UBSan checks covered
  100,008 bigint-oracle triples and 18,228 predicate/boundary checks, including
  negative residuals, nonprimitive controls, large bases and deliberate aliases.
- **Do not add a per-point primitive gcd on this evidence.** For +/-42,
  gcd(a,b,c)=1 is necessary and equals the coefficient gcd under the certified
  unimodular transformation. Generic targets instead require g^5 to divide an
  allowed target. Early gcd was slower; cached suffix gcd was approximately
  break-even before setup and redundant with most modular pruning.
- **Keep the host arithmetic candidate.** Exact GMP roots plus the structured
  inverse reduced a common local host pipeline median from 2.401616 s to
  1.742182 s (1.38x), with matching certificates and 107 passing host tests.
  This ratio is from a separate experiment and must not be multiplied by 1.44x.
- **Width 32 won the selected CPU calibration, not a GPU competition.** Width 64
  reduced preparation but increased native CPU work; width 128 was much costlier.
  The objective for future work is distinct certified geometric coverage per
  fixed total wall-time budget, rather than repeated regions or patch rates.
- **Other directions remain experimental.** Consistent target-sign masks and
  mod 11 strengthen target-only modular pruning. Prime-power filters and
  pair-sum divisibility were studied; no factorization-based replacement is
  recommended. Compact transport had no reliable measured gain. The multiple-
  coordinator prototype and fixed-time exploration executor are not validated.

## Non-negotiable scope and integration cautions

1. Keep the exact full-width residual check after every low-word precheck:
   large residuals can alias modulo 2^64. Apply the actual fixed cap, not a
   hard-coded 42. The c-dependent mode with cap 5*c^2 is not covered by simply
   inserting the fixed-cap test. The current two-tail experiment also admits
   everything at cap zero; that is safe but ineffective. For unsigned values
   and 0 <= C <= INT64_MAX, `(u + C) <= 2*C` handles zero correctly.
2. The high8/high32 packets cover a selected narrow ratio strip near 0.3 and
   100000000001 <= c <= 200000000000, not a complete shell. Small/control packets
   omit the direct low-c bands recorded in their manifest. Patch hit records
   can duplicate one triple. The independent audit supplies omitted controls.
3. The primitivity report's small1000 table describes its packet under the
   full-domain preparation plan. It is not, by itself, the complete B=1000
   domain: its direct c=1..3 work is separate. The independent B=1000 oracle
   supplies the bounded no-+/-42 conclusion. See the audit for this distinction.
4. No larger full-box exclusion, unbounded theorem, new overnight coverage,
   GPU speedup, or completed fixed-time exploration run is claimed. The prepared
   exploration plan's prior-coverage ledger is explicitly non-exhaustive.
5. Future Ada execution must wait for both the search and final publisher,
   acquire existing leases and independently validate frozen CUDA sources,
   binaries, nonempty controls and committed coverage. This archive launches
   nothing automatically and grants no permission to change that environment.

## Start here

- `REPRODUCE.md`: dependencies, exact patch order, isolated rebuild and checks.
- `fifth42-primitivity-20261106/REPORT.md`: proof, gcd experiments and sphere work.
- `fifth42-other-sieves-20261106/REPORT.md`: low-word, modular and divisor findings.
- `lowword-audit-20261106/REPORT.md`: independent audit and scope corrections.
- `fifth42-coordinator-20261105/ada_validation/host-ideas-20261106/README.md`:
  host experiments, wider patches and the distinct-coverage plan.
- `package-validation/`: fresh packaging correctness checks, separate from the
  original performance evidence. No new performance inference is made from them.
- `SHA256SUMS`: SHA-256 of every bundled regular file except this checksum list.

The earlier coordinator deliverables are included as dependencies. The untouched
base source archive and both ordered patches allow reconstruction of the supplied
source snapshot. The low-word and gcd experiments are standalone harnesses, not
production patches. Prebuilt original binaries are preserved as evidence only;
rebuild them for your own machine.
