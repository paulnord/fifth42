import Fifth42Outside
import Fifth42TameTable
open scoped NumberField
open NumberField Ideal IsDedekindDomain ClassFieldTheory
open GlobalClassFieldTheory.Reciprocity
open AlgebraicNumberTheory.PowerResidueSymbols
namespace Fifth42

noncomputable def zI : 𝓞 F := z_primitive.toInteger
theorem zI_prim : IsPrimitiveRoot zI 5 := z_primitive.toInteger_isPrimitiveRoot
theorem zI_cyclo : zI^4+zI^3+zI^2+zI+1=0 := by
  have hp : (zI-1)*(zI^4+zI^3+zI^2+zI+1)=0 := by
    calc
      _ = zI^5-1 := by ring
      _ = 0 := by rw [zI_prim.pow_eq_one, sub_self]
  exact (mul_eq_zero.mp hp).resolve_left (sub_ne_zero.mpr (fun h ↦ by
    have := zI_prim.pow_inj (i:=1) (j:=0) (by decide) (by decide) (by simpa using h)
    omega))

noncomputable def zIroot : rootsOfUnity (n:ℕ) (𝓞 F) :=
    ⟨⟨zI, zI^4, by rw [← pow_succ',zI_prim.pow_eq_one],
                   by rw [← pow_succ,zI_prim.pow_eq_one]⟩, by
         apply Units.ext; exact zI_prim.pow_eq_one⟩

noncomputable def carryRoot : rootsOfUnity (n:ℕ) (𝓞 F) →* rootsOfUnity (n:ℕ) F :=
  (KummerTheory.nthRootsSubgroupEquivRootsOfUnity F (n:ℕ)).toMonoidHom.comp
    (integralRootsOfUnityToNthRoots F (n:ℕ))

noncomputable def zRoot : rootsOfUnity (n:ℕ) F := carryRoot zIroot
theorem zRoot_field : ((zRoot.1 : Fˣ) : F) = z := rfl

theorem tameCharP (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7) :
    CharP (𝓞 F ⧸ (tamePlace p hp).asIdeal) p := by
  let P := (tamePlace p hp).asIdeal
  let : P.IsMaximal := (tamePlace p hp).isPrime.isMaximal (tamePlace p hp).ne_bot
  apply (CharP.charP_iff_prime_eq_zero (Fact.out : Nat.Prime p)).mpr
  rw [← map_natCast (Ideal.Quotient.mk P),Ideal.Quotient.eq_zero_iff_mem]
  let : P.LiesOver (Ideal.span {(p:ℤ)}) := tamePlace_lies_over p hp
  simpa using (Ideal.mem_of_liesOver (p := Ideal.span {(p:ℤ)}) (P := P) (p:ℤ)).mp
    (Ideal.mem_span_singleton_self _)

theorem tameLog_lt (p : ℕ) (hp : p=2 ∨ p=3 ∨ p=7) (a b : Fin p)
    (hn : ¬ (a.val=0 ∧ b.val=0)) : elog p a b < 5 := by
  have h2 : ∀ a b : Fin 2, ¬ (a.val=0 ∧ b.val=0) → elog 2 a b < 5 := by decide
  have h3 : ∀ a b : Fin 3, ¬ (a.val=0 ∧ b.val=0) → elog 3 a b < 5 := by decide
  have h7 : ∀ a b : Fin 7, ¬ (a.val=0 ∧ b.val=0) → elog 7 a b < 5 := by decide
  rcases hp with rfl|rfl|rfl
  · exact h2 _ _ hn
  · exact h3 _ _ hn
  · exact h7 _ _ hn

theorem quotient_tame_eval (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7)
    (u v : ℤ) (hl : elog p (u%p).toNat (v%p).toNat < 5) :
    let P := (tamePlace p hp).asIdeal
    let m := Ideal.Quotient.mk P
    (m ((u:𝓞 F)+zI*(v:𝓞 F)))^((p^4-1)/5) =
      (m zI)^(elog p (u%p).toNat (v%p).toNat) := by
  let : CharP (𝓞 F ⧸ (tamePlace p hp).asIdeal) p := tameCharP p hp
  let m := Ideal.Quotient.mk (tamePlace p hp).asIdeal
  have hcy : (m zI)^4+(m zI)^3+(m zI)^2+m zI+1=0 := by
    simpa using congrArg m zI_cyclo
  have h₁ (a : ℤ) :
      (a:𝓞 F ⧸ (tamePlace p hp).asIdeal) = ((a%(p:ℤ)).toNat:𝓞 F ⧸ (tamePlace p hp).asIdeal) := by
    rw [CharP.intCast_eq_intCast_mod _ p, ← Int.cast_natCast]
    congr 1
    exact (Int.toNat_of_nonneg (Int.emod_nonneg _ (Int.natCast_ne_zero.mpr (Fact.out : Nat.Prime p).ne_zero))).symm
  have he := elog_eval (m zI) p (Fact.out : Nat.Prime p).one_lt hcy
    (u%p).toNat (v%p).toNat hl
  simp only [map_add,map_mul,map_intCast]
  rw [h₁ u,h₁ v]
  exact he

theorem tame_linear_not_mem (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7)
    (u v : ℤ) (hl : elog p (u%p).toNat (v%p).toNat < 5) :
    ((u:𝓞 F)+zI*(v:𝓞 F)) ∉ (tamePlace p hp).asIdeal := by
  intro hm
  let P := (tamePlace p hp).asIdeal
  let : P.IsMaximal := (tamePlace p hp).isPrime.isMaximal (tamePlace p hp).ne_bot
  have H := quotient_tame_eval p hp u v hl
  dsimp only at H
  rw [(Ideal.Quotient.eq_zero_iff_mem).mpr hm, zero_pow (by rcases hp with rfl|rfl|rfl <;> decide)] at H
  have hpow : (Ideal.Quotient.mk P zI)^5=1 := by rw [← map_pow,zI_prim.pow_eq_one,map_one]
  have hn : Ideal.Quotient.mk P zI ≠ 0 := by intro e; rw [e,zero_pow (by decide)] at hpow; exact zero_ne_one hpow
  exact (pow_ne_zero _ hn) H.symm

theorem tame_power_residue (p : ℕ) [Fact (Nat.Prime p)] (hp : p=2 ∨ p=3 ∨ p=7)
    (u v : ℤ) (hl : elog p (u%p).toNat (v%p).toNat < 5) :
    let P := tamePlace p hp
    primeIdealPowerResidueSymbol F P n primitive5_nonempty
      (coprime_norm_five P (tame_place_not_five p hp)) ((u:𝓞 F)+zI*(v:𝓞 F))
      (tame_linear_not_mem p hp u v hl) = zIroot^(elog p (u%p).toNat (v%p).toNat) := by
  dsimp only
  let P := tamePlace p hp
  let : P.asIdeal.IsMaximal := P.isPrime.isMaximal P.ne_bot
  let : Field (𝓞 F ⧸ P.asIdeal) := Ideal.Quotient.field P.asIdeal
  let : Fintype (𝓞 F ⧸ P.asIdeal) := Fintype.ofFinite _
  let c : (Ideal.absNorm P.asIdeal).Coprime (n:ℕ) := coprime_norm_five P (tame_place_not_five p hp)
  change primeIdealPowerResidueSymbol F P n primitive5_nonempty c ((u:𝓞 F)+zI*(v:𝓞 F)) _ = _
  apply (rootsOfUnityReductionEquiv F P n primitive5_nonempty c).injective
  rw [rootsOfUnityReductionEquiv_primeIdealPowerResidueSymbol,map_pow,rootsOfUnityReductionEquiv_apply]
  apply Subtype.ext
  apply Units.ext
  rw [finiteFieldPowerResidueSymbol_apply,card_primeIdealResidueField]
  change (Ideal.Quotient.mk P.asIdeal ((u:𝓞 F)+zI*(v:𝓞 F)))^((Ideal.absNorm P.asIdeal-1)/5) =
    (Ideal.Quotient.mk P.asIdeal zI)^(elog p (u%p).toNat (v%p).toNat)
  rw [tame_norm p hp]
  exact quotient_tame_eval p hp u v hl

#print axioms tame_power_residue
end Fifth42
