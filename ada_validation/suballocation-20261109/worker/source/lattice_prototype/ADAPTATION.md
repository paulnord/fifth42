# Bounded published-library adaptation, 2026-11-04

Based on `paulnord/fifth42`, branch `handoff/fifth-lattice-prototype`,
`lattice_prototype/lattice5.py` Git blob `1d3ab55b8696c78e1c404254d7ee04fd32dc60db`.
Fetched via GitHub connector and verified equal to the local source snapshot.
The other original handoff files and historical results are retained as context.
`PUBLICATION.md` describes that original handoff, not publication of this adaptation.
This adaptation has not been pushed, deployed or run on ADA.

## Scope

Optional published SymPy and fpylll/fplll LLL backends, retaining exact covering
and exhaustive sphere enumeration. Optional modular filtering is a separate
experimental module, not a change to the default search. See THIRD_PARTY.md and
MODULAR_FILTERS.md. No GPU execution or complete large-shell search is claimed.

## New evidence

- results/sympy-baseline-tests.txt: original 17 tests, passed.
- results/backend-tests.txt: five added backend tests, passed.
- results/backend-tests-optimized.txt: same five under python -O, passed.
- results/published-upstream-validation.txt: original frozen GMP CPU and CPU
  emulation comparator rerun; checks the retained original bounded results.
- results/backend-benchmark.json: new paired backend runs, independent exact
  oracle equality, selected large fixture patches, reduction-only measurements.
- Modular benchmark/tests are separate and explicitly identify their patch scope.

Benchmark reports measure this cloud environment only. Three warm trials are
used for each backend/domain; import/setup is excluded. These are exploratory
wall-clock samples, not a controlled dedicated-host performance study, and some
validation work may run concurrently. Do not extrapolate them to ADA, GPUs or
large denominators. Exact result equality is independently checked in every run.

## Final added checks and consolidated report

CURRENT_RESULTS.md consolidates the completed benchmark evidence. The final
core suite is results/adaptation-final-tests.txt (31 tests); optional optimized
mode is results/adaptation-final-tests-optimized.txt (14 tests). The isolated
compiled-rational experiment adds five tests in normal and optimized mode,
results/compiled-final-tests*.txt. Its large-fixture checks pass without making
any claim of full large-shell coverage. All three backend comparison batches
completed; earlier interrupted process logs are superseded by these final files.

The downloadable text-only snapshot excludes regenerated comparator binaries,
Python caches and binary profiler files. Source, license notices, raw JSON and
text profile reports are retained. SHA256SUMS covers every delivered file except
itself. No external publication was performed.
