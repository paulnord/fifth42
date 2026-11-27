import Fifth42KummerNorm
import Fifth42Hensel
import Fifth42LocalRoot
import Mathlib.RingTheory.Valuation.LocalSubring

namespace Fifth42
open Polynomial AdjoinRoot

/-- In a Henselian valuation ring with residue field F₅ and uniformizer π
satisfying 5=cπ⁴, each level-two principal unit is a Kummer norm. -/
theorem level₂_is_kummer_norm {K : Type} [Field K] (V : ValuationSubring K)
    [HenselianRing V (IsLocalRing.maximalIdeal V)]
    (res : IsLocalRing.ResidueField V ≃+* ZMod 5)
    (z : K) (hz : IsPrimitiveRoot z 5)
    (c pi : V) (hc : res (IsLocalRing.residue V c) = -1)
    (hpi : res (IsLocalRing.residue V pi) = 0)
    (hπ : pi ≠ 0) (h5 : (5:V)=c*pi^4)
    (hdiv : ∀ x : V, res (IsLocalRing.residue V x) = 0 → ∃ t : V, x = pi*t)
    (y : V) :
    ∃ w : (AdjoinRoot (X^5-C (42:K)))ˣ,
      Algebra.norm K (w : AdjoinRoot (X^5-C (42:K))) = ((1+pi^2*y : V) : K) := by
  let red := res.toRingHom.comp (IsLocalRing.residue V)
  have H : Irreducible (X ^ 5 - C (42 : K)) := by
    apply kummer42_irreducible_of_residue V.subtype Subtype.val_injective red pi c hπ
      hpi (hc.symm ▸ (by decide : (-1:ZMod 5) ≠ 0)) h5 hdiv
    intro x hx
    refine IsIntegrallyClosed.isIntegral_iff.mp ?_
    exact ⟨X^5-C (42:V), monic_X_pow_sub_C _ (by decide), by simp [map_ofNat, hx]⟩
  let := Fact.mk H
  let L := AdjoinRoot (X^5-C (42:K))
  let : Module.Finite K L := Module.Finite.of_basis (AdjoinRoot.powerBasis H.ne_zero).basis
  let : Module.Free K L := Module.Free.of_basis (AdjoinRoot.powerBasis H.ne_zero).basis
  let D := (⇑(algebraMap K L))
  let a : L := AdjoinRoot.root (X^5-C (42:K))
  let i : V →+* K := V.subtype
  have hpK : i pi ≠ 0 := by
    intro h
    exact hπ (Subtype.ext h)
  have h5K : (5:K)=i c*(i pi)^4 := by simpa [map_ofNat] using congrArg i h5
  obtain ⟨s,t,he⟩ := level₂_norm_factorization V res c pi hc hpi hdiv y
  let S : K := i s/(i pi)^2
  let T : K := i t/i pi
  let w₂ : L := 1+D S*(a-2)^3
  let w₃ : L := 1+D T*(a-2)^3
  have hw₂ : Algebra.norm K w₂ = i (1+pi^2*digit₂ c pi s) := by
    change Algebra.norm K (1+algebraMap K L S*(a-2)^3) = _
    rw [shifted_cube_norm hz H]
    change normPolynomial S = _
    rw [normPolynomial_level₂ (i c) (i pi) (i s) S h5K (by
      exact (div_mul_cancel₀ (i s) (pow_ne_zero _ hpK)).symm.trans (mul_comm _ _))]
    simp [digit₂,map_ofNat]
  have hw₃ : Algebra.norm K w₃ = i (1+pi^3*digit₃ c pi t) := by
    change Algebra.norm K (1+algebraMap K L T*(a-2)^3) = _
    rw [shifted_cube_norm hz H]
    change normPolynomial T = _
    rw [normPolynomial_level₃ (i c) (i pi) (i t) T h5K (by
      exact (div_mul_cancel₀ (i t) hpK).symm.trans (mul_comm _ _))]
    simp [digit₃,map_ofNat]
  have hw : Algebra.norm K (w₂*w₃) = i (1+pi^2*y) := by
    rw [map_mul, hw₂, hw₃, ← map_mul, ← he]
  have hyv : (1+pi^2*y : V) ≠ 0 := by
    intro h
    let red := res.toRingHom.comp (IsLocalRing.residue V)
    have e := congrArg red h
    simp [map_add,map_mul,map_pow,show red pi=0 from hpi] at e
    exact (show (1:ZMod 5) ≠ 0 by decide) e
  have hn : w₂*w₃ ≠ 0 := by
    intro h
    have : i (1+pi^2*y) = 0 := by simpa [h] using hw.symm
    exact hyv (Subtype.ext this)
  exact ⟨Units.mk0 (w₂*w₃) hn, hw⟩

#print axioms level₂_is_kummer_norm

end Fifth42
