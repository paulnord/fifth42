# Fifth42: a Lean proof for 42

Start with the theorem in [`Fifth42Complete.lean`](Fifth42Complete.lean):

    theorem Fifth42.no_three_fifth_powers_sum_42 (x y z : ℤ) :
      x^5 + y^5 + z^5 ≠ 42

It has no assumptions on the integers and no problem-specific axioms. It proves
the integer obstruction for **42**. It does not prove local solubility,
nonexistence for other targets, or rational nonexistence.

## Argument

1. Reduce the integer equation to a contradiction between three pairwise
   residue-symbol sums. The tables for 2, 3 and 7, and the labels modulo 25,
   are evaluated by Lean. See `Fifth42Bridge.lean`.
2. Instantiate the Hilbert product formula in the fifth cyclotomic number
   field. The only relevant finite places lie above 2, 3, 5 and 7.
   See `Fifth42ReciprocityAudit.lean`, `Fifth42CyclotomicPlaces.lean`,
   `Fifth42PrimeData.lean`, and `Fifth42Outside.lean`.
3. Use the explicit Kummer norm construction at the prime above 5 to show that
   a primary rotated linear factor has trivial local symbol. See
   `Fifth42AtFive.lean`, `Fifth42WildSymbol.lean`, and
   `Fifth42WildFinish.lean` and their supporting norm lemmas.
4. Evaluate the tame local factors using the power-residue formula from NYLL
   and the checked finite-field tables. See `Fifth42TameTable.lean`,
   `Fifth42TameFinish.lean` and `Fifth42SymbolFinish.lean`.
5. Combine the local factors by reciprocity, discharge the conditional
   bridge, and apply it to the integer equation in `Fifth42Complete.lean`.

The formal proof uses the Hilbert product formula rather than importing
Eisenstein reciprocity as an unproved assumption.

## Reproduce

Use Lean **4.36.0** and a clone of
[NYLL](https://github.com/n-yamaguchi-0729/NYLL) at commit
`30a178706c4828aa2c8e8d5c494c785be842af82`. That checkout pins Mathlib at
`fc4f59e577feb1a4956671bc04ac18aaaf8cd842`. With Lean managed by Elan, clone and
pin NYLL in a separate working directory:

    git clone https://github.com/n-yamaguchi-0729/NYLL.git
    git -C NYLL checkout 30a178706c4828aa2c8e8d5c494c785be842af82

Then run this from the directory containing this README:

    bash check.sh /absolute/path/to/NYLL

The script builds the required dependencies in NYLL and then compiles these
proof files in order. The first dependency build can take a while.
`verification.txt` records the proof-module build and the axiom audit. The
final theorem uses only Lean's standard `propext`, `Classical.choice`,
and `Quot.sound`.
