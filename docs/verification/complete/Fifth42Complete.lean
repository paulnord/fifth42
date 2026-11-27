import Fifth42SymbolFinish
open scoped NumberField
open NumberField Ideal IsDedekindDomain ClassFieldTheory
namespace Fifth42
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

noncomputable abbrev P2 := tamePlace 2 p2_ok
noncomputable abbrev P3 := tamePlace 3 p3_ok
noncomputable abbrev P7 := tamePlace 7 p7_ok

private theorem lt_for_pair (u v w : ℤ) (he : u^5+v^5+w^5=42) (p : ℕ)
    (hp : p=2 ∨ p=3 ∨ p=7) :
    elog p (u%p).toNat (v%p).toNat < 5 := by
  have hp0 : 0<p := by rcases hp with rfl|rfl|rfl <;> decide
  apply tameLog_lt p hp (residue p hp0 u) (residue p hp0 v)
  have hN := pair_nonzero u v w he p hp0
    (by rcases hp with rfl|rfl|rfl <;> decide)
    (by rcases hp with rfl|rfl|rfl <;> decide)
    (by rcases hp with rfl|rfl|rfl <;> decide)
  intro hn
  change (u%(p:ℤ)).toNat=0 ∧ (v%(p:ℤ)).toNat=0 at hn
  have pos : (p:ℤ) ≠ 0 := Int.natCast_ne_zero.mpr (by omega)
  have hu := Int.emod_nonneg u pos
  have hv := Int.emod_nonneg v pos
  exact hN ⟨by omega,by omega⟩

private theorem tame_finset_product (b : Fˣ) (hout : ∀ P : HeightOneSpectrum (𝓞 F),
    P ≠ P2 → P ≠ P3 → P ≠ P7 → P ≠ prime5_place → finiteSymbol5 P a42 b = 1)
    (h5 : finiteSymbol5 prime5_place a42 b = 1) :
    finiteSymbol5 P2 a42 b * finiteSymbol5 P3 a42 b * finiteSymbol5 P7 a42 b = 1 := by
  classical
  let S : Finset (HeightOneSpectrum (𝓞 F)) := {P2,P3,P7,prime5_place}
  have all := finite_reciprocity_on a42 b S (by
    intro P h
    have notMem := mt (fun q ↦ q : P ∈ S → P ∈ S) h
    simp only [S, Finset.mem_insert,Finset.mem_singleton,not_or] at notMem
    exact hout P notMem.1 notMem.2.1 notMem.2.2.1 notMem.2.2.2)
  have neq {p q : ℕ} [Fact (Nat.Prime p)] [Fact (Nat.Prime q)] (hp : p=2 ∨ p=3 ∨ p=7)
      (hq : q=2 ∨ q=3 ∨ q=7) (h : p^4 ≠ q^4) : tamePlace p hp ≠ tamePlace q hq := by
    intro e
    exact h ((tame_norm p hp).symm.trans (by rw [e,tame_norm q hq]))
  have e23 : P2 ≠ P3 := neq p2_ok p3_ok (by decide)
  have e27 : P2 ≠ P7 := neq p2_ok p7_ok (by decide)
  have e37 : P3 ≠ P7 := neq p3_ok p7_ok (by decide)
  have e25 : P2 ≠ prime5_place := tame_place_not_five 2 p2_ok
  have e35 : P3 ≠ prime5_place := tame_place_not_five 3 p3_ok
  have e75 : P7 ≠ prime5_place := tame_place_not_five 7 p7_ok
  simpa [S, e23, e27,e37,e25,e35,e75,h5,mul_assoc] using all

private theorem zRoot_pow_one (k : ℕ) (h : zRoot^k = 1) : 5 ∣ k := by
  have hh := congrArg (fun a : rootsOfUnity (n:ℕ) F ↦ ((a.1:Fˣ):F)) h
  apply (z_primitive.pow_eq_one_iff_dvd _).mp
  simpa only [Subgroup.coe_pow, Units.val_pow_eq_pow_val, Subgroup.coe_one,Units.val_one,zRoot_field] using hh

