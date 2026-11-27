import Std

/-! Kernel-checked finite certificates for the fifth42 reciprocity obstruction.
The class field theory producing the three target exponents is an input to
the final theorem, not an axiom in this file. -/
namespace Fifth42

set_option maxHeartbeats 0
set_option maxRecDepth 100000

structure Quad where
  x0 : Nat
  x1 : Nat
  x2 : Nat
  x3 : Nat
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq

/-- Product of reduced representatives in F_p[X]/(X^4+X^3+X²+X+1).
X^5=1, X^6=X. For reduced inputs, 4*p*p bounds the subtracted coefficient. -/
def mul (p : Nat) (a b : Quad) : Quad :=
  let c0 := a.x0*b.x0
  let c1 := a.x0*b.x1+a.x1*b.x0
  let c2 := a.x0*b.x2+a.x1*b.x1+a.x2*b.x0
  let c3 := a.x0*b.x3+a.x1*b.x2+a.x2*b.x1+a.x3*b.x0
  let c4 := a.x1*b.x3+a.x2*b.x2+a.x3*b.x1
  let c5 := a.x2*b.x3+a.x3*b.x2
  let c6 := a.x3*b.x3
  let offset := 4*p*p-c4
  ⟨(c0+c5+offset)%p,(c1+c6+offset)%p,(c2+offset)%p,(c3+offset)%p⟩

def one : Quad := ⟨1,0,0,0⟩
def zeta : Quad := ⟨0,1,0,0⟩

def powAux (p : Nat) (a : Quad) : Nat → Nat → Quad
  | 0, _ => one
  | fuel+1, n =>
    if n=0 then one else
    let half := powAux p a fuel (n/2)
    let sq := mul p half half
    if n%2=0 then sq else mul p sq a

def fpow (p : Nat) (a : Quad) (n : Nat) : Quad := powAux p a (n+1) n

/-- The fifth root of unity exponent. The sentinel 5 signals a nonroot. -/
def elog (p x y : Nat) : Nat :=
  let w := fpow p ⟨x%p,y%p,0,0⟩ ((p^4-1)/5)
  if w == one then 0 else if w == zeta then 1
  else if w == ⟨0,0,1,0⟩ then 2 else if w == ⟨0,0,0,1⟩ then 3
  else if w == ⟨p-1,p-1,p-1,p-1⟩ then 4 else 5

abbrev Triple := Nat × Nat × Nat

/-- Character order corresponds to A+ζC, B+ζC, A+ζB. -/
def chars (p a b c : Nat) : Triple := (elog p a c, elog p b c, elog p a b)

def valid (p a b c : Nat) : Prop :=
  (a^5+b^5+c^5)%p = 42%p ∧ a+b+c ≠ 0
instance (p a b c : Nat) : Decidable (valid p a b c) := by unfold valid; infer_instance

def p2 : List Triple := [(3,4,3),(4,3,0),(0,0,4)]
def p3 : List Triple := [(1,3,1),(3,1,0),(3,3,3),(0,0,3)]
def p7 : List Triple := [(0,0,0),(2,2,0),(4,1,1),(0,3,2),(1,4,4),(3,0,3)]

theorem table2 : ∀ a b c : Fin 2, valid 2 a b c → (p2.contains (chars 2 a b c)) = true := by decide
theorem table3 : ∀ a b c : Fin 3, valid 3 a b c → (p3.contains (chars 3 a b c)) = true := by decide
theorem table7 : ∀ a b c : Fin 7, valid 7 a b c → (p7.contains (chars 7 a b c)) = true := by decide

def sum3 (u v w : Triple) : Triple :=
  ((u.1+v.1+w.1)%5,(u.2.1+v.2.1+w.2.1)%5,(u.2.2+v.2.2+w.2.2)%5)

theorem combine : ∀ u ∈ p2, ∀ v ∈ p3, ∀ w ∈ p7, sum3 u v w ≠ (0,0,3) := by decide

