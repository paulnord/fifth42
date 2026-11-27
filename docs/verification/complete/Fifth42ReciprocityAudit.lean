import Nyll.ClassFieldTheory.Theorems.HilbertSymbols.HilbertProductFormula
import Nyll.ClassFieldTheory.LocalClassFieldTheory.Kummer.GeneralTameFormula
import Mathlib.NumberTheory.NumberField.Cyclotomic.Ideal

open scoped BigOperators NumberField
open NumberField IsDedekindDomain ClassFieldTheory

#print axioms exists_globalHilbertPairingFamily_productFormula
#print axioms finitePlaceAdicHilbertPairingFamily_productFormula
#print axioms LocalClassFieldTheory.Kummer.localHilbertSymbol_tame_formula_general_reduction

namespace Fifth42

abbrev F := CyclotomicField 5 ℚ
abbrev n : ℕ+ := 5
private instance : NeZero ((5:ℕ):ℚ) := ⟨by decide⟩

instance cyclotomicFive : IsCyclotomicExtension ({5}:Set ℕ) ℚ F :=
  CyclotomicField.isCyclotomicExtension 5 ℚ

theorem primitive5_nonempty : (primitiveRoots (n:ℕ) F).Nonempty :=
  ⟨IsCyclotomicExtension.zeta 5 ℚ F, (mem_primitiveRoots (by decide)).2
    (IsCyclotomicExtension.zeta_spec 5 ℚ F)⟩

/-- The global reciprocity formula already instantiated to the actual
cyclotomic number field and the fifth Hilbert pairing. -/
theorem actual_cyclotomic_reciprocity :
    let B := finitePlaceAdicHilbertPairingFamily F n primitive5_nonempty
    GlobalHilbertPairingFamily.IsLocallyHilbert F B ∧
      GlobalHilbertPairingFamily.HasFiniteSupport F B primitive5_nonempty ∧
      ∀ a b : Fˣ,
        (∏ v : InfinitePlace F, globalInfinitePlaceHilbertSymbol F n v a b) *
          ∏ᶠ v : HeightOneSpectrum (𝓞 F),
            GlobalHilbertPairingFamily.finiteFactor F B primitive5_nonempty v a b = 1 :=
  finitePlaceAdicHilbertPairingFamily_productFormula F n primitive5_nonempty

noncomputable def finiteSymbol5 (v : HeightOneSpectrum (𝓞 F)) (a b : Fˣ) :
    rootsOfUnity 5 F :=
  GlobalHilbertPairingFamily.finiteFactor F
    (finitePlaceAdicHilbertPairingFamily F n primitive5_nonempty)
    primitive5_nonempty v a b

theorem finite_reciprocity (a b : Fˣ) :
    ∏ᶠ v : HeightOneSpectrum (𝓞 F), finiteSymbol5 v a b = 1 := by
  have h := actual_cyclotomic_reciprocity.2.2 a b
  have hinf (v : InfinitePlace F) : globalInfinitePlaceHilbertSymbol F n v a b = 1 := by
    unfold globalInfinitePlaceHilbertSymbol
    exact dite_eq_right (by decide)
  simp only [hinf, Finset.prod_const_one, one_mul] at h
  exact h

/-- After the proof of triviality outside a selected set of places, the
global reciprocity constraint reduces to a product on that finite set. -/
theorem finite_reciprocity_on (a b : Fˣ) (places : Finset (HeightOneSpectrum (𝓞 F)))
    (outside : ∀ v, v ∉ places → finiteSymbol5 v a b = 1) :
    (∏ v ∈ places, finiteSymbol5 v a b) = 1 := by
  have hsub : Function.mulSupport (fun v ↦ finiteSymbol5 v a b) ⊆ (places : Set _) := by
    intro v hv
    by_contra hm
    exact hv (outside v hm)
  rw [← finprod_eq_prod_of_mulSupport_subset _ hsub]
  exact finite_reciprocity a b

#print axioms finite_reciprocity
#print axioms finite_reciprocity_on

#print axioms actual_cyclotomic_reciprocity

end Fifth42
