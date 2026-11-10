# Other production-speed experiments (TEST_ONLY)

This branch packages **four separate investigations**, not a production update.
The CGBN/cuPQC root-preparation package is on its own branch. No search controller,
service, deadline, ledger, reservation or production journal is changed here.
Results never count as additional production coverage.

## Included

1. **Grouping 4/8/16:** matched finite whole-pipeline replay of three regions,
   three rotated-order repeats, native hit equality across grouping, within-group
   fingerprints/point counts, nonempty brute-force/GMP controls, periodic GMP
   audits and closed durable journals. This adapts the existing November9 test
   to local paths and permitted CPU affinity. It rebuilds archived source, not
   whichever live code happens to be installed. Timings include preparation,
   enumeration, checking and persistence, with startup separate.
2. **Warm lattice reduction:** nearby exact unimodular transform as initial basis,
   fresh reduction, exact certificates and cold fallback. Six unit tests and
   a bounded actual-shell geometry benchmark. Local first results were negative
   (slower in the sampled regions, slightly more enumeration volume). This is
   not a production recommendation. See `warm/WARM_REDUCTION.md`.
3. **Sealed packet validation:** avoids repeated packet construction on reuse,
   preserving content/input binding and corruption checks. Eight tests include
   17 mutation controls. Synthetic transport-only timing uses real packet
   classes, not certified searchable geometry. Initial seal cost can exceed
   savings on single-use packets. See `sealed/README.md`.
4. **CUDA two-stream within-packet overlap:** pinned buffers, two lanes, unchanged
   protocol and global task accounting, complete overflow rejection. Compare
   six controls and actual certified packets against the unchanged engine and
   independent GMP. Replay timings exclude preparation and durable writes.
   Current sequential request protocol prevents cross-request overlap. See
   `overlap/README.md`.

## Local verification vs Cabbage gates

- Python compilation and shell syntax checked.
- Warm reduction: 6 tests passed; sealed packets: 8 tests passed.
- Nine region/group preparation cases passed exact certificate validation.
- Grouped nonempty controls passed against the CPU framed engine and GMP.
- Representative replay packet export passed (20 packet files).
- Overlap harness and error controls passed against the CPU framed engine.
- **CUDA code has NOT been compiled/run here (no nvcc/GPU).**
- **Complete setup/run_all has NOT been executed on GPU hardware.**
- No performance claim from local tests applies to Cabbage or production.

## Install and run

Prerequisites: Linux x86_64, Python3.12 with venv, GCC/G++, GMP development headers,
CUDA nvcc supporting sm86, driver/GPU access, curl/git and ordinary package access.
Both RTX3060 and3080Ti use sm86. Dependency versions are pinned to the archived
initializer. Setup creates a new local directory and virtualenv; no sudo/global
installation. Estimated storage is modest, but reserve several GB for logs/journals.
Use idle hardware. Stop production gracefully through its existing supported
controller and reconcile its checkpoint **before** benchmarking; this package does
not stop it or repair the reported controller KeyError.

From the cloned repository:

```sh
bash experiments/production-speed-tests-20261110/setup.sh "$HOME/fifth42-other-tests-20261110"
timeout --signal=TERM --kill-after=10s 40m bash "$HOME/fifth42-other-tests-20261110/run_all.sh"
```

The directory must not already exist. This fails closed on missing dependencies,
source hash mismatches, GPU compute processes, excessive initial CPU load,
incorrect results or any stage error. The package lock coordinates only these
experiments, not unrelated production tools; quiescent hardware remains required.
Group trials recheck load/GPU activity before each trial. If another workload
appears during later tests, discard affected timing results and repeat on idle
hardware. Do not disable guards to obtain a result.

`run_all.sh` executes warm/sealed tests and benchmarks, grouping, packet export,
and overlap controls/replays. `run_groups.py --region cabbage --repeats 3` is a
shorter grouping-only follow-up. It has a 20-minute internal budget and120-second
per-trial limit. All output paths are new local directories. Compare median
**original fine-grid cells/s**, not physical-task rate. Wider grouping need not
have the same enumeration point counts but must have identical hit sets and
exact interval coverage.

Publish raw diagnostics/result directories with source commit, hardware/versions,
commands, all failures/skips and actual time spent. Large experimental journals
may remain local with hashes; do not accidentally publish production journals.
Do not change production based on a microbenchmark alone.
