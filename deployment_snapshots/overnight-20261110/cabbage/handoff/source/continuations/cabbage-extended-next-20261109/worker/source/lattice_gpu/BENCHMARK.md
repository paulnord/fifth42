# Larger CUDA timing run

Run from a normal ADA terminal with GPU access:

```bash
python3 ~/fifth-lattice-gpu/benchmark.py --wait
```

The command waits up to 30 minutes for the CPU benchmark and production locks.
It does not hold the GPU validation lock while waiting for the CPU. Its own
ten-minute benchmark allowance begins after resources are acquired. A busy
GPU, changed validation sources, active production work, or failed checks
prevents execution. Ctrl-C stops the waiting command. To inspect readiness
without starting work, use `--check-only` instead of `--wait`.

The benchmark compares CUDA with ordinary CPU emulation at bounds 2,000,
4,000, and 8,000. Each completed level has five alternating paired repeats.
The domain is `1 <= a <= b < c <= bound` with
`abs(a^5+b^5-c^5) <= 42`. It uses the previously validated coefficient-box
prototype. This differs from the fpylll/pruning/GMP CPU implementation and
the optimized direct CPU solver in the CPU scaling reports.

The runner copies the validated sources into a new scratch workspace, runs
the host tests, builds serially, and uses an isolated copy of the host planner
whose full-domain limit is 8,000. The validated planner's 1,000 limit is
preserved. Task, point, integer, exact-certificate, output-capacity, and
coverage guards remain in force: at most 4,096 tasks, 50 million packet
points, and 10 million points per patch.

An independent native 128-bit oracle searches the full positive domain
without lattice code or modular filters. Nonempty residual controls at bounds
34 and 100 must pass before timing larger domains. Each timed CPU/CUDA result
must match the oracle and the exact per-task point counts.

For each domain, host preparation and packet certification run once.
The output records preparation, CUDA kernel, engine, complete engine-process,
host verification, cached-packet, and end-to-end timings separately.
Each timed engine invocation starts a new process; kernel timing excludes
process/context startup. End-to-end time includes the one-time preparation
cost, while cached-packet time excludes it. These are distinct use cases.
Independent oracle work is excluded from timing medians but included in the
overall ten-minute allowance. CUDA subprocess wall time has an additional
cumulative 120-second cap, including control runs.

Progress and the final report path are printed in the terminal. Results are
saved under `~/fifth-lattice-gpu/benchmark-runs/<UTC timestamp>-*/report.json`,
with individual trials, exact oracles, plans, packets, build/test logs, source
and binary hashes, GPU identity, and a detailed `results.json`. A point that
does not complete all five pairs has no median and is not reported complete.
The runner never starts a production search or schedules a continuation.