/-- Any nine residue coordinates satisfying the local equation and primitivity
at each of 2,3,7 fail the required joint tame reciprocity exponent. -/
theorem finite_obstruction (a₂ b₂ c₂ : Fin 2) (a₃ b₃ c₃ : Fin 3) (a₇ b₇ c₇ : Fin 7)
    (h₂ : valid 2 a₂ b₂ c₂) (h₃ : valid 3 a₃ b₃ c₃) (h₇ : valid 7 a₇ b₇ c₇) :
    sum3 (chars 2 a₂ b₂ c₂) (chars 3 a₃ b₃ c₃) (chars 7 a₇ b₇ c₇) ≠ (0,0,3) :=
  combine _ (List.contains_iff_mem.mp (table2 _ _ _ h₂)) _ (List.contains_iff_mem.mp (table3 _ _ _ h₃)) _ (List.contains_iff_mem.mp (table7 _ _ _ h₇))

def hasLabels (a b c : Nat) : Prop :=
  (a,b,c)=(0,3,4) ∨ (a,b,c)=(0,4,3) ∨ (a,b,c)=(3,0,4) ∨
  (a,b,c)=(3,4,0) ∨ (a,b,c)=(4,0,3) ∨ (a,b,c)=(4,3,0)
instance (a b c : Nat) : Decidable (hasLabels a b c) := by unfold hasLabels; infer_instance

theorem fifth_mod25 : ∀ a : Fin 25, (a.val%5)^5%25=a.val^5%25 := by decide

theorem labels25 : ∀ a b c : Fin 5, (a.val^5+b.val^5+c.val^5)%25=42%25 →
    hasLabels a b c := by decide

theorem calibration31 :
    (elog 2 (2-1) 2, elog 3 (3-1) 2, elog 7 (7-1) 2) = ((0,3,3) : Triple) ∧
    2^5-1=31 ∧ (2*16)%31=1 ∧ 42^6%31=16^3%31 ∧ 16^3%31=4 ∧
    (0+3+3+(5-3))%5=3 := by decide

private theorem addCong {a b c d p : Int} (h₁ : a%p=b%p) (h₂ : c%p=d%p) :
    (a+c)%p=(b+d)%p := by
  calc
    _ = (a%p+c%p)%p := Int.add_emod ..
    _ = (b%p+d%p)%p := by rw [h₁,h₂]
    _ = _ := (Int.add_emod ..).symm

private theorem powCong {a b p : Int} (h : a%p=b%p) (k : Nat) :
    (a^k)%p=(b^k)%p := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Int.pow_succ,Int.pow_succ,Int.mul_emod,ih,h,← Int.mul_emod]

def residue (p : Nat) (hp : 0<p) (x : Int) : Fin p :=
  ⟨(x%(p:Int)).toNat, by
    have h := Int.emod_lt_of_pos x (show (0:Int)<p by omega)
    omega⟩

private theorem signed_reduce (x y z : Int) (h : x^5+y^5+z^5=42)
    (p : Nat) (hp : 0<p) :
    ((residue p hp x).val^5+(residue p hp y).val^5+(residue p hp z).val^5)%p=42%p := by
  have castres (w : Int) : ((residue p hp w).val:Int)=w%(p:Int) :=
    Int.toNat_of_nonneg (Int.emod_nonneg _ (by omega))
  apply Int.ofNat_inj.mp
  simp only [Int.natCast_emod, Int.natCast_add, Int.natCast_pow, castres]
  have f (w : Int) : (w%(p:Int))^5%(p:Int) = w^5%(p:Int) := powCong (Int.emod_emod ..) 5
  exact (addCong (addCong (f x) (f y)) (f z)).trans (congrArg (·%(p:Int)) h)

private theorem rawlabels : ∀ x y z : Fin 25, (x.val^5+y.val^5+z.val^5)%25=42%25 →
    hasLabels (x.val%5) (y.val%5) (z.val%5) := by decide

