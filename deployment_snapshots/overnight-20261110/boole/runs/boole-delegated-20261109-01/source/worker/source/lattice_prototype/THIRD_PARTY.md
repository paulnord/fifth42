# Published library adaptation

This experiment replaces only reduction, not the mathematical patch covering or exhaustive enumerator. The adapters are new glue calling published APIs, not copied implementations of Elkies' or Healy's searches.

* fpylll 0.6.4, https://github.com/fplll/fpylll, installed from PyPI's CPython 3.12 manylinux wheel. GPL version 2 or later, verified from package metadata and included LICENSE. Calls `IntegerMatrix` and `LLL.reduction(method="proved", delta=0.75)` with an explicit identity transform.
* That wheel reports fplll 5.5.0 via `fpylll.config.version`. Its published license is LGPL 2.1, https://github.com/fplll/fplll/blob/5.5.0/COPYING. Native library code is not copied or redistributed here.
* cysignals 1.12.5 supplies fpylll's runtime dependency; LGPL v3 license, included from package distribution.
* SymPy 1.14.0, https://github.com/sympy/sympy/tree/1.14.0, already installed in this cloud environment. BSD 3-clause license, included from package distribution. Calls `DomainMatrix.lll_transform` over ZZ with exact QQ(3,4). Source: https://github.com/sympy/sympy/blob/1.14.0/sympy/polys/matrices/lll.py.

The fpylll/GPL licensing is materially different from SymPy's permissive licensing. No claim is made that an eventual combined distributed application is exempt from GPL obligations. Review the repository's licensing and distribution plan before shipping a bundled integration. This artifact contains only adapters, dependency pins and license notices, not the third-party binary wheels.

## Exact safety boundary

For rational row basis A, choose one common positive integer D clearing every denominator. Reduce D*A and obtain integer U and B_int. Independently verify |det U|=1 and U*A=B_int/D with Python arbitrary-precision integers/Fractions. These checks are explicit exceptions, not assertions, and stay active under `python -O`. Thus n -> nU is a bijection of Z^3 and enumerating all n with ||n B_int/D||^2 <= 3 enumerates exactly the same physical lattice points. Scaling each row independently would NOT preserve this lattice and is not done.

The exact original Gram-Schmidt sphere enumerator, outward patch bounds, inclusive boundaries, residual checks, signed42 reduction and work guards remain in place. No fplll floating-point enumeration, short-vector-only search, pruning coefficient or probabilistic sieve is used. LLL quality affects efficiency, not coverage once the unimodular certificate is verified. A library error or invalid certificate fails closed with complete:false via BudgetExceeded. The default remains the original reference reducer; selection is explicit with --backend sympy or --backend fpylll.

The time budget is checked before and after reduction, not a hard interrupt inside native LLL. The existing Python reducer likewise has no wall-clock interruption inside a call. Production watchdogs would require a process-level timeout. No production suitability is asserted.

The tested fpylll import also loads NumPy 2.3.5 (preinstalled here); it is pinned
in the optional requirements for reproducibility. NumPy is not used for
floating-point exclusion decisions in the search. Its source and license are
available at https://github.com/numpy/numpy/tree/v2.3.5.
