# Four distinct signed 133rd powers summing to 42

This reproducible bounded search applies the new base-sum filter **before pair generation**. It searches every four-distinct-integer solution in the inclusive box `[-2,100,000, 2,100,000]^4`, with arbitrary signs. No solution was found. This is a finite negative result, not a global impossibility proof.

The proof reductions and independent audit are recorded in companion files. The large prime is used only as a necessary congruence. An exact solution could not evade it. Any surviving candidates are checked with arbitrary-precision integers by `check133_complementary.py`; both full runs produced zero modular candidates.

## Completed computation

Both production runs completed all 1,156 gap checkpoints, each generating 118,098,508 left pairs and 117,636,843 right pairs. Both found zero modular coincidences. The final-source runs took 18.6531 and 19.9598 seconds, with peak resident memory about 24 MiB. Timing includes modular-power initialization, pair generation, sorting, joining, and checkpoint output.

Independent audits checked every per-gap pair count, the unique modulo-1597 residue multiset, all complementary pair types, the mathematical search bounds, and actual compiled collision-rich searches. See `independent_proof.md`, `audit_independent_counts.py/json`, and `audit_complementary_independent.py/json`.

## Algorithm

The base sum is 42 modulo D = 4,206,930 because each prime p in {2,3,5,7,13,23,67} has p-1 dividing 132. Sign and magnitude inequalities force the base sum to equal 42 for the supported bounds, not just for the naive 4B<D range. The program deliberately rejects B>2,103,443; beyond that range, additional sums 42+kD must be included unless further rigorously excluded.

For exact sum 42 only two positive and two negative bases are possible. Write the positives `a<b` and negative magnitudes `c<d`. Every solution must have `c<a<b<d`. Put h=d-b>0. Then a=c+h+42. A convexity estimate forces `66 h^2 < 42 B`, so B=2,100,000 requires only h=1,...,1,156.

Modulo 1597 the only possible unordered multiset of four 133rd-power residues summing to 42 is {1,1,325,1312}. Call these labels A,A,U,V. For each h, generate positive-sum pairs `(a,-c)` and complementary negative-sum pairs `(b,-d)`. Only pair types AA,AU,AV,UV can occur, with complements UV,AV,AU,AA. Residue classes of c and b modulo1597 are precomputed, allowing direct arithmetic-progression generation rather than scanning every integer.

The left key is `a^133-c^133 (mod m)`; the right key is `42+d^133-b^133 (mod m)`. Sort and merge each complementary type. Full Cartesian multiplicity is retained for equal keys. Retain a<b, which ensures the two positive bases are distinct; the other order and distinctness conditions follow from the parameterization.

Each completed h emits its pair counts, candidates, elapsed time, and peak resident memory. Optional start/end h arguments support bounded chunks or restarting after the last completed checkpoint. A partial run is labelled PARTIAL_DONE and is not a coverage certificate.

## Reproduce

```
g++ -O3 -std=c++17 -Wall -Wextra -Wconversion search133_complementary.cpp -o search133_complementary
./search133_complementary --self-test
./search133_complementary 2100000 > run_2100000.log
python check133_complementary.py run_2100000.log --output report_2100000.json

g++ -O3 -std=c++17 -DSEARCH_MODULUS=2305843009213693951ULL search133_complementary.cpp -o search133_complementary_mod2
./search133_complementary_mod2 --self-test
./search133_complementary_mod2 2100000 > run_2100000_mod2.log
python check133_complementary.py run_2100000_mod2.log --output report_2100000_mod2.json

python test_join.py

g++ -O3 -std=c++17 -DSEARCH_MODULUS=43ULL search133_complementary.cpp -o audit_search133_mod43
./audit_search133_mod43 400 > audit_search133_mod43.log
python audit_complementary_independent.py
python audit_independent_counts.py run_2100000.log
python audit_independent_counts.py run_2100000_mod2.log
```

The direct Python join test uses modulus97 at B=1000 to force real modular collisions, and compares the entire candidate multiset against the C++ output. It finds 128 modular coincidences, of which61 have a<b. This tests matching and multiplicity rather than relying only on zero-hit production runs.

No ada, Valpo, or BNL resource was used. Computation ran in the current assistant cloud workspace.
