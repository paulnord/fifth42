import Fifth42AtFive

open scoped NumberField
open NumberField IsDedekindDomain ClassFieldTheory Polynomial

namespace Fifth42
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

noncomputable def a42 : Fˣ := Units.mk0 42 (by norm_num)

private theorem completion_42_as_unit :
    ((Units.map (algebraMap F C5).toMonoidHom a42 : C5ˣ) : C5) = 42 := by
  change algebraMap F C5 42 = 42
  exact map_ofNat (algebraMap F C5) 42

/-- Deep principal units give the identity for the *same* finite-place
Hilbert symbol that appears in the global product. -/
theorem finiteSymbol5_at_five_eq_one_of_deep (b : Fˣ) (y : V5)
    (hb : algebraMap F C5 (b : F) = ((1+piC^2*y : V5) : C5)) :
    finiteSymbol5 prime5_place a42 b = 1 := by
  let B := finitePlaceAdicHilbertPairingFamily F n primitive5_nonempty
  let e : rootsOfUnity 5 F ≃* rootsOfUnity 5 C5 :=
    rootsOfUnityEquivOfPrimitiveRoots (algebraMap F C5).injective primitive5_nonempty
  let A := Units.map (algebraMap F C5).toMonoidHom a42
  let D := Units.map (algebraMap F C5).toMonoidHom b
  have hm : IsKummerNorm C5 n A D := by
    unfold IsKummerNorm KummerAlgebra
    change ∃ w : (AdjoinRoot (X^5-C (A:C5)))ˣ,
      Algebra.norm C5 (w : AdjoinRoot (X^5-C (A:C5))) = (D:C5)
    rw [show (A:C5)=42 from completion_42_as_unit]
    change ∃ w : (AdjoinRoot (X^5-C (42:C5)))ˣ,
      Algebra.norm C5 (w : AdjoinRoot (X^5-C (42:C5))) = algebraMap F C5 (b:F)
    rw [hb]
    exact actual_wild_principal_norm y
  have hnorm := ((actual_cyclotomic_reciprocity.1 prime5_place).2.2.2 A D).mpr hm
  change e.symm ((B prime5_place).symbol A D)=1
  exact (congrArg e.symm hnorm).trans (map_one _)

#print axioms finiteSymbol5_at_five_eq_one_of_deep

end Fifth42
