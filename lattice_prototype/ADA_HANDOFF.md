# Handoff for Codex on ADA

## Task

Review and reproduce the fifth-power tangent-patch/lattice prototype in this directory for `x^5+y^5+z^5=42`. It is a correctness prototype inspired by Elkies, not a replacement for the existing exact CPU/GPU search and not evidence of a speedup. Do not use BNL resources.

## Protect ongoing work

1. Inspect the current repository status and active ADA jobs before any changes or tests. Do not stop, modify, compete materially with, or restart the active four133 job or any existing production search.
2. Fetch `origin/handoff/fifth-lattice-prototype`. Use a new detached worktree or a new scratch checkout, not a branch switch in a working tree used by a running job. Do not reset or overwrite local edits.
3. Read `README.md`, `COVERAGE.md`, `AUDIT.md`, `RESULTS.md`, `PUBLICATION.md`, and `vendor/SOURCES.json`.
4. Verify `SHA256SUMS` before running anything. Preserve the published `results/` bytes as evidence. To reproduce, copy this directory to a separate scratch directory first, because the scripts regenerate result files and local comparator binaries.

The publication itself does not authorize a new production run, large search, GPU workload, optimization campaign or system-wide installation. If an active job makes even modest single-CPU tests unsuitable, defer them and report that fact rather than interrupting the job. Ask Paul before additional work beyond review and bounded reproduction, and before any expensive run.

## Bounded reproduction in the scratch copy

Requirements: Python 3.10+ standard library. The optional upstream comparison needs an already-installed C++17-capable `g++` plus GMP C++ headers/library. Do not install packages system-wide to make this work.

```sh
sha256sum -c SHA256SUMS
python3 -m unittest -v test_lattice5 audit_tests
python3 reproduce.py --bound 1000
python3 compare_upstream.py
```

The last command compiles the exact frozen `vendor/` sources. Its GPU-row comparisons are CPU emulation, not GPU execution. `run_validation.sh` bundles these checks but regenerates `results/`, so run it only in the scratch copy. The recorded cloud run took roughly two minutes of single-process work; this is not an ADA timing promise.

Expected checks:

- 17 tests pass.
- All 10 published Healy-threshold near misses through c=1,000 are recovered and agree with the independent exhaustive reference.
- No target42 solution occurs in the full signed +/-1,000 box, matching the upstream exact search. This does not extend the prior 70-million result.
- 20 upstream CPU/emulation runs agree, including nonempty target12 and target2951 controls.
- The two selected large-fixture patches recover their known points. Do not call these full-shell coverage or blind discovery.
- Exhausted guards fail closed and never emit complete coverage.

## Report back

State the exact fetched branch commit, source hashes, commands, environment, pass/fail status, elapsed times and any differences from the published raw evidence. Distinguish complete finite-domain checks from selected patches and CPU emulation from GPU execution. Identify the smallest useful next implementation/benchmark step, but do not begin a large search or claim a proven speedup. Leave production code and active jobs unchanged.
