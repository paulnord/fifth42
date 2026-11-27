import Fifth42CyclotomicPlaces
import Fifth42UnitNorm
import Nyll.ClassFieldTheory.AlgebraicNumberTheory.Completion.LocalField
import Nyll.ValuedFieldTheory.Valuation.Topology.AdicCompletionInverseLimit

open scoped NumberField WithZero
open NumberField IsDedekindDomain Polynomial

namespace Fifth42

abbrev C5 := prime5_place.adicCompletion F
noncomputable abbrev V5 := prime5_place.adicCompletionIntegers F

noncomputable def piC : V5 := algebraMap (𝓞 F) V5 pi5

noncomputable def completion_residue5 : IsLocalRing.ResidueField V5 ≃+* ZMod 5 :=
  (GlobalClassFieldTheory.ClassFieldAxiom.ringOfIntegersQuotientEquivAdicResidueField
    (K := F) prime5_place).symm.trans prime5_residue

private theorem pi5_ne_zero : pi5 ≠ 0 := by
  intro eq
  exact prime5_ne_bot (by simp [prime5,eq])

private theorem piC_uniformizer :
    (Valued.v : Valuation C5 (WithZero (Multiplicative ℤ))).IsUniformizer (piC : C5) := by
  let v : Valuation C5 (WithZero (Multiplicative ℤ)) := Valued.v
  have hp : v (piC : C5) = WithZero.exp (-1) := by
    change Valued.v (algebraMap (𝓞 F) C5 pi5) = _
    calc
      _ = prime5_place.valuation F (algebraMap (𝓞 F) F pi5) :=
        prime5_place.valuedAdicCompletion_eq_valuation (K := F) pi5
      _ = prime5_place.intValuation pi5 := prime5_place.valuation_of_algebraMap (K := F) pi5
      _ = _ := prime5_place.intValuation_singleton pi5_ne_zero rfl
  apply Valuation.IsUniformizer.iff.mpr
  rw [hp]
  exact congrArg Units.val (Valuation.IsRankOneDiscrete.generator_eq_exp_neg_one_of_mem_range ⟨_,hp⟩).symm

theorem piC_maximal : IsLocalRing.maximalIdeal V5 = Ideal.span {piC} :=
  piC_uniformizer.is_generator

private instance henselian5 : HenselianRing V5 (IsLocalRing.maximalIdeal V5) := by
  let : IsAdicComplete (IsLocalRing.maximalIdeal V5) V5 := by
    have e := LubinTate.Valuations.completeValuedField_uniformizerIdeal_isAdicComplete piC_uniformizer
    rw [LubinTate.Valuations.completeValuedField_uniformizerPowerIdeal_one_eq_maximalIdeal
       piC_uniformizer] at e
    exact e
  infer_instance

noncomputable def zC : V5 := algebraMap (𝓞 F) V5 z_primitive.toInteger

private theorem zC_cyclotomic : zC^4+zC^3+zC^2+zC+1=0 := by
  have hζ : IsPrimitiveRoot zC 5 :=
    z_primitive.toInteger_isPrimitiveRoot.map_of_injective
      (by
        intro x y eq
        have e := congrArg (fun a : V5 ↦ (a:C5)) eq
        change algebraMap (𝓞 F) C5 x = algebraMap (𝓞 F) C5 y at e
        rw [IsScalarTower.algebraMap_apply (𝓞 F) F C5] at e
        exact RingOfIntegers.coe_injective ((algebraMap F C5).injective e))
  apply mul_left_cancel₀ (sub_ne_zero.mpr (hζ.ne_one (by decide)))
  rw [mul_zero]
  calc
    _ = zC^5-1 := by ring
    _ = 0 := sub_eq_zero.mpr hζ.pow_eq_one

/-- The norm lemma at level two, specialized to the actual completion at 5. -/
theorem actual_wild_principal_norm (y : V5) :
    ∃ w : (AdjoinRoot (X^5-C (42:C5)))ˣ,
      Algebra.norm C5 (w : AdjoinRoot (X^5-C (42:C5))) = ((1+piC^2*y : V5) : C5) := by
  have hpz : piC = zC-1 := by simp [piC,pi5,zC]
  obtain ⟨d,hd⟩ := cyclotomic_five_unit zC zC_cyclotomic
  let c := -1+piC*d
  have h5 : (5:V5)=c*piC^4 := by simpa [c,hpz] using hd
  let red := completion_residue5.toRingHom.comp (IsLocalRing.residue V5)
  have hpi : red piC=0 := by
    change completion_residue5 (IsLocalRing.residue V5 piC)=0
    rw [← completion_residue5.map_zero]
    congr 1
    exact (IsLocalRing.residue_eq_zero_iff _).mpr (by rw [piC_maximal]; exact Ideal.mem_span_singleton_self _)
  have hc : red c = -1 := by
    change red (-1+piC*d) = -1
    rw [map_add,map_mul,hpi,zero_mul,add_zero,map_neg,map_one]
  have hπ : piC ≠ 0 := fun e ↦ piC_uniformizer.ne_zero (by simp [e])
  have hdiv : ∀ x : V5, red x=0 → ∃ t : V5, x=piC*t := by
    intro x hx
    have e : IsLocalRing.residue V5 x=0 := completion_residue5.injective (hx.trans completion_residue5.map_zero.symm)
    have h := (IsLocalRing.residue_eq_zero_iff _).mp e
    rw [piC_maximal,Ideal.mem_span_singleton] at h
    exact h
  exact level₂_is_kummer_norm (prime5_place.adicCompletionIntegers F) completion_residue5
    (algebraMap F C5 z) (z_primitive.map_of_injective (algebraMap F C5).injective)
    c piC hc hpi hπ h5 hdiv y

#print axioms actual_wild_principal_norm

end Fifth42
