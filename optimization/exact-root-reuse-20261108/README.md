# Exact fifth-root reuse: bounded test handoff

This branch publishes a reviewable, tested optimization for a compute node to
pick up later. It does not modify the active Ada/Boole search, deploy a release,
or change any existing repository source or deployment snapshot.

## How long does it take?

The complete packaged command with `--benchmark` took **154.038 seconds
(2 minutes 34 seconds)** in an isolated cloud workspace and exited successfully.
That includes native compilation, all 142 tests, 16 baseline/candidate exact
native comparisons, and all 30 bounded timing trials. The original timing-only
suite took 101.260 seconds. Plan roughly **3–5 minutes on an idle node with the
dependencies already installed**, but this is an estimate, not a node-specific
measurement. Environment setup, load, compiler and filesystem differences can
add time. CUDA/NFS acceptance testing is a separate step.

This is a short validation and performance comparison, not a new full search.
There is no once-per-search cache to build. The patch reuses an exact lower
fifth-root bound already computed within each individual patch construction,
only when an exact comparison proves it can do so.

## Pick up and run in a separate directory

Use a new checkout and a **new, nonexistent** scratch output directory. Do not
check out this branch in a running worker's source directory.

```sh
git clone --single-branch --branch handoff/exact-root-reuse-20261108 \
  https://github.com/paulnord/fifth42.git fifth42-root-reuse-handoff
cd fifth42-root-reuse-handoff/optimization/exact-root-reuse-20261108
sha256sum -c ARCHIVE_SHA256SUMS
unzip -q fifth42-exact-root-reuse-20261108.zip
cd fifth42-exact-root-reuse
sh reproduce.sh /absolute/new/scratch /absolute/pinned/python --benchmark
```

Replace the two absolute paths. The Python executable must be from an existing
Python 3.12 environment with sympy 1.14.0, fpylll 0.6.4, cysignals 1.12.5,
numpy 2.3.5 and gmpy2 2.2.2. The host also needs g++, make, patch, sha256sum and
GMP C++ development headers/libraries. No CUDA is needed for this packaged
CPU comparison. The script installs nothing and starts no services. Omit
`--benchmark` to run correctness/build checks without the 30 timing trials.

The script checks all packaged file hashes before building or running code.
It writes results only into the new scratch output directory and refuses an
existing output directory. It requires no connection to live journals, shared
ledgers, services or remote repositories. Do not run the benchmark alongside a
production job on the same resources if you want an uncontended timing result.

## What is published here?

- `fifth42-exact-root-reuse-20261108.zip`: the exact 167-file package previously
  tested, including pinned baseline source, patch, tests, reproduction script,
  independent review and complete raw results.
- `reuse-exact-lower-root.patch`: a readable copy of the two-source-file patch.
- `TECHNICAL-REPORT.md`: a readable copy of the package's explanation, proof,
  test coverage, measurements and integration boundaries.
- `benchmark-summary.json`: all original paired timing samples and limitations.
- `ARCHIVE_SHA256SUMS`: checksum of the unchanged ZIP.

Archive SHA-256:

`9a96836119eb45d89159542aec1891ae5efdf398794ba269cf8223ae59524059`

The exact baseline is commit
`da4e1e312ce1558c9d8cf027c009f8b400f22b83`, directory
`deployment_snapshots/weekend-20261107/ada/worker`. Later status-publication
commits may appear in this branch's ancestry; the test package remains pinned
to that explicit source baseline.

## Findings and integration boundary

Five alternating local CPU pairs showed about 6–7% higher pipeline throughput
in two selected windows and about 1% in an enumeration-heavy window. These are
not measurements on Ada/Boole's CUDA/NFS pipeline. All paired mathematical
identities, counts and hits matched. The fallback branch retains the original
root calculation and can add overhead when reuse is not possible.

This is a handoff, not a deployable release manifest. Any later production
adoption needs refreshed source/binary identities, bounded GPU and NFS/ledger
acceptance tests, and an authorized fresh process/run. Do not hot-patch an
existing process or silently resume an active journal with changed code.
