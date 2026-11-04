# Independent proof supporting the complementary-pair search

Let four signed integer bases lie in [-B, B], with their 133rd powers summing to 42. The code's supported scope is 44≤B≤2,103,443.

## 1. Forced residues and exclusion of zero

Exhaustive enumeration modulo 1597 gives power-image residues
{0,1,222,223,285,325,610,987,1272,1312,1374,1375,1596}.
The only four-element multiset from this image with sum 42 modulo 1597 is (1,1,325,1312). This enumeration includes repetition. In particular no base can be 0 or divisible by 1597.

## 2. The ordinary base sum is exactly 42

Put D=2·3·5·7·13·23·67=4,206,930. For every listed prime p, p−1 divides 132, so Fermat's theorem, including the zero residue separately, gives x^133≡x modulo p. Hence the base sum S is 42 modulo D.

A solution must contain both signs: four positive powers are either all 1 (sum 4) or include a power≥2^133>42; four negative powers cannot sum to 42.

For two terms of each sign, -2B<S<2B. For three positives and one negative magnitude d, the lower bound S≥-2B is automatic. If S>2B+42, the smallest positive base a satisfies a≥d+S−2B>d+42, since the other two positive bases total at most 2B. Then a^133−d^133>42, contradicting the power sum 42. For one positive p and three negative magnitudes, the upper bound S≤2B+42 is automatic. If S<-2B, the smallest negative magnitude exceeds p, since the other two negative magnitudes total at most 2B; the power sum is then negative. Thus every solution satisfies
-2B≤S≤2B+42.

At B≤2,103,443 this interval excludes both adjacent values congruent to 42 modulo D: -4,206,888 and 4,206,972. Therefore S=42.

## 3. Only two positive and two negative terms are possible

One positive and three negative magnitudes x, y, z would require the positive base to equal x+y+z+42. Strict superadditivity implies its 133rd power exceeds x^133+y^133+z^133+42, impossible.

For three positives a≤b≤c and one negative magnitude d, define g(x)=x^133−x for positive integers. This is nonnegative and strictly increasing. If d≤c, the difference between the power sum and the base sum equals g(a)+g(b)+g(c)−g(d)>0. Equality could occur only with a=b=1 and c=d, giving base sum 2, not 42. Thus d=c+h with h≥1.

Now a+b=h+42 and b≤h+41. Positivity of the power sum requires
 a^133+b^133 > (c+h)^133−c^133 ≥133h*c^132 ≥133h*b^132.
Since a≤b, the left side is at most 2b^133. Therefore 133h<2b≤2h+82, or 131h<82, impossible for h≥1.

## 4. Canonical ordering and gap parameter

Write positive bases a≤b and negative magnitudes c≤d. If b≥d, the positive pair weakly majorizes the negative pair because a+b=c+d+42. For the increasing convex function g(x)=x^133−x, this gives g(a)+g(b)>g(c)+g(d), contrary to equality of both power and base sums 42. This can also be seen directly: when a≥c, both componentwise differences are nonnegative with one strict. When a<c, the interval [d, b] is longer than [a, c] by 42 and lies to its right, so its integral of g' is strictly larger.

Consequently b<d. The base-sum identity then gives a−c=d−b+42>0. Thus
 c<a≤b<d.
Set h=d−b≥1. Then a=c+h+42 and d=b+h, and the target equation is
 [(c+h+42)^133−c^133] = [(b+h)^133−b^133]+42.

Distinctness requires a<b. The negative magnitudes are automatically distinct. The implemented raw modular-match counter includes a=b before the output filter; therefore a run with zero raw matches also excludes repeated-positive-base solutions.

## 5. Exhaustive gap bound used by the code

The left increment is at most 133(h+42)a^132. By the positive binomial terms and b≥a, the right increment is at least
133h*a^132 + (133·132/2)h²*a^131.
Subtracting, the full power sum is at most
133a^131[42a−66h²].
Its required value 42 is positive, so 66h²<42a≤42B. Every possible h is therefore at most floor(sqrt((42B−1)/66)). The code computes exactly this strict integer bound. At B=2,100,000 it is 1156.

## 6. Residue pairing and the finite computation

Each cross-pair comprises one positive and one negative signed base. The forced full multiset (1,1,325,1312) can split only as
AA|UV, AU|AV, AV|AU, UV|AA,
where A=1, U=325, V=1312. These are exactly the four code types and their complements. The code independently ranges every positive c≤B−h−42 and every positive b≤B−h in the admissible modulo 1597 classes, computes their modular power increments, and joins equal residues modulo the large sieve modulus. Any exact solution must appear among those modular matches. All equal-residue preimages are retained in the Cartesian join.

These proofs establish completeness of the mathematical search region. Code inspection, independent count reconciliation and recorded execution establish computational evidence for that region; they do not constitute formal executable certification or a hardware-error certificate.
