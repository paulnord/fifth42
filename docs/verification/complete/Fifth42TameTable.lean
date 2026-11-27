import Mathlib.Algebra.CharP.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Fifth42Bridge

namespace Fifth42

def Quad.bounded (p : Nat) (a : Quad) : Prop :=
  a.x0 < p ∧ a.x1 < p ∧ a.x2 < p ∧ a.x3 < p

def Quad.eval {K : Type} [CommRing K] (z : K) (a : Quad) : K :=
  a.x0 + a.x1*z + a.x2*z^2 + a.x3*z^3

theorem mul_bounded {p : Nat} (hp : 0 < p) (a b : Quad) : (mul p a b).bounded p := by
  simp only [mul, Quad.bounded]; exact ⟨Nat.mod_lt _ hp,Nat.mod_lt _ hp,Nat.mod_lt _ hp,Nat.mod_lt _ hp⟩

theorem mul_eval {K : Type} [CommRing K] (z : K) (p : Nat) [CharP K p]
    (hz : z^4+z^3+z^2+z+1=0) (a b : Quad) (ha : a.bounded p) (hb : b.bounded p) :
    (mul p a b).eval z = a.eval z * b.eval z := by
  obtain ⟨a₀,a₁,a₂,a₃⟩ := a
  obtain ⟨b₀,b₁,b₂,b₃⟩ := b
  simp only [Quad.bounded] at ha hb
  have bound (x y : Nat) (hx : x ≤ p) (hy : y ≤ p) : x*y ≤ p*p := Nat.mul_le_mul hx hy
  have hb4 : a₁*b₃+a₂*b₂+a₃*b₁ ≤ 4*p*p := by
    have h₁ := bound a₁ b₃ ha.2.1.le hb.2.2.2.le
    have h₂ := bound a₂ b₂ ha.2.2.1.le hb.2.2.1.le
    have h₃ := bound a₃ b₁ ha.2.2.2.le hb.2.1.le
    nlinarith only [h₁,h₂,h₃, show 0 ≤ p*p by omega]
  have hcast (x : Nat) : ((x%p : Nat) : K) = (x:K) := (CharP.natCast_eq_natCast_mod K p x).symm
  have h4 : z^4 = -(z^3+z^2+z+1) := by linear_combination hz
  have h5 : z^5=1 := by linear_combination (z-1)*hz
  have h6 : z^6=z := by linear_combination z*h5
  have off : ((4*p*p-(a₁*b₃+a₂*b₂+a₃*b₁):Nat):K) =
      -((a₁:K)*b₃+a₂*b₂+a₃*b₁) := by
    rw [Nat.cast_sub hb4]
    simp
  simp only [mul, Quad.eval, hcast, Nat.cast_add, Nat.cast_mul, off]
  linear_combination -((a₁:K)*b₃+a₂*b₂+a₃*b₁)*h4 -
    ((a₂:K)*b₃+a₃*b₂)*h5 - ((a₃:K)*b₃)*h6

private theorem one_bounded {p : Nat} (hp : 1 < p) : one.bounded p :=
  ⟨hp,Nat.zero_lt_of_lt hp,Nat.zero_lt_of_lt hp,Nat.zero_lt_of_lt hp⟩

private theorem powAux_spec {K : Type} [CommRing K] (z : K) (p : Nat) [CharP K p]
    (hp : 1 < p) (hz : z^4+z^3+z^2+z+1=0) (a : Quad) (ha : a.bounded p)
    (fuel n : Nat) (hf : n < fuel) :
    (powAux p a fuel n).bounded p ∧ (powAux p a fuel n).eval z = (a.eval z)^n := by
  induction fuel generalizing n with
  | zero => omega
  | succ fuel ih =>
    by_cases hn : n=0
    · subst n; refine ⟨one_bounded hp,?_⟩
      simp [powAux, Quad.eval, one]
    · have hhalf : n/2 < fuel := by omega
      have hh := ih (n/2) hhalf
      have hhalfBound := hh.1
      let half := powAux p a fuel (n/2)
      let sq := mul p half half
      have hsBound : sq.bounded p := mul_bounded (by omega) _ _
      have hsEval : sq.eval z = (a.eval z)^(n/2*2) := by
        rw [show sq=mul p half half from rfl, mul_eval z p hz _ _ hhalfBound hhalfBound]
        rw [hh.2, ← pow_add]
        congr 1
        omega
      rw [powAux, ite_eq_right hn]
      change (if n%2=0 then sq else mul p sq a).bounded p ∧
        (if n%2=0 then sq else mul p sq a).eval z=(a.eval z)^n
      by_cases hpar : n%2=0
      · rw [ite_eq_left hpar,hsEval, show n/2*2=n by omega]
        exact ⟨hsBound,rfl⟩
      · rw [ite_eq_right hpar, mul_eval z p hz _ _ hsBound ha, hsEval, ← pow_succ,
          show n/2*2+1=n by omega]
        exact ⟨mul_bounded (by omega) _ _,rfl⟩

