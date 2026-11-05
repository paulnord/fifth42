# Packing-only optimization on ADA — 2026-11-05

**PASS:** the optimized packer preserves the exact geometry, canonical JSON
certificate bytes and SHA-256 values, immutable plans, streamed engine packet
bytes, candidate boxes, coverage counts, and exact hit sets. All 60 timed
pipeline observations passed. Each of four cases contains five alternating
baseline/optimized pairs. The experiment used 16 physical CPU cores and one
RTX 3080 Ti, with a ten-minute total allowance. Suite elapsed time was
**53.489 seconds**; this is distinct from per-search timing.

## Per-search medians

All values are seconds. Every timed variant generated and certified **fresh
geometry**. No prepared-geometry cache or changed patch width contributed to
the measured gain.

| Execution regime | Bound | Baseline GPU pipeline | Optimized GPU pipeline | Time reduction |
|---|---:|---:|---:|---:|
| Persistent engines | 8,000 | 0.397004 | 0.322207 | 18.8% |
| Persistent engines | 32,000 | 1.494903 | 1.231908 | 17.6% |
| Cold one-pass | 8,000 | 0.804445 | 0.737880 | 8.3% |
| Cold one-pass | 32,000 | 1.940277 | 1.686408 | 13.1% |

Persistent-engine measurements retain the existing worker pool and CPU/CUDA
engine processes, while rebuilding the geometry and verifying it for every
variant. They include preparation, certification, packing, engine requests,
and exact output validation. Actual cold one-pass measurements create fresh
workers and a fresh GPU process for each variant and include their startup
and shutdown in measured elapsed time. Cold values are real lifetime
measurements, rather than warm medians plus an estimated startup constant.
Report-file writes are outside both timing definitions.

The persistent-engine CPU pipeline was also paired against the same change;
all CPU and CUDA samples and stage metrics are in [samples.csv](samples.csv).
Medians are recomputed independently in [medians.csv](medians.csv).
Each preparation is charged once to each CPU/GPU pipeline measurement using it;
there were 40 fresh preparations across the timed comparisons.

## Change and validation

Profiling identified repeated recursive `dataclasses.asdict()` conversion
inside parent-process certificate identity checks. Task fields are immutable
integer/tuple data. The new serializer reads those fields directly and uses
the **same** canonical JSON settings and SHA-256 hash. It keeps the full
parent-process identity check and all exact arithmetic, transform, enclosure,
resource, and coverage guards. Packet construction is unchanged.

At bound 32,000, persistent-engine packing medians fell from 0.632695 to
0.360282 seconds. The full pipeline gain was 17.6%, not the hypothetical
1.7x ceiling for eliminating all packing. The diagnostic profiler and isolated
packing timing reused saved geometry solely to locate/measure the packing
cost; those results are clearly labeled and are not full-workflow evidence.

Four targeted tests cover canonical bytes for every task field, complete plan
and packet identity across split batches, tampering/missing patches/exhausted
budgets, and AST equality of the assembly algorithm after namespace
normalization. All 22 local tests passed before and after launcher integration;
the frozen benchmark scratch ran 19 tests (the three unrelated older benchmark
tests are not copied into that scratch workspace). Nonempty oracle controls
at bounds 34 and 100 preceded timing. Post-run review verified every trial
hash, decoded every streamed response with the original checks, checked every
task's full count, compared exact results with the independent oracle, and
recomputed every median. See [post-run-review.json](post-run-review.json).

## Use and reproduce

The installed `scaling.py` launcher now selects optimized packing by default.
`--packing baseline` retains the old path. This selection changes only which
assembly function is called; the exact canonical hash format is unchanged.
The measured optimized module is byte-identical to the installed module.

```bash
python3 ~/fifth-lattice-gpu/scaling.py --wait
python3 ~/fifth-lattice-gpu/scaling.py --packing baseline --wait
python3 ~/fifth-lattice-gpu/packing_benchmark.py --wait
```

The first two commands run the larger scaling matrix. The third reproduces
this isolated 16-worker packing comparison. Execute GPU commands in an
approved GPU-visible environment. The ordinary scaling matrix retains its
20-minute cap; the packing comparison has a ten-minute cap. No wider-patch
or preparation-reuse experiment was started. Production source, binaries,
checkpoints, and the original pinned lattice package were preserved.

## Artifacts

The full local benchmark remains at `${PACKING_RUN_DIR}`.
[local-artifact-manifest.json](local-artifact-manifest.json) records every
original local file's hash and size. This publication retains all timing
samples and original trial hashes, canonical task-count tables, exact oracles,
executed source transcripts, build/test logs, and the post-run review. Repeated
large count tables and binaries remain local. Canonical geometry/packet
identities match the earlier complete scaling plans.

[executed-source](executed-source/) contains exactly the code used for the
measurements. [installed-source](installed-source/) records the subsequent
launcher default and rollback-option integration, checked with the same unit
tests. Source transcripts use ordinary local filenames plus `.txt` and replace
absolute local paths with aliases; substitute actual paths before installing
elsewhere. Original hashes refer to local bytes, while
[SHA256SUMS](SHA256SUMS) verifies the published artifact bytes.
