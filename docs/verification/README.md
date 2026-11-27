# Lean verification for the target 42

The [complete Lean proof](complete/) now proves nonexistence of integer
solutions for 42 without the conditional interface described below.
It includes build instructions and the axiom audit.

## Earlier conditional checkpoint

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

## Hilbert-symbol route (also conditional)

`Fifth42Local.lean` proves the polynomial identity for the Kummer norm
candidate, the leading fifth-power digit, the finite descent from level
9 to level 2, and the reduction from explicit Hilbert-symbol
evaluations to the finite contradiction. To reproduce the checks:

```sh
lean -o Fifth42Bridge.olean Fifth42Bridge.lean
env LEAN_PATH=. lean Fifth42Local.lean
```

Both files check on Lean 4.36.0 without `sorryAx`. This does not
discharge the theorem arguments: the local Hilbert character and
its evaluations are not yet instantiated in Lean.

The intended instantiation uses the local symbols for the fixed
radicand 42 in the completions of Q(ζ₅). With π = ζ₅−1, let
Uⱼ = 1 + πʲ𝒪 at the unique place above 5. For the arithmetic Artin
normalization, the following are the remaining connections:

1. The cutoff U₉ is made of fifth powers by Hensel, since the
   valuation of 5 is 4. At levels 6, 7 and 8, use the checked
   fifth-power digit and the fact that 5/π⁴ is a unit to match each
   successive coefficient. At level 5, use the norm of
   1 + sπα, where α⁵=42, whose checked conjugate product is
   1 + 42s⁵π⁵. Its leading digit ranges over the residue field F₅.
2. The automorphism ζ₅ ↦ ζ₅² acts as 2ʲ on Uⱼ/Uⱼ₊₁ and as 2 on
   the target fifth roots of unity. Norm-residue equivariance and
   the checked descent kill U₂. The same equivariance kills rational
   scalars, which are fixed by this automorphism. Therefore the
   character on u+ζ₅v equals h times its value on ζ₅, where
   h ≡ v/(u+v) (mod 5), when u+v is a unit there.
3. The primes 2, 3, 7 are inert and the valuation of 42 at each
   is one. At these places the tame exponent for (42,u+ζ₅v)
   is the negative of the computed residue exponent. Away from
   2, 3, 5, 7, either both entries are units or the reduction of
   42 is the nonzero fifth power w⁵ (by divisibility by u+ζ₅v),
   so the local symbol is trivial. The places at infinity are
   complex. Apply the product formula first to (42,ζ₅) to obtain
   the wild exponent 4, then to (42,u+ζ₅v) to obtain the required
   pair sum.

The pinned [NYLL source](https://github.com/n-yamaguchi-0729/NYLL/tree/30a178706c4828aa2c8e8d5c494c785be842af82/Nyll/ClassFieldTheory)
contains the general Hilbert product formula, tame formula, and
local norm criterion. These library results are not imported or
audited by the standalone checks above.
