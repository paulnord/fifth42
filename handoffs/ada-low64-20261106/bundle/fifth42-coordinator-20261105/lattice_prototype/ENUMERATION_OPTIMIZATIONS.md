# Additional exact enumeration experiments

The optional `modular_filters.py` modes `progression` and `interval` extend the
original `prune` experiment. Defaults remain unchanged.

## Progressions

With suffix coefficients fixed, each modulus supplies the exact admissible
first-coefficient residue set. Choose the sparsest residue set and iterate its
arithmetic progressions within the original inclusive coefficient interval,
intersecting the other modular conditions. This is equivalent to testing every
integer in that interval, but avoids visiting modularly impossible choices.
No CRT union is materialized. The original outward interval length is still
charged to `enumeration_nodes`, even for skipped integers; budget checking occurs
before emitting its candidates. Thus skipping does not evade work guards.

## Exact final-coordinate interval

At recursion level zero let center=A/B, squared Gram-Schmidt norm=C/D and remaining
squared radius=E/F, all in lowest terms, B,C,D,F positive and E nonnegative.
The original inequality is

    (n+A/B)^2 * C/D <= E/F.

It is exactly equivalent to

    (n*B+A)^2 <= floor(E*B^2*D/(F*C)).

Taking integer `isqrt` gives R and the inclusive interval

    ceil((-R-A)/B) <= n <= floor((R-A)/B).

Intersect this with the original outward interval, then intersect the modular
progressions. Every surviving integer passes the norm inequality, so there is
no need to construct a Fraction and compute its gcd for each leaf. Exact
original coordinate reconstruction and fifth-power residual acceptance remain.
This rule includes rational/integer boundary equality and negative n.

`interval_rejects` counts outward-bound candidates rejected by this exact norm
interval, while `modular_rejects` counts modular failures in the tightened interval.
Their sum explains the excluded leaf choices. `norm_tests` counts the remaining
rational norm tests at upper recursion levels; `integer_intervals` counts exact
leaf interval calculations. The conservative `enumeration_nodes` count remains
identical across modes, verified on seeded random rational bases and complete
bounded searches. Counts are not falsely presented as fewer visited reference
nodes.

## Profiling and bounded evaluation

`results/profile-pruned-1000.txt` is a cProfile report for the earlier prune mode:
Fraction arithmetic and gcd dominate after fpylll reduction and modular pruning.
Profiler times are not directly comparable with uninstrumented wall times.

Run `benchmark_enumeration.py` for three-trial bound100 and bound1000 comparisons,
including interval mode without modular filters, independent signed dictionary
oracles, and nonempty residual12/384/2951 controls. Its JSON preserves every
sample and exact result set.

Run `benchmark_widths.py` for widths1/2/4/8 at complete bound1000, plus a nonempty
2951 control for every width. These are the existing rigorously enclosed uniform
patches, not a new adaptive covering. A larger width changes efficiency, not
coverage, under the unchanged COVERAGE.md argument. Do not infer an optimal
large-scale width from one small bound.

Compiled rational arithmetic, parallel patch processing and adaptive widths are
not implemented here. Their potential does not justify changing the exact safety
boundary without separate tests. No production run or ADA access occurred.