theorem fpow_eval {K : Type} [CommRing K] (z : K) (p : Nat) [CharP K p]
    (hp : 1 < p) (hz : z^4+z^3+z^2+z+1=0) (a : Quad) (ha : a.bounded p) (n : Nat) :
    (fpow p a n).eval z=(a.eval z)^n :=
  (powAux_spec z p hp hz a ha (n+1) n (Nat.lt_succ_self n)).2

private theorem elog_decode {K : Type} [CommRing K] (z : K) (p : Nat) [CharP K p]
    (hp : 1 < p) (hz : z^4+z^3+z^2+z+1=0) (w : Quad)
    (h : (if w == one then 0 else if w == zeta then 1
        else if w == ⟨0,0,1,0⟩ then 2 else if w == ⟨0,0,0,1⟩ then 3
        else if w == ⟨p-1,p-1,p-1,p-1⟩ then 4 else 5) < 5) :
    w.eval z = z^(if w == one then (0:Nat) else if w == zeta then 1
        else if w == ⟨0,0,1,0⟩ then 2 else if w == ⟨0,0,0,1⟩ then 3
        else if w == ⟨p-1,p-1,p-1,p-1⟩ then 4 else 5) := by
  simp only [beq_iff_eq] at h ⊢
  by_cases e₀ : w=one
  · subst w; simp [Quad.eval,one]
  rw [ite_eq_right e₀] at h ⊢
  by_cases e₁ : w=zeta
  · subst w; simp [Quad.eval,zeta]
  rw [ite_eq_right e₁] at h ⊢
  by_cases e₂ : w=⟨0,0,1,0⟩
  · subst w; simp [Quad.eval]
  rw [ite_eq_right e₂] at h ⊢
  by_cases e₃ : w=⟨0,0,0,1⟩
  · subst w; simp [Quad.eval]
  rw [ite_eq_right e₃] at h ⊢
  by_cases e₄ : w=⟨p-1,p-1,p-1,p-1⟩
  · subst w
    rw [ite_eq_left rfl]
    have hm : (((p-1:Nat)):K) = -1 := by
      rw [Nat.cast_sub (by omega), CharP.cast_eq_zero, Nat.cast_one, zero_sub]
    simp only [Quad.eval,hm]
    linear_combination -hz
  rw [ite_eq_right e₄] at h
  omega

/-- Interpretation of the integer lookup table in any residue field of
characteristic p with the given image of the cyclotomic generator. -/
theorem elog_eval {K : Type} [CommRing K] (z : K) (p : Nat) [CharP K p]
    (hp : 1 < p) (hz : z^4+z^3+z^2+z+1=0) (a b : Nat) (h : elog p a b < 5) :
    ((a:K)+z*(b:K))^((p^4-1)/5) = z^(elog p a b) := by
  let v : Quad := ⟨a%p,b%p,0,0⟩
  have hv : v.bounded p := ⟨Nat.mod_lt _ (by omega),Nat.mod_lt _ (by omega),Nat.zero_lt_of_lt hp,Nat.zero_lt_of_lt hp⟩
  have he : v.eval z = (a:K)+z*(b:K) := by
    simp only [v,Quad.eval,Nat.cast_zero,zero_mul,add_zero, ← CharP.natCast_eq_natCast_mod K p]
    rw [mul_comm (b:K)]
  let n := (p^4-1)/5
  have e := fpow_eval z p hp hz v hv n
  rw [he] at e
  rw [← e]
  exact elog_decode z p hp hz (fpow p v n) h

#print axioms mul_eval
#print axioms fpow_eval
#print axioms elog_eval

end Fifth42
