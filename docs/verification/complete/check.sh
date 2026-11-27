#!/usr/bin/env bash
set -euo pipefail
NYLL="$(cd "${1:?Usage: bash check.sh /path/to/NYLL}" && pwd)"
bundle="$(cd "$(dirname "$0")" && pwd)"
cd "$NYLL"
if [[ "$(git rev-parse HEAD)" != 30a178706c4828aa2c8e8d5c494c785be842af82 ]]; then
  echo "Expected NYLL commit 30a178706c4828aa2c8e8d5c494c785be842af82" >&2
  exit 1
fi
lake build \
  +Mathlib.Algebra.CharP.Basic \
  +Mathlib.Algebra.Field.ZMod \
  +Mathlib.Data.ZMod.Basic \
  +Mathlib.FieldTheory.KummerExtension \
  +Mathlib.FieldTheory.KummerPolynomial \
  +Mathlib.NumberTheory.NumberField.Cyclotomic.Ideal \
  +Mathlib.RingTheory.Norm.Transitivity \
  +Mathlib.RingTheory.Valuation.LocalSubring \
  +Mathlib.Tactic.FinCases \
  +Mathlib.Tactic.IntervalCases \
  +Mathlib.Tactic.Linarith \
  +Mathlib.Tactic.LinearCombination \
  +Mathlib.Tactic.NormNum \
  +Mathlib.Tactic.Ring \
  +Nyll.ClassFieldTheory.AlgebraicNumberTheory.Completion.LocalField \
  +Nyll.ClassFieldTheory.GlobalClassFieldTheory.Reciprocity.PowerResidueReciprocity \
  +Nyll.ClassFieldTheory.LocalClassFieldTheory.Kummer.GeneralTameFormula \
  +Nyll.ClassFieldTheory.Theorems.HilbertSymbols.HilbertProductFormula \
  +Nyll.ValuedFieldTheory.Valuation.Henselian.NonmonicSimpleRoot \
  +Nyll.ValuedFieldTheory.Valuation.Topology.AdicCompletionInverseLimit
toolchain_path="$(lake env printenv PATH)"
lean_path="$(lake env printenv LEAN_PATH | tr ':' '\n' | sed "s|^\.|$NYLL/.|" | paste -sd:)"
out="$(mktemp -d)"
trap 'rm -rf -- "$out"' EXIT
cd "$bundle"
export PATH="$toolchain_path" LEAN_PATH="$lean_path:$out"
lean --version
for mod in Fifth42Bridge Fifth42ShiftedNorm Fifth42KummerNorm \
  Fifth42NormDigits Fifth42LocalRoot Fifth42Hensel Fifth42UnitNorm \
  Fifth42ReciprocityAudit Fifth42CyclotomicPlaces Fifth42AtFive Fifth42TameTable Fifth42WildSymbol Fifth42WildFinish \
  Fifth42PrimeData Fifth42Outside Fifth42TameFinish Fifth42SymbolFinish Fifth42Complete; do
  printf '\n## %s\n' "$mod"
  output="$(lean -o "$out/$mod.olean" "$mod.lean" 2>&1)" || { printf '%s\n' "$output"; exit 1; }
  printf '%s\n' "$output"
  if grep -q 'sorryAx' <<< "$output"; then exit 1; fi
  if [[ "$mod" == Fifth42Complete ]]; then
    grep -Fxq "'Fifth42.no_three_fifth_powers_sum_42' depends on axioms: [propext, Classical.choice, Quot.sound]" <<< "$output"
  fi
done
