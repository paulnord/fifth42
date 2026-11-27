import Fifth42ReciprocityAudit
import Mathlib.Algebra.Field.ZMod
import Mathlib.Tactic.IntervalCases

open scoped NumberField
open NumberField Ideal IsDedekindDomain
open IsCyclotomicExtension.Rat

namespace Fifth42

noncomputable def z : F := IsCyclotomicExtension.zeta 5 ℚ F
theorem z_primitive : IsPrimitiveRoot z 5 := IsCyclotomicExtension.zeta_spec 5 ℚ F
noncomputable def pi5 : 𝓞 F := z_primitive.toInteger - 1
noncomputable def prime5 : Ideal (𝓞 F) := Ideal.span {pi5}

private instance : Fact (Nat.Prime 5) := ⟨by decide⟩
private instance : IsCyclotomicExtension ({5^(0+1)}:Set ℕ) ℚ F := cyclotomicFive

theorem prime5_absNorm : Ideal.absNorm prime5 = 5 :=
  absNorm_span_zeta_sub_one 5 0 z_primitive

theorem prime5_ne_bot : prime5 ≠ ⊥ :=
  span_zeta_sub_one_ne_bot 5 0 z_primitive

instance prime5_prime : prime5.IsPrime := isPrime_span_zeta_sub_one' 5 z_primitive

noncomputable def prime5_place : HeightOneSpectrum (𝓞 F) := ⟨prime5, prime5_prime, prime5_ne_bot⟩

/-- The residue ring at the prime above 5 is literally a model of F₅. -/
noncomputable def prime5_residue : (𝓞 F ⧸ prime5) ≃+* ZMod 5 := by
  classical
  let : Finite (𝓞 F ⧸ prime5) := z_primitive.finite_quotient_span_sub_one'
  let : Fintype (𝓞 F ⧸ prime5) := Fintype.ofFinite _
  exact (ZMod.ringEquivOfPrime _ (by decide : Nat.Prime 5)
    (by rw [← Nat.card_eq_fintype_card, ← Ideal.absNorm_eq_natCard, prime5_absNorm])).symm

theorem only_above_five (P : Ideal (𝓞 F)) [P.IsPrime] [P.LiesOver (Ideal.span {(5:ℤ)})] :
    P = prime5 :=
  eq_span_zeta_sub_one_of_liesOver' 5 F z_primitive P

theorem order_tame (p : ℕ) (hp : p=2 ∨ p=3 ∨ p=7) : orderOf (p:ZMod 5) = 4 := by
  let : Fact (Nat.Prime 2) := ⟨by decide⟩
  rcases hp with rfl|rfl|rfl <;>
    exact orderOf_eq_prime_pow (p := 2) (n := 1) (by decide) (by decide)

theorem tame_place_degree_e (p : ℕ) (hp : p=2 ∨ p=3 ∨ p=7) [Fact (Nat.Prime p)]
    (P : Ideal (𝓞 F)) [P.IsPrime] [P.LiesOver (Ideal.span {(p:ℤ)})] :
    P.inertiaDeg ℤ = 4 ∧ P.ramificationIdx ℤ = 1 ∧ Ideal.absNorm P = p^4 := by
  have h : ¬ p ∣ 5 := by rcases hp with rfl|rfl|rfl <;> decide
  have hf : P.inertiaDeg ℤ = 4 := (inertiaDeg_eq_of_not_dvd p F P h).trans (order_tame p hp)
  have hr := ramificationIdx_eq_of_not_dvd p F P h
  exact ⟨hf,hr, by rw [← Ideal.pow_inertiaDeg p P, hf]⟩

theorem tame_prime_unique (p : ℕ) [fact : Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    ((Ideal.span {(p:ℤ)}).primesOver (𝓞 F)).ncard = 1 := by
  let P : Ideal ℤ := Ideal.span {(p:ℤ)}
  let : P.IsPrime := by
    apply (Ideal.span_singleton_prime (by exact_mod_cast fact.out.ne_zero : (p:ℤ) ≠ 0)).mpr
    exact Int.prime_iff_natAbs_prime.mpr (by simpa using fact.out)
  let : IsGalois ℚ F := IsCyclotomicExtension.isGalois ({5}:Set ℕ) ℚ F
  have h : ¬ p ∣ 5 := by rcases hp with rfl|rfl|rfl <;> decide
  have hf := (inertiaDegIn_eq_of_not_dvd p F h).trans (order_tame p hp)
  have hr := ramificationIdxIn_eq_of_not_dvd p F h
  have hcard : Nat.card (F ≃ₐ[ℚ] F) = 4 := by
    rw [IsGalois.card_aut_eq_finrank, IsCyclotomicExtension.finrank F (Polynomial.cyclotomic.irreducible_rat (by decide : 0<5))]
    decide
  have eq := Ideal.ncard_primesOver_mul_ramificationIdxIn_mul_inertiaDegIn P (𝓞 F) (F ≃ₐ[ℚ] F)
  rw [show P.ramificationIdxIn (𝓞 F)=1 from hr,show P.inertiaDegIn (𝓞 F)=4 from hf,hcard] at eq
  change (P.primesOver (𝓞 F)).ncard = 1
  omega

#print axioms tame_prime_unique

#print axioms prime5_residue
#print axioms only_above_five
#print axioms tame_place_degree_e
end Fifth42
