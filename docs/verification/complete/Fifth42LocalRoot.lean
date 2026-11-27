import Mathlib.FieldTheory.KummerPolynomial
import Mathlib.Algebra.Field.ZMod
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.LinearCombination

namespace Fifth42
open Polynomial

/-- The putative local root reduces to 2, but every lift of 2 has
fifth power congruent to 32 modulo π⁵. -/
theorem no_fifth_root_of_residue {R : Type} [CommRing R] [IsDomain R]
    (red : R →+* ZMod 5) (pi c : R) (hpi : pi ≠ 0) (hpi0 : red pi = 0)
    (hc0 : red c ≠ 0) (h5 : (5:R)=c*pi^4)
    (hdiv : ∀ x : R, red x = 0 → ∃ t : R, x = pi*t) :
    ∀ x : R, x^5 ≠ 42 := by
  let : Fact (Nat.Prime 5) := ⟨by decide⟩
  intro x hx
  have xr : (red x)^5 = 42 := by rw [← map_pow, hx, map_ofNat]
  have fin₅ : ∀ j : ZMod 5, j^5 = 42 → j = 2 := by decide
  obtain ⟨v, hv⟩ := hdiv (x-2) (by simp [fin₅ _ xr,map_ofNat])
  have hform : x=2+pi*v := by linear_combination hv
  have above : x^5 = 32+pi^5*(16*c*v+16*c*pi*v^2+8*c*pi^2*v^3+2*c*pi^3*v^4+v^5) := by
    rw [hform]
    linear_combination (16*pi*v+16*pi^2*v^2+8*pi^3*v^3+2*pi^4*v^4)*h5
  have cancel : pi^4*(2*c)=pi^4*(pi*(16*c*v+16*c*pi*v^2+8*c*pi^2*v^3+2*c*pi^3*v^4+v^5)) := by
    linear_combination above - hx - 2*h5
  have residue := congrArg red (mul_left_cancel₀ (pow_ne_zero _ hpi) cancel)
  have hc : (2:ZMod 5)*red c = 0 := by simpa [hpi0,map_ofNat] using residue
  exact (mul_ne_zero (by decide : (2:ZMod 5) ≠ 0) hc0) hc

/-- Connect the local-root obstruction to the binomial field construction. -/
theorem kummer42_irreducible_of_residue {R K : Type} [CommRing R] [IsDomain R] [Field K]
    (incl : R →+* K) (hincl : Function.Injective incl)
    (red : R →+* ZMod 5) (pi c : R) (hpi : pi ≠ 0) (hpi0 : red pi = 0)
    (hc0 : red c ≠ 0) (h5 : (5:R)=c*pi^4)
    (hdiv : ∀ x : R, red x = 0 → ∃ t : R, x = pi*t)
    (hlift : ∀ x : K, x^5 = 42 → ∃ y : R, incl y = x) :
    Irreducible (X^5 - C (42:K)) := by
  apply irreducible_X_pow_sub_C_of_prime (by decide : Nat.Prime 5)
  intro x hx
  obtain ⟨y, rfl⟩ := hlift x hx
  apply no_fifth_root_of_residue red pi c hpi hpi0 hc0 h5 hdiv y
  apply hincl
  simpa only [map_pow,map_ofNat] using hx

#print axioms no_fifth_root_of_residue
#print axioms kummer42_irreducible_of_residue

end Fifth42
