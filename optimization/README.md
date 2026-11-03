# GPU optimization experiments

This directory is independent of the production search in the parent directory.
Editing, compiling and testing here leaves the production source, executable and
checkpoint fingerprints unchanged. Do not promote a candidate until its device
tests pass and measured GPU times show a benefit.

## Candidates

* `baseline`: the original two-pointer loop, compiled in this experiment.
* `cached` (default): retain both endpoint powers in registers and reload only
  the endpoint whose pointer changed. This preserves the original step count.
* `pruned`: cached loop plus exact bounds on feasible pairs, found with binary
  searches. If `a^5 < goal-max_power`, no partner can reach the goal. If
  `b^5 > goal-min_power`, every partner is too large. Ordered pairs also require
  `a^5 <= floor(goal/2)` and `b^5 >= ceil(goal/2)`. All boundaries include equality.
* `highword`: the same pruning with separate arrays of low/high words. The high
  word of a sum is either `a_hi+b_hi` or that value plus one. When both compare
  the same way with the target's high word, low words cannot change the answer.
  Otherwise perform the full exact 128-bit comparison. Unsigned carry/wrap and
  signed high-word ordering are explicitly handled.

The device emits pair indices, decoded on the host, so it no longer needs the
entire integer-value array. At B=35 million that removes roughly 127 MB of device
allocation and upload. Packed powers have 16-byte alignment. Block sizes 64,
128, 256 and 512 are accepted for later controlled tuning.

All actual powers and pair/target arithmetic remain within the same proven
35-million signed-128-bit limit. No floating-point approximation is used.

## Validation and limits of present evidence

```bash
make test
```

This builds the CUDA candidates but runs only CPU tests, so it can be used while
the production GPU job runs. It checks the existing 14 groups plus eight
optimization groups. The exact row routines compiled for the GPU are also
compiled for CPU emulation and compared with the native-128-bit reference and
Python integers. Known positive solutions, negative/repeated variables, all row
partitions, empty slices, large cancellation, capacity failures, ASan and UBSan
are included. High-word comparisons are checked against Python on 21,904 cases,
including carries, sign boundaries, wrapped bit patterns, equality and adjacent
targets. Emulation is never labeled as GPU validation or search coverage.

At a test edge row with B=1000, the two-pointer comparisons fall from 910 to
703 with pruning. That is an exact operation count, **not a GPU speedup claim**.
Static compilation reports 26 registers for the experimental baseline,
36 cached, 38 pruned and 34 highword, with no stack/local spill allocation.
The production baseline uses 28 registers. Additional register pressure can
offset saved loads, so benchmarks must decide the winner.

The production checkpoints put about 95% of elapsed engine time in the search
kernel, so a persistent process/table cache would address only a few percent
of this run. Kernel memory traffic, dependencies and branching are the primary
experiments. Their precise hardware bottleneck is not yet profiled.

## GPU validation and bounded comparison after the production job

From a GPU-visible normal Ada terminal:

```bash
cd ~/fifth42/optimization
make test-gpu
python3 bench_gpu.py
```

Both steps check that the production 35-million run has released its lock.
Device tests must pass for the exact current sources/binaries before the
benchmark will run. `make test-gpu` rebuilds unchanged production source as
`reference_gpu`/`reference_cpu` and records their hashes, avoiding committed
binaries. `bench_gpu.py` compares the reference and all three optimized variants
on 65,536-row samples in negative-edge, middle and positive-edge regions at
B=1 million. It verifies every candidate with Python, compares hits with the
reference, saves timings incrementally, and has a 30-second total budget.
Those overlapping samples do not establish whole-box coverage. The script
does not launch a larger search or automatically continue after the budget.

Only after these measurements should we try block sizes or profile selected
short kernels with the locally installed Nsight Compute. Profiling adds overhead,
so profiler timings must not be confused with normal benchmark timings.
