# Independent mathematical audit of the three-million search

Let F be the sum of the four signed 133rd powers, S the sum of their bases, and B=3,000,000.

## Ordinary-sum branches

For D=4,206,930=2·3·5·7·13·23·67, every integer satisfies x^133≡x modulo D. Hence F=42 implies S≡42 modulo D.

The signed-power residue multiset modulo 1597 is uniquely (1,1,325,1312), including when repeated bases are allowed. Zero bases are therefore impossible. Both signs must occur. The previously established general bound -2B≤S≤2B+42 does not depend on the earlier numerical limit on B: three positives with S>2B+42 would have their smallest positive base exceed the negative magnitude by more than 42; one positive with S<-2B would have its smallest negative magnitude exceed the positive base. Two terms of each sign already give |S|<2B.

At B=3,000,000 the only remaining ordinary sums are
-4,206,888; 42; 4,206,972.

## The S=42 branch

The earlier conditional proof for S=42 remains valid. It excludes one-positive/three-negative and three-positive/one-negative patterns and gives the canonical shape
c<a≤b<d,
with signed bases (a,b,-c,-d), h=d-b≥1, and a=c+h+42. The necessary inequality is
66h²<42a≤42B.
Thus h≤1381 at B=3,000,000. Distinctness is a<b; keeping a=b until after the raw join also covers repeated-base possibilities.

The old upper bound 2,103,443 was needed only to force S=42 as the sole ordinary-sum branch. It was not needed in this conditional shape or gap argument.

## The two extra ordinary sums

Reflect the negative ordinary-sum branch by negating all four bases. The two normalized searches become
(S,T)=(4,206,972,+42) and (4,206,888,-42),
where T is the normalized target power sum.

Both S values exceed B. Two positives and two negatives are impossible: writing positives a≤b and negative magnitudes c,d, S>B and b≤B imply a>c+d. Strict superadditivity then makes the power sum exceed 42. A single positive with three negatives is likewise impossible because that positive exceeds the sum of the negative magnitudes by S. All-positive and all-negative patterns cannot give either tiny target in these large-sum branches. Thus each normalized search has three positives and one negative.

Write positive bases a≤b≤c and negative magnitude d. Necessarily d>c. If d≤c, the power sum is positive; for target +42 it is either the small degenerate value 2 when a=b=1 and c=d, or at least a positive jump of order 2^133, never 42. The large ordinary sum also excludes that degenerate case.

Set d=c+h, h≥1. The ordinary-sum relation gives a+b=S+h. Consequently
ceil((S+h)/2)≤b≤c≤B-h,
and a=S+h-b is positive because S>B. Distinctness requires a<b<c; inclusive generation followed by this test preserves repeated-base cases as well.

Since (c+h)^133-c^133=a^133+b^133-T and a,b≤c,
133h*c^132≤2c^133-T.
For T=+42 this gives 133h<2c and hence 135h<2B. For T=-42, c≥2 implies 42/c^132<1; integrality gives 133h≤2c and hence 135h≤2B. Both permit h≤44444 at B=3,000,000. The additional necessary bound 3h≤2B-S is safe, though weaker here.

The signed-power multiset for T=-42 is the negation of the +42 multiset: (285,1272,1596,1596) modulo 1597. The negative term contributes -d^133, not +d^133. After the normalized negative-target branch is checked, negating its tuple returns a tuple for the original target +42.

## Incremental union

In every canonical branch, d is strictly larger than every other absolute base. Therefore the shell 2,100,000<max|base|≤3,000,000 can be enumerated by requiring d>2,100,000 only in the right-pair list. The complete left-pair list must remain available to join it. Every h up to the new bound must be searched, including old h values.

The prior independently audited search covers max|base|≤2,100,000. Its union with the new shell covers the full inclusive three-million box. These two regions are disjoint at the boundary because the new shell uses a strict lower inequality. Neither the mathematical shape nor this union argument requires a solution to have distinct bases; the raw zero-match claim would exclude repetitions too.

## Computational audit scope

Independent small-modulus tests compare direct enumeration with the compiled C++ for all three branches, including collision multiplicities, reflected output, repeated positive bases, shell boundaries, and split h intervals. Those tests support the implementation but do not replace complete production logs and final checkpoint/count reconciliation. A full negative claim requires every branch and gap under both configured sieve moduli, or an explicitly narrower separately justified claim. No formal proof-checker installation or formal executable certification is involved.
