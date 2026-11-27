import Fifth42CyclotomicPlaces
import Nyll.ClassFieldTheory.GlobalClassFieldTheory.Reciprocity.PowerResidueReciprocity
import Mathlib.Tactic.FinCases
open scoped NumberField
open NumberField Ideal IsDedekindDomain ClassFieldTheory
open GlobalClassFieldTheory.Reciprocity
open AlgebraicNumberTheory.PowerResidueSymbols
namespace Fifth42

theorem lies_over_of_nat_mem (p : ℕ) [Fact (Nat.Prime p)]
    (P : HeightOneSpectrum (𝓞 F)) (hp : (p:𝓞 F) ∈ P.asIdeal) :
    P.asIdeal.LiesOver (Ideal.span {(p:ℤ)}) := by
  have h0 : (Ideal.span {(p:ℤ)}) ≤ P.asIdeal.under ℤ := by
    rw [Ideal.span_singleton_le_iff_mem]
    change (algebraMap ℤ (𝓞 F) (p:ℤ)) ∈ P.asIdeal
    simpa using hp
  exact ⟨(Int.ideal_span_isMaximal_of_prime p).eq_of_le
    (by simpa using P.isPrime.ne_top) h0⟩

noncomputable def tamePlace (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    HeightOneSpectrum (𝓞 F) := by
  let h := Set.ncard_eq_one.mp (tame_prime_unique p hp)
  let P := h.choose
  have hP := h.choose_spec
  have hmem : P ∈ (Ideal.span {(p:ℤ)}).primesOver (𝓞 F) := by exact hP.symm ▸ Set.mem_singleton P
  let hPrime : P.IsPrime := hmem.1
  have hNZ : P ≠ ⊥ := by
    let : P.LiesOver (Ideal.span {(p:ℤ)}) := hmem.2
    have h := (Ideal.mem_of_liesOver (p := Ideal.span {(p:ℤ)}) (P := P) (p:ℤ)).mp
      (Ideal.mem_span_singleton_self _)
    intro e
    rw [e, Ideal.mem_bot] at h
    simp at h
    exact (Fact.out : Nat.Prime p).ne_zero h
  exact ⟨P,hPrime,hNZ⟩

instance tamePlace_lies_over (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    (tamePlace p hp).asIdeal.LiesOver (Ideal.span {(p:ℤ)}) := by
  let h := Set.ncard_eq_one.mp (tame_prime_unique p hp)
  have hmem : h.choose ∈ (Ideal.span {(p:ℤ)}).primesOver (𝓞 F) := by
    let P := h.choose
    have hs : (Ideal.span {(p:ℤ)}).primesOver (𝓞 F) = {P} := h.choose_spec
    change P ∈ _
    exact hs.symm ▸ Set.mem_singleton P
  exact hmem.2

theorem tamePlace_of_mem (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7)
    (v : HeightOneSpectrum (𝓞 F)) (hm : (p:𝓞 F) ∈ v.asIdeal) : v=tamePlace p hp := by
  let h := Set.ncard_eq_one.mp (tame_prime_unique p hp)
  have hv : v.asIdeal ∈ (Ideal.span {(p:ℤ)}).primesOver (𝓞 F) :=
    ⟨v.isPrime,lies_over_of_nat_mem p v hm⟩
  rw [h.choose_spec,Set.mem_singleton_iff] at hv
  exact HeightOneSpectrum.ext hv

theorem prime5_of_mem (v : HeightOneSpectrum (𝓞 F)) (hm : (5:𝓞 F) ∈ v.asIdeal) :
    v=prime5_place := by
  let : Fact (Nat.Prime 5) := ⟨by decide⟩
  let : v.asIdeal.LiesOver (Ideal.span {(5:ℤ)}) := lies_over_of_nat_mem 5 v hm
  exact HeightOneSpectrum.ext (only_above_five v.asIdeal)

theorem not_five_mem (v : HeightOneSpectrum (𝓞 F)) (hv : v ≠ prime5_place) :
    (5:𝓞 F) ∉ v.asIdeal := fun h ↦ hv (prime5_of_mem v h)

theorem coprime_norm_five (v : HeightOneSpectrum (𝓞 F)) (hv : v ≠ prime5_place) :
    (Ideal.absNorm v.asIdeal).Coprime 5 := by
  apply Nat.Coprime.symm
  apply (Nat.Prime.coprime_iff_not_dvd (by decide : Nat.Prime 5)).mpr
  intro hdiv
  obtain ⟨P,hmax,hover,hP⟩ := Ideal.exists_isMaximal_dvd_of_dvd_absNorm'
    (by decide : Nat.Prime 5) v.asIdeal hdiv
  have e : P = v.asIdeal :=
    (v.isPrime.isMaximal v.ne_bot |>.eq_of_le hmax.ne_top (Ideal.le_of_dvd hP)).symm
  have h5 : (5:𝓞 F) ∈ v.asIdeal := by
    have hh : (5:ℤ) ∈ P.under ℤ := by rw [hover]; exact Ideal.mem_span_singleton_self _
    change algebraMap ℤ (𝓞 F) (5:ℤ) ∈ P at hh
    simpa [e] using hh
  exact not_five_mem v hv h5

theorem away_five (v : HeightOneSpectrum (𝓞 F)) (hv : v ≠ prime5_place) :
    v ∉ powerResidueExponentFinitePlaces F n := by
  rw [mem_powerResidueExponentFinitePlaces_iff, powerResidueExponentIdeal, Ideal.dvd_span_singleton]
  exact not_five_mem v hv

theorem tame_norm (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    Ideal.absNorm (tamePlace p hp).asIdeal = p^4 :=
  (tame_place_degree_e p hp (tamePlace p hp).asIdeal).2.2

theorem tame_place_not_five (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    tamePlace p hp ≠ prime5_place := by
  intro e
  have q := tame_norm p hp
  rw [e,show prime5_place.asIdeal=prime5 from rfl,prime5_absNorm] at q
  rcases hp with rfl|rfl|rfl <;> omega

theorem tame_p_mem (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    (p:𝓞 F) ∈ (tamePlace p hp).asIdeal := by
  let P := (tamePlace p hp).asIdeal
  simpa using (Ideal.mem_of_liesOver (p := Ideal.span {(p:ℤ)}) (P := P) (p:ℤ)).mp
    (Ideal.mem_span_singleton_self _)

theorem tame_other_not_mem (p q : ℕ) [Fact (Nat.Prime p)] [Fact (Nat.Prime q)]
    (hp : p=2 ∨ p=3 ∨ p=7) (hq : q=2 ∨ q=3 ∨ q=7) (hne : p≠q) :
    (q:𝓞 F) ∉ (tamePlace p hp).asIdeal := by
  intro h
  have e := tamePlace_of_mem q hq (tamePlace p hp) h
  have hnorm := (tame_norm p hp).symm.trans ((congrArg (fun v : HeightOneSpectrum (𝓞 F) ↦ Ideal.absNorm v.asIdeal) e).trans (tame_norm q hq))
  rcases hp with rfl|rfl|rfl <;> rcases hq with rfl|rfl|rfl <;> omega

theorem tame_multiplicity_p (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    idealPrimeMultiplicity F (tamePlace p hp) (Ideal.span {(p:𝓞 F)}) = 1 := by
  let P := tamePlace p hp
  have hmap : Ideal.map (algebraMap ℤ (𝓞 F)) (Ideal.span {(p:ℤ)}) = Ideal.span {(p:𝓞 F)} := by simp [Ideal.map_span]
  have hnz : Ideal.span {(p:𝓞 F)} ≠ ⊥ := by
    rw [ne_eq,Ideal.span_singleton_eq_bot]
    exact Nat.cast_ne_zero.mpr (Fact.out : Nat.Prime p).ne_zero
  have hcount := Ideal.IsDedekindDomain.ramificationIdx_eq_factors_count
    (Ideal.span {(p:ℤ)}) P.asIdeal (hmap.symm ▸ hnz)
  rw [hmap, UniqueFactorizationMonoid.factors_eq_normalizedFactors] at hcount
  unfold idealPrimeMultiplicity
  rw [Ideal.count_associates_factors_eq (show Ideal.span {(p:𝓞 F)} ≠ 0 from hnz) P.isPrime P.ne_bot, ← hcount]
  exact (tame_place_degree_e p hp P.asIdeal).2.1


abbrev p2_ok : 2=2 ∨ 2=3 ∨ 2=7 := Or.inl rfl
abbrev p3_ok : 3=2 ∨ 3=3 ∨ 3=7 := Or.inr (Or.inl rfl)
abbrev p7_ok : 7=2 ∨ 7=3 ∨ 7=7 := Or.inr (Or.inr rfl)

instance : Fact (Nat.Prime 2) := ⟨by decide⟩
instance : Fact (Nat.Prime 3) := ⟨by decide⟩
instance : Fact (Nat.Prime 7) := ⟨by decide⟩

theorem tame_multiplicity_42 (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    idealPrimeMultiplicity F (tamePlace p hp) (Ideal.span {(42:𝓞 F)}) = 1 := by
  let P := tamePlace p hp
  let M := idealPrimeMultiplicity F P
  have h0 (k : ℕ) (hk : k ≠ 0) : Ideal.span {(k:𝓞 F)} ≠ 0 := by
    rw [ne_eq,Ideal.zero_eq_bot,Ideal.span_singleton_eq_bot]
    exact Nat.cast_ne_zero.mpr hk
  have hval (q : ℕ) [Fact (Nat.Prime q)] (hq : q=2 ∨ q=3 ∨ q=7) :
      M (Ideal.span {(q:𝓞 F)}) = if p=q then 1 else 0 := by
    split
    · next e => subst q; exact tame_multiplicity_p p hp
    · next e =>
      apply idealPrimeMultiplicity_eq_zero_of_not_dvd F P _ (h0 q (Fact.out : Nat.Prime q).ne_zero)
      rw [Ideal.dvd_span_singleton]
      exact tame_other_not_mem p q hp hq e
  let I2 := Ideal.span {((2:ℕ):𝓞 F)}
  let I3 := Ideal.span {((3:ℕ):𝓞 F)}
  let I7 := Ideal.span {((7:ℕ):𝓞 F)}
  have hs : Ideal.span {(42:𝓞 F)} = I2 * I3 * I7 := by
    dsimp only [I2,I3,I7]
    rw [Ideal.span_singleton_mul_span_singleton,Ideal.span_singleton_mul_span_singleton]
    norm_num
  have hs₂ : M (I2 * I3 * I7) = M I2 + M I3 + M I7 := by
    dsimp only [M]
    rw [idealPrimeMultiplicity_mul F P _ _ (mul_ne_zero (h0 2 (by decide)) (h0 3 (by decide))) (h0 7 (by decide)),
      idealPrimeMultiplicity_mul F P _ _ (h0 2 (by decide)) (h0 3 (by decide))]
  change M _ = 1
  rw [hs,hs₂,show M I2 = _ from hval 2 p2_ok,show M I3 = _ from hval 3 p3_ok,show M I7 = _ from hval 7 p7_ok]
  rcases hp with rfl|rfl|rfl <;> decide

#print axioms coprime_norm_five
#print axioms tame_norm
#print axioms tame_multiplicity_42
end Fifth42