/-- Signed-integer solutions admit exactly the six permutations of base residues
0,3,4 modulo five. -/
theorem signed_labels (x y z : Int) (h : x^5+y^5+z^5=42) :
    hasLabels ((x%5).toNat) ((y%5).toNat) ((z%5).toNat) := by
  have e (w : Int) : (residue 25 (by decide) w).val%5=(w%5).toNat := by
    simp only [residue]
    omega
  simpa only [e] using rawlabels _ _ _ (signed_reduce x y z h 25 (by decide))

private theorem signed_valid (x y z : Int) (h : x^5+y^5+z^5=42)
    (p : Nat) (hp : 0<p) (hsq : ¬ ((p:Int)^2 ∣ 42)) :
    valid p (residue p hp x) (residue p hp y) (residue p hp z) := by
  refine ⟨signed_reduce x y z h p hp, ?_⟩
  intro hz
  have div5 (w : Int) (hw : (residue p hp w).val=0) : (p:Int)^2 ∣ w^5 := by
    have hnon := Int.emod_nonneg w (show (p:Int) ≠ 0 by omega)
    simp only [residue] at hw
    obtain ⟨k,hk⟩ := Int.dvd_of_emod_eq_zero (show w%(p:Int)=0 by omega)
    exact ⟨(p:Int)^3*k^5, by rw [hk,Int.mul_pow, ← Int.mul_assoc, ← Int.pow_add]⟩
  have dx := div5 x (by omega)
  have dy := div5 y (by omega)
  have dz := div5 z (by omega)
  exact hsq (h ▸ Int.dvd_add (Int.dvd_add dx dy) dz)

def tameSum (a b c : Int) : Triple :=
  let atPrime (p : Nat) := chars p (a%(p:Int)).toNat (b%(p:Int)).toNat (c%(p:Int)).toNat
  sum3 (atPrime 2) (atPrime 3) (atPrime 7)

/-- For any signed solution, its actual reductions violate the specified target. -/
theorem signed_tame_obstruction (a b c : Int) (h : a^5+b^5+c^5=42) :
    tameSum a b c ≠ (0,0,3) :=
  finite_obstruction
    (residue 2 (by decide) a) (residue 2 (by decide) b) (residue 2 (by decide) c)
    (residue 3 (by decide) a) (residue 3 (by decide) b) (residue 3 (by decide) c)
    (residue 7 (by decide) a) (residue 7 (by decide) b) (residue 7 (by decide) c)
    (signed_valid a b c h 2 (by decide) (by decide))
    (signed_valid a b c h 3 (by decide) (by decide))
    (signed_valid a b c h 7 (by decide) (by decide))

/-- Statement isolating the exact reciprocity implication supplied in the paper. -/
def ReciprocityLaw : Prop :=
  ∀ a b c : Int, a^5+b^5+c^5=42 → (a%5).toNat=3 → (b%5).toNat=4 →
    (c%5).toNat=0 → tameSum a b c=(0,0,3)

/-- Once the reciprocity implication is supplied, the integer equation is impossible. -/
theorem no_solution_of_reciprocity (law : ReciprocityLaw) (x y z : Int) :
    x^5+y^5+z^5≠42 := by
  intro h
  have impossible (a b c : Int) (e : a^5+b^5+c^5=42) (a3 : (a%5).toNat=3)
      (b4 : (b%5).toNat=4) (c0 : (c%5).toNat=0) : False :=
    signed_tame_obstruction a b c e (law a b c e a3 b4 c0)
  rcases signed_labels x y z h with r|r|r|r|r|r
  all_goals simp only [Prod.mk.injEq] at r
  · exact impossible y z x (by omega) r.2.1 r.2.2 r.1
  · exact impossible z y x (by omega) r.2.2 r.2.1 r.1
  · exact impossible x z y (by omega) r.1 r.2.2 r.2.1
  · exact impossible x y z h r.1 r.2.1 r.2.2
  · exact impossible z x y (by omega) r.2.2 r.1 r.2.1
  · exact impossible y x z (by omega) r.2.1 r.1 r.2.2

