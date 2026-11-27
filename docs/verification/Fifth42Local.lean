import Fifth42Bridge

/-!
The elementary portion of the Hilbert-symbol route. This file proves the
polynomial identities behind the finite-depth unit argument, and isolates
the local/global facts still needed. It is not an unconditional proof.
-/
namespace Fifth42
open Lean.Grind
attribute [local instance] Ring.intCast Semiring.natCast

section Polynomial
variable {R : Type} [CommRing R]

/-- The product over the five conjugates of a linear polynomial in the
Kummer radical. The interpretation as a field/algebra norm is separate. -/
theorem kummer_product (z X : R) (hz : z^4+z^3+z^2+z+1=0) :
    (1+X)*(1+z*X)*(1+z^2*X)*(1+z^3*X)*(1+z^4*X)=1+X^5 := by
  have hh : z^5=1 := by
    have h := congrArg (fun a => (z-1)*a) hz
    rw [Semiring.mul_zero] at h
    grind
  have a₁ : z+z^2+z^3+z^4 = -1 := by grind
  have a₂ : z+z^2+2*z^3+2*z^4+2*z^5+z^6+z^7 = 0 := by
    have h₆ : z^6=z := by grind
    have h₇ : z^7=z^2 := by grind
    grind
  have a₃ : z^3+z^4+2*z^5+2*z^6+2*z^7+z^8+z^9 = 0 := by
    have h₆ : z^6=z := by grind
    have h₇ : z^7=z^2 := by grind
    have h₈ : z^8=z^3 := by grind
    have h₉ : z^9=z^4 := by grind
    grind
  have a₄ : z^6+z^7+z^8+z^9+z^10=0 := by
    have h₆ : z^6=z := by grind
    have h₇ : z^7=z^2 := by grind
    have h₈ : z^8=z^3 := by grind
    have h₉ : z^9=z^4 := by grind
    have h₁₀ : z^10=1 := by grind
    grind
  have a₅ : z^10=1 := by grind
  grind

/-- Explicit norm candidate producing the fifth principal-unit digit. -/
theorem norm_candidate (z alpha pi s : R)
    (hz : z^4+z^3+z^2+z+1=0) (ha : alpha^5=42) :
    let X := s*pi*alpha
    (1+X)*(1+z*X)*(1+z^2*X)*(1+z^3*X)*(1+z^4*X)=1+42*s^5*pi^5 := by
  dsimp
  rw [kummer_product _ _ hz]
  grind

/-- With 5 = c*pi^4, the fifth power of a principal unit on level j+2
produces the coefficient c*s on level j+6, up to the next level. -/
theorem fifth_power_digit (pi c s : R) (j : Nat) (h5 : (5:R)=c*pi^4) :
    ∃ q : R, (1+s*pi^(j+2))^5 = 1+c*s*pi^(j+6)+pi^(j+7)*q := by
  refine ⟨2*c*s^2*pi^(j+1)+2*c*s^3*pi^(2*j+3)+c*s^4*pi^(3*j+5)+
    s^5*pi^(4*j+3), ?_⟩
  have ex (a b : Nat) : pi^(a+b)=pi^a*pi^b := Semiring.pow_add ..
  let a := pi^(j+2)
  let b := pi^5
  let d := pi^4
  have l : pi^(j+6)=a*d := ex (j+2) 4
  have f : pi^(j+7)=a*b := ex (j+2) 5
  have s₂ : a*a=pi^((j+2)+(j+2)) := (ex _ _).symm
  have s₃ : a*a*a=pi^((j+2)+(j+2)+(j+2)) := by
    rw [s₂]
    exact (ex _ _).symm
  have s₄ : a*a*a*a=pi^((j+2)+(j+2)+(j+2)+(j+2)) := by
    rw [s₃]
    exact (ex _ _).symm
  have h₁ : b*pi^(j+1)=a*d := by
    change pi^5*pi^(j+1)=pi^(j+2)*pi^4
    rw [← ex 5 (j+1), ← ex (j+2) 4]
    congr 1
    omega
  have h₂ : b*pi^(2*j+3)=a*a*d := by
    rw [s₂]
    change pi^5*pi^(2*j+3)=pi^((j+2)+(j+2))*pi^4
    rw [← ex 5 (2*j+3), ← ex ((j+2)+(j+2)) 4]
    congr 1
    omega
  have h₃ : b*pi^(3*j+5)=a*a*a*d := by
    rw [s₃]
    change pi^5*pi^(3*j+5)=pi^((j+2)+(j+2)+(j+2))*pi^4
    rw [← ex 5 (3*j+5), ← ex ((j+2)+(j+2)+(j+2)) 4]
    congr 1
    omega
  have h₄ : b*pi^(4*j+3)=a*a*a*a := by
    rw [s₄]
    change pi^5*pi^(4*j+3)=pi^((j+2)+(j+2)+(j+2)+(j+2))
    rw [← ex 5 (4*j+3)]
    congr 1
    omega
  have algebra (a b c d s w x y z : R) (hc : (5:R)=c*d)
      (hw : b*w=a*d) (hx : b*x=a*a*d) (hy : b*y=a*a*a*d)
      (hz : b*z=a*a*a*a) :
      (1+s*a)^5=1+c*s*(a*d)+(a*b)*(2*c*s^2*w+2*c*s^3*x+c*s^4*y+s^5*z) := by
    calc
      _ = 1+c*d*(s*a)+2*c*d*(s*a)^2+2*c*d*(s*a)^3+c*d*(s*a)^4+(s*a)^5 := by
        have t (C T : R) (hC : (5:R)=C) :
            (1+T)^5=1+C*T+2*C*T^2+2*C*T^3+C*T^4+T^5 := by
          rw [← hC]
          grind
        have e := t (c*d) (s*a) hc
        grind
      _ = 1+c*s*(a*d)+2*c*s^2*(a*(b*w))+2*c*s^3*(a*(b*x))+
          c*s^4*(a*(b*y))+s^5*(a*(b*z)) := by
        rw [hw,hx,hy,hz]
        grind
      _ = _ := by grind
  rw [l,f]
  exact algebra a b c d s _ _ _ _ h5 h₁ h₂ h₃ h₄

