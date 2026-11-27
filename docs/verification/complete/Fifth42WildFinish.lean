import Fifth42WildSymbol
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

open scoped NumberField
open NumberField IsDedekindDomain ClassFieldTheory

namespace Fifth42
set_option maxRecDepth 4096
set_option maxHeartbeats 2200000

/-- The second argument in the finite place symbol is a group homomorphism. -/
noncomputable def finiteSymbol5Right (v : HeightOneSpectrum (𝓞 F)) (a : Fˣ) :
    Fˣ →* rootsOfUnity 5 F := by
  let B := finitePlaceAdicHilbertPairingFamily F n primitive5_nonempty
  let e : rootsOfUnity 5 F ≃* rootsOfUnity 5 (v.adicCompletion F) :=
    rootsOfUnityEquivOfPrimitiveRoots (algebraMap F (v.adicCompletion F)).injective
      primitive5_nonempty
  let m := Units.map (algebraMap F (v.adicCompletion F)).toMonoidHom
  exact e.symm.toMonoidHom.comp ((B v (powerClass _ n (m a))).comp
    ((powerClass _ n).comp m))

theorem finiteSymbol5Right_apply (v : HeightOneSpectrum (𝓞 F)) (a b : Fˣ) :
    finiteSymbol5Right v a b = finiteSymbol5 v a b := rfl

private theorem V5_pi' : piC = zC - 1 := by simp [piC,pi5,zC]

private theorem V5_zC_inj : Function.Injective (algebraMap (𝓞 F) V5) := by
  intro x y eq
  have e := congrArg (fun a : V5 ↦ (a:C5)) eq
  change algebraMap (𝓞 F) C5 x = algebraMap (𝓞 F) C5 y at e
  rw [IsScalarTower.algebraMap_apply (𝓞 F) F C5] at e
  exact RingOfIntegers.coe_injective ((algebraMap F C5).injective e)

private theorem V5_zC_cyclo : zC^4+zC^3+zC^2+zC+1=0 := by
  have hζ : IsPrimitiveRoot zC 5 :=
    z_primitive.toInteger_isPrimitiveRoot.map_of_injective V5_zC_inj
  apply mul_left_cancel₀ (sub_ne_zero.mpr (hζ.ne_one (by decide)))
  rw [mul_zero]
  exact (show (zC-1)*(zC^4+zC^3+zC^2+zC+1)=zC^5-1 by ring).trans
    (sub_eq_zero.mpr hζ.pow_eq_one)