def pairSum (u v : Int) : Nat :=
  let atPrime (p : Nat) := elog p (u%(p:Int)).toNat (v%(p:Int)).toNat
  (atPrime 2 + atPrime 3 + atPrime 7)%5

/-- h is the residue v/(u+v), with the denominator required to be a unit mod 5. -/
def isPrimaryExponent (u v : Int) (h : Nat) : Prop :=
  let a := (u%5).toNat
  let b := (v%5).toNat
  (a+b)%5 ≠ 0 ∧ ((a+b)*h)%5=b

theorem zetaExponents :
    (elog 2 0 1, elog 3 0 1, elog 7 0 1) = ((3,1,0) : Triple) := by decide

/-- This pairwise consequence is the mathematical input from the classical
Eisenstein reciprocity argument. The character of ζ is computed in this file. -/
def PairwiseEisenstein : Prop :=
  ∀ (u v w : Int) (h : Nat), u^5+v^5+w^5=42 → isPrimaryExponent u v h →
    pairSum u v=((elog 2 0 1 + elog 3 0 1 + elog 7 0 1)*h)%5

theorem reciprocityLaw_of_pairwiseEisenstein (law : PairwiseEisenstein) : ReciprocityLaw := by
  intro a b c eqn ha hb hc
  have ac := law a c b 0 (by omega) (by simp [isPrimaryExponent,ha,hc])
  have bc := law b c a 0 (by omega) (by simp [isPrimaryExponent,hb,hc])
  have ab := law a b c 2 eqn (by simp [isPrimaryExponent,ha,hb])
  have eac : pairSum a c=0 := ac.trans (by decide)
  have ebc : pairSum b c=0 := bc.trans (by decide)
  have eab : pairSum a b=3 := ab.trans (by decide)
  have joined : (pairSum a c,pairSum b c,pairSum a b)=((0,0,3) : Triple) :=
    Prod.ext eac (Prod.ext ebc eab)
  simpa only [tameSum, sum3, chars, pairSum] using joined

theorem no_solution_of_pairwiseEisenstein (law : PairwiseEisenstein) (x y z : Int) :
    x^5+y^5+z^5≠42 :=
  no_solution_of_reciprocity (reciprocityLaw_of_pairwiseEisenstein law) x y z

#print axioms zetaExponents
#print axioms reciprocityLaw_of_pairwiseEisenstein
#print axioms no_solution_of_pairwiseEisenstein
#print axioms signed_tame_obstruction
#print axioms no_solution_of_reciprocity
#print axioms signed_labels
#print axioms table2
#print axioms table3
#print axioms table7
#print axioms finite_obstruction
#print axioms fifth_mod25
#print axioms labels25
#print axioms calibration31


/-! Cyclotomic factorization and integer congruences used by the actual reciprocity proof. -/
section AlgebraicBridge

open Lean.Grind
attribute [local instance] Ring.intCast Semiring.natCast
variable {R : Type} [CommRing R]

private theorem zeta_fifth (z : R) (hz : z^4+z^3+z^2+z+1=0) : z^5=1 := by
  have q : (z-1)*(z^4+z^3+z^2+z+1)=0 := by rw [hz, Semiring.mul_zero]
  grind

private theorem linear_factor (z a b : R) (hz : z^4+z^3+z^2+z+1=0) :
    (a+z*b)*(a^4-z*a^3*b+z^2*a^2*b^2-z^3*a*b^3+z^4*b^4)=a^5+b^5 := by
  have q : (z-1)*(z^4+z^3+z^2+z+1)*b^5=0 := by
    rw [hz, Semiring.mul_zero, Semiring.zero_mul]
  grind

