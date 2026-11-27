import Mathlib.FieldTheory.KummerExtension
import Mathlib.RingTheory.Norm.Transitivity
import Mathlib.Tactic.Ring
import Fifth42ShiftedNorm

/-! Interpret the explicit conjugate product as the norm in the Kummer
field, conditional only on the indicated binomial being irreducible. -/
namespace Fifth42

open Polynomial AdjoinRoot
open scoped BigOperators

noncomputable section

private def rootsFin {K : Type} [Field K] {z : K} (hz : IsPrimitiveRoot z 5) :
    Fin 5 ≃ rootsOfUnity 5 K :=
  Equiv.ofBijective
    (fun i ↦ rootsOfUnity.mkOfPowEq (z ^ i.val) (by rw [← pow_mul, mul_comm, pow_mul, hz.pow_eq_one, one_pow]))
    ⟨fun i j h ↦ Fin.ext (hz.pow_inj i.isLt j.isLt (by
        exact congrArg (fun η : rootsOfUnity 5 K ↦ ((η : Kˣ) : K)) h)),
      fun η ↦ by
        have hη : ((η : Kˣ) : K)^5 = 1 := by exact_mod_cast (mem_rootsOfUnity' 5 (η : Kˣ)).mp η.property
        obtain ⟨j, hj, he⟩ := hz.eq_pow_of_pow_eq_one hη
        refine ⟨⟨j, hj⟩, ?_⟩
        apply Subtype.ext
        apply Units.ext
        exact he⟩

theorem shifted_cube_norm {K : Type} [Field K] {z : K}
    (hz : IsPrimitiveRoot z 5) (H : Irreducible (X ^ 5 - C (42 : K))) (t : K) :
    Algebra.norm K
      (1+algebraMap K (AdjoinRoot (X^5-C (42:K))) t *
           (AdjoinRoot.root (X^5-C (42:K))-2)^3) =
       1-40*t+1900*t^2+85600*t^3+716000*t^4+1000*t^5 := by
  classical
  let := Fact.mk H
  let L := AdjoinRoot (X ^ 5 - C (42:K))
  let : Field L := inferInstanceAs (Field (AdjoinRoot _))
  have hζ : (primitiveRoots 5 K).Nonempty := ⟨z, (mem_primitiveRoots (by decide)).2 hz⟩
  let : IsSplittingField K L (X ^ 5 - C (42:K)) :=
    isSplittingField_AdjoinRoot_X_pow_sub_C hζ H
  let : IsGalois K L := isGalois_of_isSplittingField_X_pow_sub_C hζ H L
  let : FiniteDimensional K L := Module.Finite.of_basis (AdjoinRoot.powerBasis H.ne_zero).basis
  let e : Fin 5 ≃ (L ≃ₐ[K] L) := (rootsFin hz).trans (autAdjoinRootXPowSubCEquiv hζ H).toEquiv
  let a : L := AdjoinRoot.root (X ^ 5 - C (42:K))
  let Z : L := algebraMap K L z
  let T : L := algebraMap K L t
  let x : L := 1 + T*(a-2)^3
  change Algebra.norm K x = _
  have hσ (i : Fin 5) : e i x = 1+T*(Z^i.val*a-2)^3 := by
    have ha : e i a = Z^i.val*a := by
      change autAdjoinRootXPowSubC _ _ _ _ = _
      rw [autAdjoinRootXPowSubC_root, Algebra.smul_def, ← map_pow]
      rfl
    simp only [x, T, map_add, map_one, map_mul, map_pow, map_sub, map_ofNat, AlgEquiv.commutes, ha]
  apply (algebraMap K L).injective
  rw [Algebra.norm_eq_prod_automorphisms (K := K) (L := L) x]
  rw [← Fintype.prod_equiv e (fun i ↦ 1+T*(Z^i.val*a-2)^3) (fun σ ↦ σ x) (fun i ↦ (hσ i).symm)]
  have ha5 : a^5 = 42 := by
    change (AdjoinRoot.root (X^5-C (42:K)))^5 = _
    calc
      _ = algebraMap K L (42:K) := root_X_pow_sub_C_pow 5 (42:K)
      _ = _ := map_ofNat (algebraMap K L) 42
  have hz5 : Z^4+Z^3+Z^2+Z+1=0 := by
    have hprim : IsPrimitiveRoot Z 5 := hz.map_of_injective (algebraMap K L).injective
    have hn : Z - 1 ≠ 0 := sub_ne_zero.mpr (by
      intro eq
      have hd := hprim.dvd_of_pow_eq_one 1 (by simpa using eq)
      norm_num at hd)
    apply (mul_left_cancel₀ hn)
    rw [mul_zero]
    calc
      _ = Z^5-1 := by ring
      _ = 0 := sub_eq_zero.mpr hprim.pow_eq_one
  simp only [map_add, map_sub, map_one, map_mul, map_pow, map_ofNat]
  calc
    (∏ i : Fin 5, (1+T*(Z^i.val*a-2)^3)) =
        (1+T*(a-2)^3)*(1+T*(Z*a-2)^3)*(1+T*(Z^2*a-2)^3)*
          (1+T*(Z^3*a-2)^3)*(1+T*(Z^4*a-2)^3) := by
      simp [Fin.prod_univ_succ]
      ring
    _ = _ := shifted_cube_product a Z T ha5 hz5

#print axioms shifted_cube_norm

end
end Fifth42
