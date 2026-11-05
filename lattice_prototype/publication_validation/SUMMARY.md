# Fresh publication checks

Date: 2026-11-05 UTC. Executed in an isolated cloud scratch copy, not on ADA.
Existing pinned dependencies were reused. No dependency installation,
production run, GPU execution, or ADA action was performed.

All original archive bytes were verified against the input ZIP before and
after validation. Its SHA-256 is recorded in `PUBLICATION_20261105.md`.
All 95 original root-manifest entries and 12 compiled-manifest entries passed.
Fresh generated evidence was copied here; original `results/` was not changed.

## Commands and results

These commands ran sequentially from the scratch `lattice_prototype/`:

```sh
python3 -m unittest -v test_lattice5 audit_tests test_backends test_modular_filters
python3 -O -m unittest -v test_backends test_modular_filters
python3 compiled_experiment/test_mpq.py
python3 -O compiled_experiment/test_mpq.py
python3 compare_upstream.py
```

- `tests.txt`: 31 tests passed, 53.951 seconds, no skips.
- `tests-optimized.txt`: 14 tests passed, 24.821 seconds, no skips.
- `compiled-tests.txt`: 5 tests passed, 0.060 seconds.
- `compiled-tests-optimized.txt`: 5 tests passed, 0.076 seconds.
- `upstream-comparison.txt` and `.json`: all 20 CPU/emulation runs matched
  independent exact canonical hit sets for four bounded comparison cases.
- All 18 delivered Python sources compiled successfully with Python's
  `compile(..., 'exec')` syntax check without generating bytecode files.

The exact bound-100 commands and modular snippet in
`ADA_OPTIMIZATION_HANDOFF.md` were also run with an outer 60-second timeout.
The snippet was extracted directly from that document rather than retyped.

- `smoke-reference.json`: signed bound 100, complete, exact oracle equality.
- `smoke-fpylll.json`: signed bound 100, complete, exact oracle equality.
- `smoke-modular.json`: fpylll with `none` and `prune` modes at signed bound
  100, complete and exact oracle equality; positive bound-34 prune control
  recovered both `(13,16,17,12)` and `(26,32,34,384)` and matched its oracle.

These smoke timings are single cloud trials, not performance claims. Full
benchmark families and original large-fixture experiments were not rerun for
publication. Their unchanged historical evidence remains in `results/`.
The 20-run comparator used the archived bound-1000 lattice evidence and a
fresh independent signed oracle; the full bound-1000 lattice reproduction was
not rerun in this publication check.

See `environment.json` for actual versions. The core suite here includes
optional backends, so its 31-test pass is not a standard-library-only claim.
Optional dependency skips in another environment must be reported as skips.

Package hygiene checked UTF-8 decoding, NUL/binary content, the repository's
256-KiB per-file threshold, generated/private paths, and its known private-key,
GitHub-token, and AWS-access-key patterns. No prohibited content was found.
This is a focused hygiene screen, not a guarantee to detect all secrets.

Remote publication and CI status are verified separately against the actual
new branch commit. This file records local checks, not a claim that CI ran.
