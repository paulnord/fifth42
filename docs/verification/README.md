# Lean verification for the target 42

With Lean 4.36.0, run `lean Fifth42Bridge.lean` from this directory.
The file uses Lean's standard library only. It retains the archived
finite certificate and adds an algebraic bridge to it.

The bridge checks the primary rotation modulo `(ζ - 1)^2`, exact
divisibility by the rotated cyclotomic factor, and the nonvanishing of
the pair modulo 2, 3, and 7. It then derives the three pair exponents
used in the finite contradiction. The checked endpoint is
`Fifth42.no_solution_of_quintic42`.

**This is conditional.** The endpoint takes a `Quintic42` interface as
an explicit argument. This interface states the required residue-symbol
properties for numerator or denominator 42, including the general
Eisenstein reciprocity swap for a primary element. The file does not
construct that interface for the actual cyclotomic ring. The absence of
`sorryAx` in the axiom audit does not discharge this theorem argument.

The [short paper](../fifth42-short.pdf) gives the mathematical proof.
The original standalone finite certificate remains in the ZIP under
`verification/Fifth42.lean`.