theorem pair_nonzero (u v w : Int) (he : u^5+v^5+w^5=42)
    (p : Nat) (hp : 0<p) (hdiv : 42%p=0) (hsq : ¬ ((p:Int)^2 ∣ 42))
    (hroot : ∀ r : Fin p, r.val^5%p=0 → r.val=0) :
    ¬ (u%(p:Int)=0 ∧ v%(p:Int)=0) := by
  rintro ⟨hu,hv⟩
  have hval := signed_valid u v w he p hp hsq
  have hu' : (residue p hp u).val=0 := by simp [residue,hu]
  have hv' : (residue p hp v).val=0 := by simp [residue,hv]
  have hw : (residue p hp w).val^5%p=0 := by
    have t := hval.1
    simpa [hu',hv',hdiv] using t
  exact hval.2 (by simp [hu', hv', hroot _ hw])

/-- Exact divisibility of the difference by the primary rotated linear
factor, using the cyclotomic relation alone. -/
theorem rotated_factor (z : R) (u v w : Int) (k : Nat)
    (hz : z^4+z^3+z^2+z+1=0) (he : u^5+v^5+w^5=42) :
    ∃ q : R, (42:R)-(w:R)^5=(z^k*((u:R)+z*(v:R)))*q := by
  let a : R := (u:R)
  let b : R := (v:R)
  let f := a^4-z*a^3*b+z^2*a^2*b^2-z^3*a*b^3+z^4*b^4
  have zi : z^k * (z^4)^k=1 := by
    rw [← CommSemiring.mul_pow, CommSemiring.mul_comm z, ← Semiring.pow_succ, zeta_fifth z hz, Semiring.one_pow]
  have hf : (a+z*b)*f=a^5+b^5 := linear_factor z a b hz
  have hc := congrArg (fun i : Int => (i:R)) he
  simp only [Ring.intCast_add, Ring.intCast_pow] at hc
  have h42 : ((42:Int):R)=(42:R) := by grind
  rw [h42] at hc
  refine ⟨(z^4)^k*f, ?_⟩
  change (42:R)-(w:R)^5=(z^k*(a+z*b))*((z^4)^k*f)
  change a^5+b^5+(w:R)^5=(42:R) at hc
  calc
    _ = a^5+b^5 := by grind
    _ = (a+z*b)*f := hf.symm
    _ = (z^k*(a+z*b))*((z^4)^k*f) := by grind

theorem modulus_primary (u v : Int) (h : Nat)
    (hh : isPrimaryExponent u v h) :
    (u+v)%5 ≠ 0 ∧ (5:Int) ∣ v+((5-h%5:Nat):Int)*(u+v) := by
  simp only [isPrimaryExponent] at hh
  have hu : (0:Int) ≤ u%5 := Int.emod_nonneg _ (by decide)
  have hv : (0:Int) ≤ v%5 := Int.emod_nonneg _ (by decide)
  have hcu : ((u%5).toNat:Int)=u%5 := Int.toNat_of_nonneg hu
  have hcv : ((v%5).toNat:Int)=v%5 := Int.toNat_of_nonneg hv
  have sumc : (u+v)%5=(((u%5).toNat+(v%5).toNat)%5:Nat) := by
    rw [Int.natCast_emod, Int.natCast_add, hcu,hcv]
    exact Int.add_emod ..
  refine ⟨by rw [sumc]; omega, ?_⟩
  have hh' := congrArg (fun n : Nat => (n:Int)) hh.2
  simp only [Int.natCast_emod, Int.natCast_mul, Int.natCast_add, hcu,hcv] at hh'
  have prodc : ((u+v)*(h:Int))%5=v%5 := by
    rw [Int.mul_emod, Int.add_emod u v, ← Int.mul_emod]
    exact hh'
  have hc : ((5-h%5:Nat):Int)=5-(h:Int)%5 := by omega
  have hx : (5:Int) ∣ (u+v)*(h:Int)-v := by omega
  have hy : (5:Int) ∣ ((5-h%5:Nat):Int)+(h:Int) := by omega
  obtain ⟨t, ht⟩ := hx
  obtain ⟨r, hr⟩ := hy
  refine ⟨r*(u+v)-t, ?_⟩
  grind

#print axioms rotated_factor

end AlgebraicBridge
end Fifth42
