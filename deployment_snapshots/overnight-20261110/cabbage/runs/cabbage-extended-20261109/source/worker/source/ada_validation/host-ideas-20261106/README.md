# Further host ideas and distinct-coverage planning

Status: local CPU candidates tested; the next exploration plan is prepared only.
No ADA access, production edits, remote publication or new search launch occurred.
This add-on requires the earlier coordinator candidate. Existing source and the
previous deliverable remain unchanged.

## Objective update

After the small controlled comparisons below, Paul changed the main objective:
maximize **distinct certified geometric coverage per fixed time budget**. Do not
spend the main exploratory budget repeating identical regions. Keep only small
identical-work correctness/calibration controls. Different methods may explore
different strips, and patch counts across widths are not scientific coverage.

Accordingly, no repeated multi-coordinator timing trial was started. The next
plan and exact coverage-accounting code are described below. No experiment is
scheduled or running from this work.

## Exact host arithmetic

The opt-in private GMP root implementation replaces Python binary-search integer
roots with an exact GMP integer root. It never modifies the shared frozen lattice
module, and preserves outward dyadic root brackets exactly.

The structured inverse uses `B = U A`, hence `B^-1 = A^-1 U^-1`, where `U` is
integer unimodular and `A` is the explicit triangular tangent-patch basis. This
avoids large rational cofactors of `B`. It retains the exact `B * B^-1 = I` check,
independent reconstruction of the certification patch, all original transform,
point and range guards, and identical coefficient enclosures/certificates.

Five rotated fresh-work CPU trials use the same 1,024 high-range patches,
4 allowed CPUs, one native CPU thread, and the prior one-pass packer. The measured
steady section includes preparation, native execution, exact verification and
durable commits; startup/shutdown are separate.

| Arithmetic | Median seconds | Repeat range |
|---|---:|---:|
| Original arithmetic in common harness | 2.401616 | 2.178562–2.490314 |
| GMP integer roots | 2.031335 | 1.986188–2.103046 |
| Structured inverse | 2.166134 | 2.051928–2.284839 |
| Both | 1.742182 | 1.632969–1.892051 |

The combined result is 1.38× the reference throughput in this local experiment.
Summed worker CPU fell from roughly 5.84 to 3.43 seconds. Do not multiply this
ratio by earlier experiments or present it as ADA/GPU/production speedup. Five
rotations are not perfectly order-balanced for four modes.

All patch, transform, coefficient, certificate, geometry and packet identities
match the reference. New tests cover roots through 2,048-bit random/boundary
inputs, signed unimodular transforms, sampled high-shell guards, and nonempty
independent controls under ordinary CPU and ASan/UBSan execution.

## Wider certified patches

This completed calibration used the identical exact ratio union
`[3/10, 300000020483/1000000000010]`, denominator band
`100000000001 <= c <= 200000000000`, 222-bit precision, and five rotating repeats
using the combined arithmetic above. These are nested exact-width partitions,
not separately rounded full-shell grids.

| Width | Patches | Coefficient points | CPU median seconds | Range |
|---|---:|---:|---:|---|
| 8 | 256 | 560,484 | 0.306659 | 0.289288–0.319995 |
| 16 | 128 | 1,712,892 | 0.176774 | 0.168698–0.220458 |
| 32 | 64 | 5,885,988 | 0.144838 | 0.133880–0.146803 |
| 64 | 32 | 21,744,972 | 0.261137 | 0.246669–0.266333 |
| 128 | 16 | 83,151,068 | 0.840467 | 0.818921–0.936872 |

These include fresh preparation/certification/packing, CPU native enumeration
and exact decode. **Durable checkpoint costs are excluded**; startup/shutdown
are reported separately. No new full-box result follows.

Width 64 was 1.80× slower than width 32 on CPU, but its host preparation was
roughly half: 0.0414 versus 0.0816 seconds. Native CPU work grew from 0.0598 to
0.2173 seconds. Thus width 64 remains a plausible GPU exploration candidate;
these measurements do not select a GPU winner. Width 128 substantially increases
native work. No guard was relaxed. Wider full small-domain grids can hit the
existing point guards (widths 64/128 at bound 100), which remain explicit failures.

## Compact representation: not recommended yet

The lossless denominator-deduplicating binary transport reduces the selected
256-task result payload from 2,116,754 to 1,860,428 bytes (12.1%). Seven exclusive
fresh preparation/IPC/assembly pairs had medians 0.505697 and 0.489776 seconds,
with large overlapping ranges. No reliable throughput gain was established.
The representation preserves the original immutable Task and all canonical
identities. Keep it experimental. See `docs/compact_certificate_experiment.md`.

## Coordinators: code only, unbenchmarked

The isolated 1×4 versus 2×2 CPU prototype has a single engine owner, bounded
requests, exact identities, independent journals, and nested-worker affinity
handling. Five protocol/partition tests pass. Native integration and performance
are **not validated**. Repeated comparison trials were stopped before launch
when the exploration objective changed. It is not a production backend.

## Prepared next exploration

`lattice_gpu/exploration_plan.py` writes a plan and launches nothing. Proposed
budget: 60 seconds each for widths 32, 64 and 128, total at most 180 seconds,
with at most four local workers and one engine owner. Proposed preparation
chunks contain eight patches, at most 80 million coefficient points under the
unchanged per-patch guard, and split into native packets of at most 50 million. It assigns disjoint strips
starting at ratios 9/20, 11/20 and 1/5; each strip has exact ratio span
`1048576 / 100000000001` in the same high denominator band. A one-patch preparation check rejected the originally considered width-128 strip
at 13/20 under the unchanged 10-million-point guard, so that proposed strip was
replaced rather than relaxing the limit. Exact tiling uses
width/cmin and subtracts supplied prior committed coverage first.

`region_coverage.py` computes rational rectangle unions, new coverage excluding
prior work, planned gaps, guard/incomplete regions, duplicate excess and overlaps
across overlapping denominator slabs. Measures are exact row-ratio area and an
optional c-weighted geometric area; neither is a lattice-point or solution count.
Open/closed boundary detail is reported separately, because zero-measure rational
boundaries can still contain integer candidates. Conservative closed scheduling
may recheck such boundaries; that is disclosed rather than silently called new.

Partial published overnight evidence is **not** a complete prior ledger. The
prepared plan explicitly has `prior_coverage_is_exhaustive=false` until verified
coverage evidence is supplied. Novelty is relative to that supplied ledger only,
not a claim that the whole region is globally unsearched.

Before ADA execution: wait for both search and final publisher to finish, acquire
the existing leases, freeze/verify sources and binaries, validate native CUDA and
small nonempty controls, and import a verified committed coverage prefix. Budget
all preparation, queueing, transfers, kernels, exact decode and durable commits.
Only complete committed regions count. Interrupted or guarded work stays visible
as gaps. Report total actual wall time and region union, not sums of patch rates.
Different strips have different costs, so exploration productivity is not a
controlled algorithm speedup. The planner/accounting library is prepared; no
integrated fixed-time exploration executor has been validated or launched.
