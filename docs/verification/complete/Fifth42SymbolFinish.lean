import Fifth42TameFinish
open scoped NumberField
open NumberField Ideal IsDedekindDomain ClassFieldTheory
open GlobalClassFieldTheory.Reciprocity
open AlgebraicNumberTheory.PowerResidueSymbols
namespace Fifth42

private theorem a42_integral : a42 = nonzeroIntegralFieldUnit F (42:𝓞 F) (by norm_num) := by
  apply Units.ext
  change (42:F) = ((42:𝓞 F):F)
  simpa only using (map_ofNat (algebraMap (𝓞 F) F) 42).symm

noncomputable def bLin (u v : ℤ) (hn : (u:𝓞 F)+zI*(v:𝓞 F) ≠ 0) : Fˣ :=
  nonzeroIntegralFieldUnit F _ hn

theorem tame_symbol_linear (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7)
    (u v : ℤ) (hl : elog p (u%p).toNat (v%p).toNat < 5)
    (hn : (u:𝓞 F)+zI*(v:𝓞 F) ≠ 0) :
    finiteSymbol5 (tamePlace p hp) a42 (bLin u v hn) =
       (zRoot^(elog p (u%p).toNat (v%p).toNat))⁻¹ := by
  let P := tamePlace p hp
  have hv : P ≠ prime5_place := tame_place_not_five p hp
  let b : 𝓞 F := (u:𝓞 F)+zI*(v:𝓞 F)
  change finiteSymbol5 P a42 (nonzeroIntegralFieldUnit F b hn) = _
  rw [a42_integral,finiteSymbol5_skew,finiteSymbol5_compare]
  unfold globalFinitePlaceHilbertSymbol
  rw [finitePlaceHilbertSymbol_integral_eq_primeIdealPowerResidueFactor F n (by norm_num)
    primitive5_nonempty P (away_five P hv) (coprime_norm_five P hv)
    b 42 hn (by norm_num) (tame_linear_not_mem p hp u v hl),tame_multiplicity_42 p hp,pow_one]
  rw [show primeIdealPowerResidueSymbol F P n primitive5_nonempty (coprime_norm_five P hv)
       b (tame_linear_not_mem p hp u v hl) = _ from tame_power_residue p hp u v hl]
  apply congrArg Inv.inv
  exact map_pow carryRoot _ _

theorem outside_not_42 (P : HeightOneSpectrum (𝓞 F))
    (h2 : P ≠ tamePlace 2 p2_ok) (h3 : P ≠ tamePlace 3 p3_ok) (h7 : P ≠ tamePlace 7 p7_ok) :
    (42:𝓞 F) ∉ P.asIdeal := by
  intro h
  rw [show (42:𝓞 F) = 2*3*7 by norm_num] at h
  rcases P.isPrime.mem_or_mem h with h23|h7m
  · rcases P.isPrime.mem_or_mem h23 with h2m|h3m
    · exact h2 (tamePlace_of_mem 2 p2_ok P h2m)
    · exact h3 (tamePlace_of_mem 3 p3_ok P h3m)
  · exact h7 (tamePlace_of_mem 7 p7_ok P h7m)

theorem outside_symbol_linear (P : HeightOneSpectrum (𝓞 F))
    (h5 : P ≠ prime5_place) (h42 : (42:𝓞 F) ∉ P.asIdeal)
    (u v w : ℤ) (he : u^5+v^5+w^5=42)
    (hn : (u:𝓞 F)+zI*(v:𝓞 F) ≠ 0) :
    finiteSymbol5 P a42 (bLin u v hn) = 1 := by
  obtain ⟨c,hc⟩ := rotated_factor zI u v w 0 zI_cyclo he
  rw [pow_zero,one_mul] at hc
  rw [a42_integral]
  exact finiteSymbol5_of_factor P h5 42 _ h42 hn (w:𝓞 F) c hc

private theorem zRoot_bLin :
    zRoot.1 = bLin 0 1 (by simp; exact zI_prim.ne_zero (by decide)) := by
  apply Units.ext
  change z = (((0:ℤ):𝓞 F)+zI*((1:ℤ):𝓞 F) : 𝓞 F).1
  simp [zI]

theorem tame_symbol_z (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    finiteSymbol5 (tamePlace p hp) a42 zRoot.1 = (zRoot^(elog p 0 1))⁻¹ := by
  rw [zRoot_bLin]
  have hl : elog p (0%p:ℤ).toNat (1%p:ℤ).toNat < 5 := by
    rcases hp with rfl|rfl|rfl <;> decide
  have h := tame_symbol_linear p hp 0 1 hl (by simp; exact zI_prim.ne_zero (by decide))
  have e : (1%(p:ℤ)).toNat=1 := by rcases hp with rfl|rfl|rfl <;> decide
  simpa only [Int.zero_emod,Int.toNat_zero,e] using h

theorem outside_symbol_z (P : HeightOneSpectrum (𝓞 F))
    (h5 : P ≠ prime5_place) (h42 : (42:𝓞 F) ∉ P.asIdeal) :
    finiteSymbol5 P a42 zRoot.1 = 1 := by
  rw [zRoot_bLin,a42_integral]
  apply finiteSymbol5_of_factor P h5 42 _ h42 _ 0 (42*zI^4)
  simp only [Int.cast_zero,Int.cast_one,mul_one,zero_add,zero_pow (n:=5) (by decide),sub_zero]
  calc
    (42:𝓞 F) = 42*zI^5 := by rw [zI_prim.pow_eq_one,mul_one]
    _ = zI*(42*zI^4) := by ring

#print axioms tame_symbol_linear
#print axioms outside_symbol_linear
#print axioms outside_symbol_z
end Fifth42
