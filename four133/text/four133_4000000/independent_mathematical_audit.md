# Mathematical audit of the three-to-four-million shell

The C++ enumeration engine is byte-for-byte the previously audited engine. The changed production parameters are B=4,000,000 and previous bound=3,000,000. The following verifies that the same branch structure remains exhaustive at the new bound.

Every integer satisfies x^133≡x modulo D=4,206,930. For a four-term solution with target 42, the ordinary base sum S satisfies -2B≤S≤2B+42 and S≡42 modulo D. At B=4,000,000 this leaves exactly S=-4,206,888, 42, and 4,206,972. The neighboring sums with two multiples of D are -8,413,818 and 8,413,902, outside [-8,000,000,8,000,042].

The earlier conditional S=42 proof remains applicable: every solution has two positive and two negative terms, in canonical magnitude order c<a≤b<d, with h=d-b≥1 and a=c+h+42. Necessarily 66h²<42B, so h≤1595.

For each extra ordinary sum, its magnitude still exceeds B. This excludes two positives/two negatives and one positive/three negatives after normalizing the ordinary sum to be positive. The normalized branches are (S,T)=(4,206,972,+42) and (4,206,888,-42), the latter obtained by reflecting all signs. Each has positive a≤b≤c and negative -d, with d=c+h, h≥1, and a+b=S+h. The complete inclusive pair range is ceil((S+h)/2)≤b≤c≤B-h. The earlier binomial argument gives 135h<2B for T=+42 and 135h≤2B for T=-42. Both are covered by h≤59259. The additional geometry bound 3h≤2B-S remains valid and is weaker at this bound.

All residue restrictions remain target-specific: (1,1,325,1312) for +42 and (285,1272,1596,1596) for -42 modulo 1597. These restrictions exclude zero bases. Negating normalized -42 candidates recovers original +42 candidates.

In every canonical branch, d is the unique largest absolute base. Therefore requiring d>3,000,000 in the right-pair generation and d≤4,000,000 searches exactly the new shell without omitting left pairs needed for a join. Every h through the new bound must be included. The immutable, fully audited ≤3,000,000 result and this disjoint shell together cover the inclusive four-million box.

There are 1595+59259+59259=120113 gap cases per large modulus, or 240226 across two moduli. At 1024 gaps per chunk, this is 2+58+58=118 chunks per modulus, or 236 total. Parallel scheduling changes execution order only; it must not change this set of cases.

The mathematical argument allows repeated bases. Inclusive canonical generation retains a=b in the two-positive case and a=b or b=c in the three-positive case until after raw matching. Thus zero raw modular matches excludes repeated-base solutions as well. A nonzero candidate set would need the exact checker and distinctness flag interpreted separately.

These arguments establish the intended finite search space, not its completed execution. Completion requires independent reconciliation of every production chunk and gap, the exact per-gap pair counts, the frozen source/configuration/binary identities, and the preserved prior result. This is computational evidence rather than formal executable certification or a global impossibility proof.
