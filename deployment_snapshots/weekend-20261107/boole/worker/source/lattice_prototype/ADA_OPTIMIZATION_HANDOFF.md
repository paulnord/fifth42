# ADA optimization handoff, 2026-11-05

Start here for the newer, opt-in lattice optimizations. The original
`ADA_HANDOFF.md`, `PUBLICATION.md`, `ADAPTATION.md`, and `CURRENT_RESULTS.md` are
preserved historical records; statements there about unpublished code or the
old branch describe their original date, not this publication.

Repository: https://github.com/paulnord/fifth42
Branch: `handoff/fifth-lattice-optimizations-20261105`
Directory: `lattice_prototype/`
Parent: `ddf28f04725b29b2f1d53b5d33c16379b0f66a20`

This handoff publishes the tested package for a later ADA session. It does not
start a job or replace the production search. No ADA execution or timing is
claimed. No BNL resources are to be used.

## Protect the working machine and evidence

1. Inspect ADA's active jobs, process/load state, and current repository status
   before changing anything or running tests. Check the actual production
   checkout and its active locks, not a newly created scratch checkout. If jobs
   are busy, defer tests. Do not stop, resume, restart, or modify existing work.
2. Fetch the named branch and record its full commit ID. Use a new detached
   worktree or separate scratch clone. Do not switch branches in a checkout
   used by running jobs, reset edits, or merge this into main.
3. From `lattice_prototype/`, verify `sha256sum -c PACKAGE_SHA256SUMS`,
   `sha256sum -c SHA256SUMS`, and
   `sha256sum -c compiled_experiment/SHA256SUMS`.
4. Copy the directory to a separate scratch location for execution. All
   original `results/` bytes are retained evidence. Reproduction/benchmark
   scripts overwrite them and create binaries or profiles. Never run those
   scripts in the evidence checkout. Keep new output separate and label its
   machine, date, commit, commands, dependencies, bounds, and exit codes.

## Dependencies

The reference implementation needs Python 3.10+ and the standard library.
For the optional stack, use an isolated Python 3.12 virtual environment to
match the tested runtime, with these version pins:

- `requirements-sympy.txt`: SymPy 1.14.0.
- `requirements-fpylll.txt`: fpylll 0.6.4, cysignals 1.12.5, NumPy 2.3.5.
- `compiled_experiment/requirements.txt`: gmpy2 2.2.2.
- Optional upstream comparator: an existing C++17 `g++` and GMP C++ headers and
  library. It runs CPU code and CPU emulation only.

Use existing suitable dependencies when available. If setup is authorized,
install only in the new scratch virtual environment; do not install packages
system-wide, change drivers, or change a production environment. These files
are version pins, not a full hashed dependency lock. Record `pip freeze` and
the actual fplll version. The tested fpylll wheel reports fplll 5.5.0.

Read `THIRD_PARTY.md` and `COMPILED_RATIONALS.md`: fpylll is GPL-2-or-later,
SymPy is BSD, and the compiled stack has LGPL obligations. No third-party
binary wheels are published here. Review compatibility before distributing a
bundled application.

## First bounded checks, only when ADA is available

Use one CPU process, run checks sequentially, and keep native numerical
libraries to one thread. In a Bash scratch shell:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
timeout -k 5s 60s python3 lattice5.py --bound 100 --mode signed42 \
  --backend reference --max-seconds 30
timeout -k 5s 60s python3 lattice5.py --bound 100 --mode signed42 \
  --backend fpylll --max-seconds 30
```

Use the second command only after the pinned optional dependencies are
available. `timeout` must already be available; otherwise use an equivalent
process-level watchdog supplied by the environment, or stop for review. The
Python guard is cooperative and cannot interrupt a native reduction call.
Treat timeouts, nonzero exits, missing dependencies, skipped optional tests,
or `complete:false` as incomplete validation, not a passing result.

The following small opt-in candidate check covers signed bound 100 plus a
nonempty control, verifies each exact hit set against an independent oracle,
and does not overwrite evidence:

```sh
timeout -k 5s 60s python3 - <<'PY'
import json
import lattice5 as l
import modular_filters as f
rows = []
for mode in ('none', 'prune'):
    r = f.signed42_filtered(100, mode=mode, backend='fpylll', max_seconds=20)
    if not r['complete'] or set(map(tuple, r['signed_hits'])) != l.signed_reference(100, 42):
        raise RuntimeError('signed bound-100 check failed')
    rows.append(r)
r = f.search_targets_positive(34, [12, 384], mode='prune', backend='fpylll', max_seconds=20)
expected = l.direct_positive(1, 34, lambda c: 384, lambda r, c: r in (12, 384))
if not r['complete'] or not expected or set(map(tuple, r['hits'])) != expected:
    raise RuntimeError('nonempty control failed')
rows.append(r)
print(json.dumps(rows, indent=2))
PY
```

This is a correctness smoke check, not a statistically meaningful benchmark.
For test reproduction, run these sequentially in the scratch copy, wrapping
each in a suitable process timeout (300 seconds is a conservative initial cap):

```sh
python3 -m unittest -v test_lattice5 audit_tests test_backends test_modular_filters
python3 -O -m unittest -v test_backends test_modular_filters
python3 compiled_experiment/test_mpq.py
python3 -O compiled_experiment/test_mpq.py
python3 compare_upstream.py
```

Expected with all optional dependencies: 31, 14, 5, and 5 passing tests, then
20 matching upstream CPU/emulation runs. Do not run comparison or benchmark
scripts with `python -O`: several independent-oracle benchmark checks use
assertions. The optimized-mode commands above intentionally exercise tests.

## Timing and next-step limits

The candidate to evaluate is fpylll plus exact modular pruning. Keep the
reference path, exact transform certificate, enumeration and fail-closed
budgets intact. Evaluate GMP mpq separately through `compiled_experiment/`;
it must not change the live/default modules.

For a later bounded timing session, use the same fixed domains and paired
variant runs, record cold setup separately, and report all repeats and medians.
The existing benchmark scripts include bounds 100 and 1000, multiple modes,
large fixture-selected patches, and repeated trials. They are not tiny smoke
tests. Agree the wall-time/resource cap before running the full suite; do not
increase bounds or start a production search based on this handoff. If using
the aggregate script, invoke `bash run_validation.sh`, since the preserved
archive does not set its executable bit. It rewrites the scratch results.

Read `CURRENT_RESULTS.md`, `COVERAGE.md`, `AUDIT.md`, and the optimization
documents before interpreting timings. Cloud timing is not ADA performance.
Separate experiment ratios must not be multiplied into a promised speedup.
Large examples are selected single patches, not full-shell coverage. The
bounded signed-box checks do not extend the previous production search.

Report the fetched commit and hashes, environment, exact commands, pass/fail
and skip counts, bounded timings and differences from archived evidence.
Leave main, production code, and all running jobs unchanged.