private theorem V5_five : ∃ d : V5, (5 : V5) = piC^2*d := by
  obtain ⟨d,hd⟩ := cyclotomic_five_unit zC V5_zC_cyclo
  refine ⟨(-1+piC*d)*piC^2, ?_⟩
  rw [← V5_pi'] at hd
  linear_combination hd

private theorem first_order {R : Type} [CommRing R] (z : R) (k : ℕ) :
    ∃ q : R, z^k = 1+(k:R)*(z-1)+(z-1)^2*q := by
  induction k with
  | zero => exact ⟨0, by simp⟩
  | succ k ih =>
    obtain ⟨q,hq⟩ := ih
    refine ⟨(k:R)+z*q, ?_⟩
    rw [pow_succ,hq,Nat.cast_succ]
    ring

private theorem wild_rotation (u v : ℤ) (k : ℕ)
    (hd : (5:ℤ) ∣ v+(k:ℤ)*(u+v)) :
    ∃ q : V5, zC^k*((u:V5)+zC*(v:V5)) = ((u+v:ℤ):V5)+piC^2*q := by
  obtain ⟨d,hd⟩ := hd
  obtain ⟨c,hc⟩ := V5_five
  obtain ⟨p,hp⟩ := first_order zC k
  have H : (v:V5)+(k:V5)*((u:V5)+(v:V5)) = (5:V5)*(d:V5) := by
    simpa only [Int.cast_add,Int.cast_mul,Int.cast_natCast,Int.cast_ofNat] using
      congrArg (fun i : ℤ ↦ (i:V5)) hd
  rw [← V5_pi'] at hp
  have hz : zC = 1+piC := by rw [V5_pi']; ring
  refine ⟨(k:V5)*(v:V5)+p*((u:V5)+zC*(v:V5))+piC*c*(d:V5), ?_⟩
  rw [hp,Int.cast_add]
  linear_combination piC*H + piC*(d:V5)*hc +
    ((v:V5)+(k:V5)*piC*(v:V5))*hz

private theorem int_pow5_div (r : ℤ) : (5:ℤ) ∣ r-r^5 := by
  have h : ∀ q : ZMod 5, q^5=q := by decide
  apply (ZMod.intCast_zmod_eq_zero_iff_dvd (r-r^5) 5).mp
  simp [h]

private theorem V5_integer_isUnit (r : ℤ) (hr : r % 5 ≠ 0) :
    IsUnit (r : V5) := by
  let red : V5 →+* ZMod 5 :=
    completion_residue5.toRingHom.comp (IsLocalRing.residue V5)
  have hz : red (r:V5) ≠ 0 := by
    rw [map_intCast]
    exact fun h ↦ hr (Int.emod_eq_zero_of_dvd
      ((ZMod.intCast_zmod_eq_zero_iff_dvd r 5).mp h))
  rw [← IsLocalRing.notMem_maximalIdeal]
  intro hm
  have h0 : IsLocalRing.residue V5 (r:V5) = 0 :=
    (IsLocalRing.residue_eq_zero_iff _).mpr hm
  exact hz (by change completion_residue5 (IsLocalRing.residue V5 (r:V5))=0; rw [h0,map_zero])

/-- A primary argument with prime-to-five rational residue class has
trivial Hilbert symbol with 42 at the wild place. -/
theorem finiteSymbol5_at_five_eq_one_of_primary_integer (b : Fˣ) (r : ℤ) (q : V5)
    (hr : r % 5 ≠ 0)
    (hb : algebraMap F C5 (b:F) = (((r:V5)+piC^2*q : V5):C5)) :
    finiteSymbol5 prime5_place a42 b = 1 := by
  obtain ⟨d,hd⟩ := int_pow5_div r
  obtain ⟨c,hc⟩ := V5_five
  have he : (r:V5) - (r:V5)^5 = (5:V5)*(d:V5) := by
    simpa only [Int.cast_sub,Int.cast_mul,Int.cast_pow,Int.cast_ofNat] using
      congrArg (fun i : ℤ ↦ (i:V5)) hd
  have isU := V5_integer_isUnit r hr
  obtain ⟨s,hs⟩ := isU
  let y : V5 := (q+c*(d:V5))*(↑s⁻¹ : V5)^5
  have hs5 : (r:V5)^5*(↑s⁻¹ : V5)^5=1 := by
    rw [← hs, ← mul_pow, Units.mul_inv, one_pow]
  have hfac : (r:V5)+piC^2*q = (r:V5)^5*(1+piC^2*y) := by
    dsimp only [y]
    linear_combination he + (d:V5)*hc -
      piC^2*(q+c*(d:V5))*hs5
  have hr0 : r ≠ 0 := fun h ↦ hr (by simp [h])
  let R : Fˣ := Units.mk0 (r:F) (by exact_mod_cast hr0)
  let D : Fˣ := b / R^5
  have hD : algebraMap F C5 (D:F) = ((1+piC^2*y : V5):C5) := by
    have e := congrArg (fun a : V5 ↦ (a:C5)) hfac
    change (V5.subtype : V5 →+* C5) ((r:V5)+piC^2*q) =
      (V5.subtype : V5 →+* C5) ((r:V5)^5*(1+piC^2*y)) at e
    simp only [map_mul,map_pow,map_intCast] at e
    have hprod : algebraMap F C5 (b:F) = (r:C5)^5*((1+piC^2*y : V5):C5) := hb.trans e
    simp only [D, Units.val_div_eq_div_val, Units.val_pow_eq_pow_val, R, Units.val_mk0]
    rw [map_div₀,map_pow,map_intCast,hprod,mul_comm]
    exact mul_div_cancel_right₀ _ (pow_ne_zero _ (by exact_mod_cast hr0))
  have hB : b = D * R^5 := (div_mul_cancel _ _).symm
  let m := finiteSymbol5Right prime5_place a42
  change m b = 1
  rw [hB, map_mul, map_pow, finiteSymbol5Right_apply,
    finiteSymbol5_at_five_eq_one_of_deep D y hD]
  have hR : m R ^ 5 = 1 := Subtype.ext (m R).2
  rw [hR,mul_one]

/-- Wild evaluation of the primary rotation of a pair of rational integers. -/
theorem finiteSymbol5_at_five_of_rotated (b : Fˣ) (u v : ℤ) (k : ℕ)
    (hr : (u+v)%5 ≠ 0) (hd : (5:ℤ) ∣ v+(k:ℤ)*(u+v))
    (hb : (b:F) = z^k*((u:F)+z*(v:F))) :
    finiteSymbol5 prime5_place a42 b = 1 := by
  obtain ⟨q,hq⟩ := wild_rotation u v k hd
  apply finiteSymbol5_at_five_eq_one_of_primary_integer b (u+v) q hr
  have ez : (V5.subtype : V5 →+* C5) zC = algebraMap F C5 z := by
    change algebraMap (𝓞 F) C5 z_primitive.toInteger = _
    rw [IsScalarTower.algebraMap_apply (𝓞 F) F C5]
    rfl
  have h := congrArg (fun a : V5 ↦ (a:C5)) hq
  change (V5.subtype : V5 →+* C5) (zC^k*((u:V5)+zC*(v:V5))) = _ at h
  simp only [map_pow,map_add,map_mul,map_intCast] at h
  simpa only [hb,map_pow,map_add,map_mul,map_intCast,ez] using h

#print axioms finiteSymbol5_at_five_eq_one_of_primary_integer
#print axioms finiteSymbol5_at_five_of_rotated

end Fifth42
