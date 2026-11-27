import Init

/-! Cleared denominators for the shifted Kummer norm polynomial. -/
namespace Fifth42
open Lean.Grind
attribute [local instance] Ring.intCast Semiring.natCast
set_option maxHeartbeats 500000

section
variable {R : Type} [CommRing R]

def normPolynomial (t : R) : R :=
  1-40*t+1900*t^2+85600*t^3+716000*t^4+1000*t^5

def digit₂ (c pi s : R) : R :=
  -8*c*s+76*c^2*pi^2*s^2+3424*c^2*s^3+5728*c^3*pi^2*s^4+8*c^3*s^5

def digit₃ (c pi s : R) : R :=
  -8*c*s+76*c^2*pi^3*s^2+3424*c^2*pi^2*s^3+5728*c^3*pi^5*s^4+8*c^3*pi^4*s^5

/-- Integral expression for (N(1+(s/π²)β³)−1)/π². -/
theorem normPolynomial_level₂ (c pi s t : R)
    (h5 : (5:R)=c*pi^4) (ht : s = pi^2*t) :
    normPolynomial t = 1+pi^2*digit₂ c pi s := by
  have a : (40:R) = 8*(c*pi^4) := by rw [← h5]; grind
  have b : (1900:R) = 76*(c*pi^4)^2 := by rw [← h5]; grind
  have d : (85600:R) = 3424*(c*pi^4)^2 := by rw [← h5]; grind
  have e : (716000:R) = 5728*(c*pi^4)^3 := by rw [← h5]; grind
  have f : (1000:R) = 8*(c*pi^4)^3 := by rw [← h5]; grind
  unfold normPolynomial digit₂
  rw [a,b,d,e,f,ht]
  clear a b d e f h5 ht
  grind

/-- Integral expression for (N(1+(s/π)β³)−1)/π³. -/
theorem normPolynomial_level₃ (c pi s t : R)
    (h5 : (5:R)=c*pi^4) (ht : s = pi*t) :
    normPolynomial t = 1+pi^3*digit₃ c pi s := by
  have a : (40:R) = 8*(c*pi^4) := by rw [← h5]; grind
  have b : (1900:R) = 76*(c*pi^4)^2 := by rw [← h5]; grind
  have d : (85600:R) = 3424*(c*pi^4)^2 := by rw [← h5]; grind
  have e : (716000:R) = 5728*(c*pi^4)^3 := by rw [← h5]; grind
  have f : (1000:R) = 8*(c*pi^4)^3 := by rw [← h5]; grind
  unfold normPolynomial digit₃
  rw [a,b,d,e,f,ht]
  clear a b d e f h5 ht
  grind

/-- The ramification coefficient 5/π⁴ can be chosen congruent to -1. -/
theorem cyclotomic_five_unit (z : R) (hz : z^4+z^3+z^2+z+1=0) :
    ∃ d : R, (5:R)=(-1+(z-1)*d)*(z-1)^4 := by
  refine ⟨z^2+z, ?_⟩
  grind

end

theorem level₂_all_digits : ∀ r : Fin 5, ∃ s : Fin 5,
    (3*s.val+4*s.val^3+2*s.val^5)%5=r.val := by decide

theorem level₃_all_digits : ∀ r : Fin 5, ∃ s : Fin 5,
    (3*s.val)%5=r.val := by decide

#print axioms normPolynomial_level₂
#print axioms normPolynomial_level₃
#print axioms cyclotomic_five_unit
#print axioms level₂_all_digits
#print axioms level₃_all_digits

end Fifth42