end Polynomial

/-- If a nonzero member of a principal-unit layer transforms by 2^k
but the character transforms by 2, its value must vanish for k=2,3,4. -/
theorem non_weight_one (k e : Nat) (hk : 2 ≤ k ∧ k ≤ 4)
    (he : e < 5) (h : (2^k*e)%5=(2*e)%5) : e=0 := by
  have finite : ∀ k e : Fin 5, (2 ≤ k.val ∧ k.val ≤ 4) →
    (2^k.val*e.val)%5=(2*e.val)%5 → e.val=0 := by decide
  exact finite ⟨k,by omega⟩ ⟨e,he⟩ hk h

/-- The abstract part of descending through the local unit filtration.
`Deep j u` means that `u = 1 mod πʲ`. The `sigma` input is the action
`ζ ↦ ζ²`. Each `witness` is a fifth power (degrees 6 through 8)
or the explicit Kummer norm (degree 5). -/
theorem principal_units_killed
    {U : Type} [Mul U] [Pow U Nat]
    (Deep : Nat → U → Prop) (chi : U → Nat) (sigma : U → U)
    (chi_lt : ∀ x, chi x < 5)
    (chi_mul : ∀ x y, chi (x*y)=(chi x+chi y)%5)
    (chi_pow : ∀ x (n : Nat), chi (x^n)=(n*chi x)%5)
    (chi_sigma : ∀ x, chi (sigma x)=(2*chi x)%5)
    (cutoff : ∀ x, Deep 9 x → chi x=0)
    (witness : ∀ j, 5 ≤ j → j ≤ 8 → ∀ x, Deep j x →
      ∃ y r, chi y=0 ∧ Deep (j+1) r ∧ x=y*r)
    (layer_sigma : ∀ j, 2 ≤ j → j ≤ 4 → ∀ x, Deep j x →
      ∃ r, Deep (j+1) r ∧ sigma x=x^(2^j : Nat)*r) :
    ∀ x, Deep 2 x → chi x=0 := by
  have high (j : Nat) (low : 5 ≤ j) (top : j ≤ 8)
      (kill : ∀ x, Deep (j+1) x → chi x=0) : ∀ x, Deep j x → chi x=0 := by
    intro x hx
    obtain ⟨y,r,hy,hr,hxyr⟩ := witness j low top x hx
    rw [hxyr,chi_mul,hy,kill r hr]
  have low (j : Nat) (bot : 2 ≤ j) (top : j ≤ 4)
      (kill : ∀ x, Deep (j+1) x → chi x=0) : ∀ x, Deep j x → chi x=0 := by
    intro x hx
    obtain ⟨r,hr,hσ⟩ := layer_sigma j bot top x hx
    have e := chi_sigma x
    rw [hσ,chi_mul,chi_pow,kill r hr,Nat.add_zero,Nat.mod_mod] at e
    exact non_weight_one j (chi x) ⟨bot,top⟩ (chi_lt x) e
  have h8 := high 8 (by decide) (by decide) cutoff
  have h7 := high 7 (by decide) (by decide) h8
  have h6 := high 6 (by decide) (by decide) h7
  have h5 := high 5 (by decide) (by decide) h6
  have h4 := low 4 (by decide) (by decide) h5
  have h3 := low 3 (by decide) (by decide) h4
  exact low 2 (by decide) (by decide) h3

/-- Global product formula specialized at ζ: its wild exponent cancels
the three inverse tame residue exponents. This needs no prime-31 calibration. -/
theorem wild_zeta_value (e : Nat) (he : e<5)
    (h : (e+(5-elog 2 0 1)+(5-elog 3 0 1)+(5-elog 7 0 1))%5=0) :
    e=4 := by
  rw [show elog 2 0 1=3 by decide,show elog 3 0 1=1 by decide,
      show elog 7 0 1=0 by decide] at h
  omega

/-- End-to-end reduction, provided the indicated concrete Hilbert-symbol
evaluations have been connected to the imported library. No requirement to
prove the unrestricted general reciprocity swap in the original bridge. -/
theorem no_solution_of_local_components
    (wild : Int → Int → Nat)
    (hWild : ∀ u v h, isPrimaryExponent u v h → wild u v=(4*h)%5)
    (hProduct : ∀ u v w : Int, u^5+v^5+w^5=42 →
      ∀ h : Nat, isPrimaryExponent u v h → (wild u v+5-pairSum u v)%5=0)
    (a b c : Int) : a^5+b^5+c^5≠42 := by
  apply no_solution_of_pairwiseEisenstein
  intro u v w h he hh
  have p := hProduct u v w he h hh
  rw [hWild u v h hh] at p
  rw [show elog 2 0 1=3 by decide,show elog 3 0 1=1 by decide,
      show elog 7 0 1=0 by decide]
  have hs : pairSum u v < 5 := Nat.mod_lt _ (by decide)
  omega

#print axioms kummer_product
#print axioms norm_candidate
#print axioms fifth_power_digit
#print axioms non_weight_one
#print axioms principal_units_killed
#print axioms wild_zeta_value
#print axioms no_solution_of_local_components

end Fifth42