/-- The pairwise Eisenstein identity, now proved over the actual field. -/
theorem actual_pairwise_eisenstein : PairwiseEisenstein := by
  intro u v w h he hp
  obtain ⟨h5,hd⟩ := modulus_primary u v h hp
  let k := 5-h%5
  let l (p : ℕ) := elog p (u%p).toNat (v%p).toNat
  have hL (p : ℕ) (ht : p=2 ∨ p=3 ∨ p=7) : l p < 5 := lt_for_pair u v w he p ht
  have hn : (u:𝓞 F)+zI*(v:𝓞 F) ≠ 0 := by
    intro e
    exact tame_linear_not_mem 2 p2_ok u v (hL 2 p2_ok) (e ▸ P2.asIdeal.zero_mem)
  let b := bLin u v hn
  let c := zRoot.1^k*b
  have hc : (c:F)=z^k*((u:F)+z*(v:F)) := by
    change (zRoot.1^k*b:Fˣ).val=z^k*((u:F)+z*(v:F))
    rw [Units.val_mul,Units.val_pow_eq_pow_val,zRoot_field]
    have hcoe : (b:F)=(u:F)+z*(v:F) := by
      change (algebraMap (𝓞 F) F) ((u:𝓞 F)+zI*(v:𝓞 F)) = _
      rw [map_add,map_mul,map_intCast,map_intCast,show (algebraMap (𝓞 F) F) zI = z from rfl]
    rw [hcoe]
  have hw := finiteSymbol5_at_five_of_rotated c u v k h5 hd hc
  have step (P : HeightOneSpectrum (𝓞 F)) :
      finiteSymbol5 P a42 c = (finiteSymbol5 P a42 zRoot.1)^k * finiteSymbol5 P a42 b := by
    change finiteSymbol5Right P a42 (zRoot.1^k*b) =
      (finiteSymbol5Right P a42 zRoot.1)^k * finiteSymbol5Right P a42 b
    rw [map_mul,map_pow]
  have hout : ∀ P : HeightOneSpectrum (𝓞 F), P ≠ P2 → P ≠ P3 → P ≠ P7 → P ≠ prime5_place →
      finiteSymbol5 P a42 c = 1 := by
    intro P q2 q3 q7 q5
    have q42 := outside_not_42 P q2 q3 q7
    rw [step,outside_symbol_z P q5 q42,outside_symbol_linear P q5 q42 u v w he hn,one_pow,one_mul]
  have prod := tame_finset_product c hout hw
  have ht (p : ℕ) [Fact (Nat.Prime p)] (hprime : p=2 ∨ p=3 ∨ p=7) :
      finiteSymbol5 (tamePlace p hprime) a42 c =
        (zRoot^(elog p 0 1*k+l p))⁻¹ := by
    rw [step,tame_symbol_z p hprime,tame_symbol_linear p hprime u v (hL p hprime) hn]
    change ((zRoot^elog p 0 1)⁻¹)^k * (zRoot^l p)⁻¹ = _
    rw [inv_pow,← pow_mul,← mul_inv_rev, ← pow_add]
    congr 2
    omega
  have t2 : elog 2 0 1=3 := by decide
  have t3 : elog 3 0 1=1 := by decide
  have t7 : elog 7 0 1=0 := by decide
  rw [ht 2 p2_ok,ht 3 p3_ok,ht 7 p7_ok,t2,t3,t7] at prod
  have hhProd : (zRoot^(3*k+l 2))⁻¹ * (zRoot^(1*k+l 3))⁻¹ * (zRoot^(0*k+l 7))⁻¹ = 1 := prod
  rw [← mul_inv_rev,← mul_inv_rev,← pow_add,← pow_add] at hhProd
  have hdiv := zRoot_pow_one _ (inv_eq_one.mp hhProd)
  rw [t2,t3,t7]
  change (l 2+l 3+l 7)%5=(4*h)%5
  change 5 ∣ (0*k+l 7)+((1*k+l 3)+(3*k+l 2)) at hdiv
  dsimp only [k] at hdiv
  omega

/-- No three signed integer fifth powers sum to 42. -/
theorem no_three_fifth_powers_sum_42 (x y z : ℤ) : x^5+y^5+z^5 ≠ 42 :=
  no_solution_of_pairwiseEisenstein actual_pairwise_eisenstein x y z

#print axioms actual_pairwise_eisenstein
#print axioms no_three_fifth_powers_sum_42
end Fifth42
