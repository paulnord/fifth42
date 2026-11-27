import Fifth42PrimeData
import Fifth42WildFinish
open scoped NumberField
open NumberField Ideal IsDedekindDomain ClassFieldTheory
open GlobalClassFieldTheory.Reciprocity
open AlgebraicNumberTheory.PowerResidueSymbols
namespace Fifth42

theorem finiteSymbol5_compare (P : HeightOneSpectrum (𝓞 F)) (a b : Fˣ) :
    finiteSymbol5 P a b = globalFinitePlaceHilbertSymbol F n (by norm_num) primitive5_nonempty P a b :=
  finitePlaceAdicHilbertPairingFamily_finiteFactor F n (by norm_num) primitive5_nonempty P a b

theorem finiteSymbol5_skew (P : HeightOneSpectrum (𝓞 F)) (a b : Fˣ) :
    finiteSymbol5 P a b = (finiteSymbol5 P b a)⁻¹ := by
  rw [finiteSymbol5_compare, finiteSymbol5_compare]
  unfold globalFinitePlaceHilbertSymbol
  rw [finitePlaceHilbertSymbol_skew F n (by norm_num) primitive5_nonempty P a b, map_inv]
  rfl

attribute [local instance] HeightOneSpectrum.isPrime

theorem finiteSymbol5_of_factor (P : HeightOneSpectrum (𝓞 F))
    (hv : P ≠ prime5_place) (a b : 𝓞 F) (ha : a ∉ P.asIdeal) (hb0 : b ≠ 0)
    (w c : 𝓞 F) (hf : a - w^5 = b*c) :
    finiteSymbol5 P (nonzeroIntegralFieldUnit F a (fun hz ↦ ha (hz ▸ P.asIdeal.zero_mem)))
      (nonzeroIntegralFieldUnit F b hb0) = 1 := by
  have ha0 : a ≠ 0 := fun hz ↦ ha (hz ▸ P.asIdeal.zero_mem)
  rw [finiteSymbol5_compare]
  unfold globalFinitePlaceHilbertSymbol
  by_cases hb : b ∈ P.asIdeal
  · have heq : Ideal.Quotient.mk P.asIdeal a = (Ideal.Quotient.mk P.asIdeal w)^5 := by
      have e := congrArg (Ideal.Quotient.mk P.asIdeal) hf
      simp only [map_sub,map_pow,map_mul, (Ideal.Quotient.eq_zero_iff_mem).mpr hb,zero_mul] at e
      exact sub_eq_zero.mp e
    have hw0 : Ideal.Quotient.mk P.asIdeal w ≠ 0 := by
      intro h
      rw [h,zero_pow (by decide)] at heq
      exact ha ((Ideal.Quotient.eq_zero_iff_mem).mp heq)
    have rhs : primeIdealPowerResidueSymbol F P n primitive5_nonempty (coprime_norm_five P hv) a ha = 1 := by
      apply (primeIdealPowerResidueSymbol_eq_one_iff F P n primitive5_nonempty (coprime_norm_five P hv) a ha).mpr
      let : P.asIdeal.IsMaximal := P.isPrime.isMaximal P.ne_bot
      let : Field (𝓞 F ⧸ P.asIdeal) := Ideal.Quotient.field P.asIdeal
      refine ⟨Units.mk0 _ hw0, Units.ext ?_⟩
      exact heq.symm
    rw [finitePlaceHilbertSymbol_integral_eq_primeIdealPowerResidueFactor F n (by norm_num) primitive5_nonempty P
      (away_five P hv) (coprime_norm_five P hv) a b ha0 hb0 ha, rhs,map_one,one_pow,map_one]
    rfl
  · rw [finitePlaceHilbertSymbol_integral_units_eq_one F n (by norm_num) primitive5_nonempty P
      (away_five P hv) a b ha0 hb0 ha hb, map_one]
    rfl
#print axioms finiteSymbol5_of_factor
end Fifth42
