# fifth42

Exact CPU and CUDA searches for integer solutions of

```text
x^5 + y^5 + z^5 = 42
```

**Result:** no solutions with all three absolute values at most **35,000,000**.
The full signed box was completed on an RTX 3080 Ti using exact arithmetic:
6,363,637 canonical z rows, 202,479,360,247,934 two-pointer steps, 45.8 minutes
of GPU search time and 47.6 minutes of engine wall time. This is a finite-box
result, not a proof of nonexistence for arbitrary integers.

See [coverage](COVERAGE.md) and the compact [results](results/coverage.json).
All development and searches used Ada at Valparaiso; no BNL resources were used.

## Build and validate

The tested toolchain is CUDA 12.8 with `/usr/bin/g++-13`, targeting `sm_86`.
No packages or drivers are installed by the build.

```bash
make test
make test-gpu
```

`make test` runs the CPU checks and, when a GPU is visible, GPU comparisons.
It explicitly reports blocked GPU tests when no device is exposed. `make test-gpu`
requires actual device execution. The production version passed all 14 groups,
58 GPU search comparisons and 18,769 device arithmetic cases; host arithmetic
also passed Python arbitrary-precision and undefined-behavior sanitizer checks.

The CUDA 12.8/glibc 2.43 header conflict is handled by `configure_cuda.py`, which
creates a project-local compatibility header. It preserves the system header
and license and omits only three unused conflicting math declarations in CUDA
translation units. Generated headers are not committed. The toolchain paths
can be overridden with Make variables; the tested configuration is the default.

## Search and restart

Modulo 11, fifth powers are 0 or +/-1. Since 42 is -2 modulo 11, the three
residues must be a permutation of (0,-1,-1). Assign z the unique multiple of 11
and order the remaining variables a<=b. Their allowed residues modulo 11 are
2,6,7,8,10, including normalized residues for negative integers.

For each z, a monotone two-pointer search finds all pairs in the sorted fifth-
power table. CPU arithmetic uses signed `__int128`; GPU arithmetic uses two
unsigned 64-bit limbs. Every candidate is checked independently with Python
integers before its chunk counts as covered. There are no floating-point roots.
At the enforced maximum B=35,000,000, `3*B^5 + 2^63 < 2^127` bounds all actual
intermediates. Bounds above that maximum are rejected.

After successful GPU validation, a modest restartable example is:

```bash
python3 run.py new --backend gpu --bound 10000 --chunk-rows 256 \
  --max-seconds 10 --run runs/example
python3 run.py status --run runs/example
python3 run.py resume --run runs/example --max-seconds 10
```

Raw state files are atomic, fsynced checkpoints. They contain exact row ranges,
step counts, verified candidates and source/binary fingerprints. Interrupted
chunks are retried; prior committed chunks remain covered. A lock prevents
concurrent writers. Changed sources/binaries are rejected on resume. The status
command is intended after the running writer releases its lock.

Runs above B=100,000 or over 30 seconds require prior approval of bounds, time
and resources and the explicit `--approved-long` switch. No background service
or automatic continuation is installed. See [search details](docs/SEARCH.md).

## Optimization experiments

The independent [optimization workspace](optimization/README.md) contains
cached-endpoint, exact-pruning and high-word-first CUDA candidates. They compile
and pass the 14 existing CPU groups plus eight new groups, with 21,904 high-word
cases checked against Python and shared row routines checked under ASan/UBSan.
The subsequent GPU validation passed all 22 groups. In a single three-region
benchmark at B=1 million, the high-word variant reduced aggregate search time
from 1.229287 s to 0.750744 s (about 1.64x); this is not a guaranteed larger-bound
speedup. The production baseline remains unchanged. See
[measured timings](results/gpu-optimization-benchmark.json).

When the production GPU is idle, use a normal GPU-visible terminal:

```bash
cd optimization
make test-gpu
python3 bench_gpu.py
```

The GPU checks and benchmark refuse to overlap the production run's active lock.
The comparison benchmark has a 30-second budget, saves exact sample ranges and
compares against a separately rebuilt production reference. It does not launch
another full-box search.

## Repository contents

Source, tests, documentation and compact reviewed results are tracked. Executable
binaries, raw run directories, machine identifiers, generated system headers,
large archives, credentials and profiler captures are ignored. Raw checkpoints
remain available locally but are necessary for resuming those original jobs;
the committed summaries are evidence summaries, not restart files.

Refresh local result summaries with `python3 scripts/export_results.py` and check
the staged repository with `python3 scripts/check_repository.py`. The latter
checks known credential patterns and generated/binary/large files; it is a
focused review aid, not a guarantee to recognize every possible secret.

## Beyond 35 million and detached jobs

The separate [192-bit extension](extended/README.md) supports larger exact powers
and a launcher independent of this chat or the launching terminal. Its CPU and
detachment checks pass; its new GPU binary still requires device validation.
The concrete pending proposal is B=70 million with one GPU and a four-hour cap.
No extended long job has started. Read the resource estimates and validation
steps before explicitly approving the launch.
