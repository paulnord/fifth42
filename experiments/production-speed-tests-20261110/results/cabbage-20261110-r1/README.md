# Cabbage: grouping, warm reduction, packet sealing and GPU overlap

All four investigations completed on Cabbage. **Group 8 was the useful whole-pipeline
result in the sampled Cabbage region: +48.2% over group 4.** Production remains stopped.
Source: [`cb908547e6cefd51713da9595073e576eaca6950`](https://github.com/paulnord/fifth42/tree/cb908547e6cefd51713da9595073e576eaca6950/experiments/production-speed-tests-20261110).

| Test | Measured result | Scope |
| --- | --- | --- |
| Grouping | Cabbage: group 4 **24,462**, group 8 **36,249**, group 16 **30,136** original cells/s | Whole pipeline; preparation, exact checks, GMP audit, native work, durable journal and final flush; startup separate |
| Warm lattice reduction | About **36% slower** in both ordinary sampled regions; near-zero region mostly used cold fallback | Reduction/geometry microbenchmark; no native enumeration |
| Sealed-packet reuse | Repeated validation **2.580 → 1.420 ms**, **1.82×** faster; initial seal **12.661 ms** | Synthetic 1,024-task transport validation only |
| Two-stream GPU overlap | Certified-packet aggregate **34.060 → 33.733 ms**, **1.010×**; controls **0.928 → 0.930 ms** | Persistent native packet replay; excludes preparation and journals |

Grouping varies by region; group 8 is not a universal choice:

| Region / first cell | Group 4 | Group 8 | Group 16 |
| --- | ---: | ---: | ---: |
| Ada / 4,564,955,776 | **21,478** | 20,145 | 8,088 |
| Cabbage / 2,572,492,928 | 24,462 | **36,249** | 30,136 |
| Dense / 9,562,500,096 | **6,497** | 6,483 | 6,375 |

Units are original width-8 cells per second. Each entry is the median of three
rotated-order trials of 32,768 cells with 16 workers. Point counts/certificates
need not match across grouping; repeated identical groups had matching signatures,
point counts and physical-task counts. Exact hit sets matched across grouping.
All selected trials passed GMP audit, final journal drain and recovery checks.
The selected 27 samples are in `SELECTED_GROUPING_SAMPLES.json`; all 43 completed
trials, including the interrupted runs, remain in the raw archive. The Ada subset
comes from the original run; Cabbage uses its complete region-specific follow-up;
dense uses the complete final cooldown-enabled region run.

Warm reduction passed all **6 unit tests**, exact unimodular-transform/inverse checks
and complete small-sphere point comparisons. At first cells 3,750,000,000 and
7,192,000,000, cold reduction medians were 3.857/3.822 ms; warm medians were
5.250/5.189 ms. The associated box volumes increased slightly. At first cell zero,
all 15 attempted neighbor seeds per warm trial fell back to cold; no enormous
coefficient box was enumerated or counted as coverage.

Sealed packets passed all **8 unit tests**, including mutation and corruption controls.
The setup cost requires roughly 11 validations of the same packet to amortize
against the measured per-call savings. These synthetic packets are explicitly
not certified searchable geometry, and the result is not a search speedup.

Overlap passed capacity-failure, malformed-input and subsequent-clean-request
controls on the actual CUDA engine. Six nonempty/boundary control packets and
20 certified actual-shell packets matched independent GMP counts and complete
hit records on warmup and every timed replay. There were 7 alternating-order
repeats: 84 timed control responses and 280 actual-packet responses. The aggregate
above sums each packet's median RPC wall time. Individual paired full-packet-repeat
ratios ranged about 0.990–1.016. This is a small mixed difference, not evidence of
a reliable whole-pipeline gain. Per-stream kernel event sums are not interpreted
as the critical-path wall duration. All raw responses and timings are retained.

## Recorded failures and isolated scheduling correction

The original unmodified `run_all.sh` stopped after 23 grouping trials because its
system one-minute CPU-load guard exceeded **4**. Its dense-only retry stopped
after two trials for the same reason. No other heavy job was seen in the process
snapshots, but continuous outside-process telemetry was not recorded; the cause
appears to be the benchmark's own 16 preparation workers and lingering load average.
Both failures, tracebacks, exit codes, partial samples and cooldown records are
preserved. They are not represented as successful full `run_all` invocations.

The final isolated copy adds a bounded wait (at most 120 seconds) before admission
when that same load guard is high, rechecking the GPU guard while waiting. The
load threshold remains 4; the GPU check, timed child commands, arithmetic and
correctness checks are unchanged. `load-cooldown.patch` is the exact code diff,
and the tested source archive includes it. No cooldown was actually needed on
the final dense pass. All work remained inside the original 40-minute bound.
There were no CUDA build/API corrections or skipped requested components.

## Installation, provenance and reproduction

The supplied `setup.sh` ran in a fresh local directory with a new virtualenv and
pinned sympy 1.14.0, gmpy2 2.2.2, fpylll 0.6.4, cysignals 1.12.5, numpy 2.3.5.
It verified the archived source and built the baseline CUDA engine, overlap
engine and independent GMP reference. CUDA 13.2.78 and g++-13 were selected through
local wrappers; the previously diagnosed scratch NVVM layout was reused without
changing the original CUDA toolkit. Hardware: RTX 3060, Ryzen 9 5950X, 16 physical
cores/32 threads, driver 595.99.02. Exact versions and unrelated process snapshots
are in `logs/`. The existing Cabbage GPU lease and 16-core affinity were held.

Commands, setup output, every failure and the bounded follow-up invocations are
in `COMMANDS.json`, `CONTINUATION.json`, `DENSE_COOLDOWN_STATUS.json` and `logs/`.
The supplied whole suite was invoked with `timeout --signal=TERM --kill-after=10s
40m bash <fresh>/run_all.sh`. After the recorded guard stop, its unchanged
region-specific grouping and overlap commands were run separately, with the
scheduling patch disclosed above. No replacement numerical benchmark was invented.

`tested-source.tar.gz` and `TESTED_SOURCE_MANIFEST.json` identify the exact source
used, including the isolated scheduling change. The experiment's full worker
manifest retains the actual built executable hashes; binaries are retained locally
and can be rebuilt using the supplied setup. `raw-results-and-logs.tar.gz` contains
all compact results, timings, stdout/stderr, independent audit receipts, checkpoints,
packet inputs, responses and failure logs. The **83,219,812 bytes** of experimental
coverage journals are retained locally at the paths in `RAW_RESULT_MANIFEST.json`,
with sizes and full SHA256 hashes, as permitted by the handoff. No production journal
is included. The manifest also indexes every published raw result member.

## Production stop reconciliation

`PRODUCTION_RECONCILIATION.json` verifies worker exit 0, released leases, zero pending
journal records, matching final local/NFS checkpoint and a successful final-copy
receipt at **cell 1,538,849,024**. The controller's `KeyError('worker_exit_code')`
is consistent with treating a deactivating service as finished and reading the
supervisor's report before its final fields exist. Its eventual final report is
clean. This is a source/timeline diagnosis; production was not repaired or restarted.
Before any later production restart, the controller race needs a reviewed fix and
validation, and the reconciled committed cursor must be used. Production source,
configuration, services, deadlines, shared ledger and reservations were not changed.
`FINAL_SAFETY_CHECK.json` rechecks unchanged source/configuration/checkpoint identities
and absence of production/GPU workers after the experiments.
