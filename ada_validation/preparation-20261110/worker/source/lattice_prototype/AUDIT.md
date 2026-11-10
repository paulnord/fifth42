# Independent mathematical coverage audit

Reviewed `lattice5.py` independently, including the exact row-basis LLL,
Gram–Schmidt enumeration, rational patch enclosure and target-42 signed reduction.
No mathematical completeness defect was found in the reviewed implementation.
This is a small-prototype audit, not a formal proof certificate or evidence of
production-scale performance.

## Checks

- For f(u)=(1-u^5)^(1/5), f''(u)=-4u^3/f(u)^9. On a patch [l,h], the
  implemented Taylor remainder 2 h^3 delta^2 / vlo^9 is conservative because
  vlo is an outward lower bound for f(h), and delta is the patch half-width.
- The midpoint q error and slope-midpoint error are bounded independently.
  The perturbation from residual r is at most eta/(5 vmin^4), where
  eta=R/C^5 and vmin bounds the smallest possible perturbed fifth root.
- Since a<=b, (a/c)^5 <= (1+R/C^5)/2. The fixed u<=9/10 coverage is
  justified only when R/C^5<=9049/50000. The implementation tests this exact
  threshold and uses direct search for small shells that fail it.
- Multiplying (c,a,b) by the patch row basis puts all covered candidates in
  [-1,1]^3. Thus the radius-squared-3 sphere is an inclusive enclosure.
- Exact LLL preserves the lattice via B=U*A and an integer unimodular U.
  Enumeration runs backward through Gram–Schmidt coordinates, subtracts
  exact squared lengths, and uses outward integer square-root bounds.
  Conversion from the reduced integer coefficients is n*U. Boundary points
  are retained by inclusive comparisons throughout.
- The direct small-shell oracle includes the floor of the lower root, which
  can add one irrelevant integer but cannot omit any admissible integer.
  All extras are removed by exact residual filtering.
- For target 42, all-nonnegative solutions, zero-coordinate solutions and
  the two-positive case with c<b either lie in [-2,2]^3 or are excluded by
  3^5-2^5=211>42. When c=b, the remaining a^5 cannot equal 42.
  The finite box has no solution. The remaining two sign
  patterns correspond to residual +42 and -42, respectively. Sorting the
  signed triples removes permutations only, not distinct solutions.

## Independent regression tests

Run `python audit_tests.py` in this directory. The tests include:

1. Outward rational fifth-root bounds, exact dyadic roots and tiny radicands.
2. Sixteen deterministic rational lattices: compare exact sphere enumeration
   with an independently bounded coefficient-box enumeration; verify inverse
   matrices, unimodularity and exact basis reconstruction.
3. All eight normalized cube corners on the enclosing sphere.
4. The sharp u=9/10 fixture (9,9,10), residual 18098.
5. Exhaustive patch-containment checks on small shells.
6. Full near-miss sets against direct cubic-loop brute force for multiple
   residual caps and patch widths, including nonempty outputs.
7. Healy-envelope set equality through c=60 and signed-box equality through
   coordinate bound 100.
8. Enumeration/patch budget exhaustion raises rather than returns coverage.
9. Direct fallback pair and candidate guards stop within a single large shell,
   and the top-level search propagates failure without claiming coverage.

## Limitations and operational note

Budget checks now occur at patch/shell boundaries, every 256 sphere-enumeration
nodes, and every 256 direct fallback pairs or candidates. The direct fallback
omission found in the initial audit has been fixed and regression-tested.
One root computation or one LLL call is still not interruptible by the
wall-time budget. Thus the limit is a cooperative guard rather than a hard
execution deadline; bounded inputs remain appropriate for this prototype.

The separate `COVERAGE.md` argument was also reviewed: its shell threshold,
Taylor bound, row-basis convention, sphere recursion, and signed exceptions
agree with the implementation. The distinction between selected large-fixture
patches and complete shell coverage is stated correctly.
