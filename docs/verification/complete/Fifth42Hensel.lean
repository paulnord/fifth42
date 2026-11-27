import Nyll.ValuedFieldTheory.Valuation.Henselian.NonmonicSimpleRoot
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.LinearCombination
import Fifth42NormDigits

namespace Fifth42
open Polynomial

private noncomputable def digitPolynomial₃ {R : Type} [CommRing R] (c pi : R) : Polynomial R :=
  digit₃ (C c) (C pi) X

private theorem eval_digitPolynomial₃ {R : Type} [CommRing R] (c pi t : R) :
    (digitPolynomial₃ c pi).eval t = digit₃ c pi t := by
  simp [digitPolynomial₃, digit₃]

private theorem map_digitPolynomial₃ {R : Type} [CommRing R]
    (red : R →+* ZMod 5) (c pi : R) (hc : red c = -1) (hpi : red pi = 0) :
    (digitPolynomial₃ c pi).map red = C 3 * X := by
  simp [digitPolynomial₃, digit₃, hc, hpi]
  rw [← map_ofNat (C : ZMod 5 →+* Polynomial (ZMod 5)) 8, show (8:ZMod 5)=3 by decide]

/-- The level-three digit is onto the valuation ring, not just its residue
field: the normalized norm polynomial reduces to 3X and has unit derivative. -/
theorem level₃_hensel_surjective {K : Type} [Field K] (V : ValuationSubring K)
    [HenselianRing V (IsLocalRing.maximalIdeal V)]
    (res : IsLocalRing.ResidueField V ≃+* ZMod 5)
    (c pi : V) (hc : res (IsLocalRing.residue V c) = -1)
    (hpi : res (IsLocalRing.residue V pi) = 0) :
    Function.Surjective (digit₃ c pi) := by
  intro y
  let red := res.toRingHom.comp (IsLocalRing.residue V)
  let P := digitPolynomial₃ c pi - C y
  have hp : P.map red = C 3 * X - C (red y) := by
    rw [Polynomial.map_sub, Polynomial.map_C, map_digitPolynomial₃ red c pi hc hpi]
  have hs : Function.Surjective red :=
    res.surjective.comp (Ideal.Quotient.mk_surjective)
  obtain ⟨t, ht⟩ := hs (2 * red y)
  have h0 : red (P.eval t) = 0 := by
    rw [← eval₂_at_apply, ← eval_map, hp, eval_sub, eval_mul, eval_C, eval_X, eval_C, ht]
    calc
      3 * (2 * red y) - red y = ((3:ZMod 5)*2) * red y - red y := by rw [mul_assoc]
      _ = 0 := by rw [show (3:ZMod 5)*2=1 by decide, one_mul, sub_self]
  have hder : red (P.derivative.eval t) = 3 := by
    rw [← eval₂_at_apply, ← eval_map, ← derivative_map, hp]
    simp
  have h0' : P.eval t ∈ IsLocalRing.maximalIdeal V := by
    apply Ideal.Quotient.eq_zero_iff_mem.mp
    apply res.injective
    exact h0.trans res.map_zero.symm
  have hd' : IsUnit (Ideal.Quotient.mk (IsLocalRing.maximalIdeal V) (P.derivative.eval t)) := by
    change IsUnit (IsLocalRing.residue V (P.derivative.eval t))
    apply isUnit_iff_ne_zero.mpr
    intro e
    have e' := congrArg res e
    exact (show (3:ZMod 5) ≠ 0 by decide) (hder.symm.trans (e'.trans res.map_zero))
  obtain ⟨a, ha, _⟩ :=
    DiscreteValuationField.exists_root_of_henselianRing_of_simpleRoot_mod V P t h0' hd'
  use a
  simpa [P, Polynomial.IsRoot, eval_digitPolynomial₃, sub_eq_zero] using ha

/-- The level-two digit is onto the residue field. -/
theorem level₂_digit_surjective {R : Type} [CommRing R] (red : R →+* ZMod 5)
    (hred : Function.Surjective red) (c pi : R) (hc : red c = -1)
    (hp : red pi = 0) (u : ZMod 5) :
    ∃ s : R, red (digit₂ c pi s) = u := by
  have ff : ∀ y : ZMod 5, ∃ x : ZMod 5, 3*x + 4*x^3 + 2*x^5 = y := by decide
  obtain ⟨a, ha⟩ := ff u
  obtain ⟨s, hs⟩ := hred a
  refine ⟨s, ?_⟩
  simpa [digit₂, map_ofNat, hc, hp, hs, show (3424:ZMod 5)=4 by decide,
    show (8:ZMod 5)=3 by decide, show (3:ZMod 5)*(-1)^3=2 by decide] using ha

/-- A level-two unit factors as two values of the normalized norm
polynomials, first matching its residue digit and then the entire remainder. -/
theorem level₂_norm_factorization {K : Type} [Field K] (V : ValuationSubring K)
    [HenselianRing V (IsLocalRing.maximalIdeal V)]
    (res : IsLocalRing.ResidueField V ≃+* ZMod 5)
    (c pi : V) (hc : res (IsLocalRing.residue V c) = -1)
    (hpi : res (IsLocalRing.residue V pi) = 0)
    (hdiv : ∀ x : V, res (IsLocalRing.residue V x) = 0 → ∃ t : V, x = pi*t)
    (y : V) : ∃ s t : V,
    1+pi^2*y = (1+pi^2*digit₂ c pi s)*(1+pi^3*digit₃ c pi t) := by
  let red := res.toRingHom.comp (IsLocalRing.residue V)
  have hs : Function.Surjective red :=
    res.surjective.comp (Ideal.Quotient.mk_surjective)
  obtain ⟨s, hsd⟩ := level₂_digit_surjective red hs c pi hc hpi (red y)
  let d := digit₂ c pi s
  let v := 1+pi^2*d
  have hv : red v = 1 := by
    change red (1+pi^2*d) = 1
    rw [map_add, map_one, map_mul, map_pow, show red pi = 0 from hpi]
    simp
  have hu : IsUnit v := by
    rw [← IsLocalRing.notMem_maximalIdeal]
    intro e
    have e' := Ideal.Quotient.eq_zero_iff_mem.mpr e
    have he := congrArg res e'
    exact (show (1:ZMod 5) ≠ 0 by decide) (hv.symm.trans (he.trans res.map_zero))
  obtain ⟨b, hb⟩ := hdiv (y-d) (by change red (y-d)=0; rw [map_sub, show red d=red y from hsd, sub_self])
  obtain ⟨u, hu₁⟩ := hu
  obtain ⟨t, ht⟩ := level₃_hensel_surjective V res c pi hc hpi (↑u⁻¹ * b)
  refine ⟨s,t,?_⟩
  change 1+pi^2*y = v*(1+pi^3*digit₃ c pi t)
  rw [← hu₁]
  rw [ht, mul_add, mul_one]
  calc
    _ = (1+pi^2*d) + pi^3*b := by linear_combination pi^2*hb
    _ = _ := by
      change v+pi^3*b = _
      rw [← hu₁]
      rw [mul_left_comm (u:V), ← mul_assoc (u:V), u.mul_inv, one_mul]

#print axioms level₂_digit_surjective
#print axioms level₂_norm_factorization

#print axioms level₃_hensel_surjective

end Fifth42
