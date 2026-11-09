Reproduction on the existing Ada deployment

Use the pinned Python 3.12 environment and existing resource helper; all GPU tests
are covered by the original CPU/GPU leases. Recreate experiments/worker using
make_worker.py and the released worker source plus baseline overrides. Reuse the
validated binaries from the NFS bundle or build the actual native-baseline and
independent GMP sources with the validated host toolchain. A fresh build may have
host-specific binary hashes; --allow-rebuilt-binaries permits only those binary
differences and never a source difference. Run correctness tests before timings.

The run_validation.py, run_wire_validation.py and run_scheduling_validation.py
wrappers perform the exact/GMP, failure/recovery and queue tests. benchmark.py,
benchmark_wire.py, benchmark_scheduling.py, benchmark_holdout.py and
benchmark_boole4.py recreate the five timing matrices. Their commands and per-trial
parameters are in source; results/ contains every original sample. Source groups
and candidate/certificate/packet signatures are checked across every comparison.

These are deployment-specific tools: external environment/helper paths describe
the actual Ada setup, and peer nodes must use their own validated resource guard
and pinned interpreter. TEST_ONLY outputs never alter production reservations or
claim full mathematical coverage. RAM-only timings provide no durable checkpoint.
