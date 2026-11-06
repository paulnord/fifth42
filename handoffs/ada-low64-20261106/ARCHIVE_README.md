# ADA morning test handoff

Prepared 6 November 2026. This is an isolated test package, not a deployment.
No ADA command, GPU run, remote publication, live checkpoint change or restart
was performed while preparing it. The overnight search and final publisher must
finish before anyone starts these tests on ADA.

## What is actually ready

- **New proposed low64 kernel candidate:** source, exact patch, CPU builds,
  bigint audit, bounded CUDA build commands and an A/B parity probe are included.
  CPU and UBSan checks passed here. CUDA compilation and execution are **not run**.
  Treat it as a candidate to validate, not a validated GPU implementation.
- **Original host arithmetic, coordinator/prefetch and batch-size prototypes:**
  runnable CPU commands are below. Their engine sessions and status fields are
  hard-coded for CPU emulation. They cannot be turned into CUDA tests by passing
  a different binary. No GPU adapter is included or claimed.
- **Multiple coordinators and fixed-time distinct-coverage exploration:**
  still experimental. No integrated GPU executor has been validated. Do not
  replace the overnight job with either prototype.

The earlier low64 result (1.44x on one selected CPU packet) and combined host
result (1.38x in a separate CPU experiment) are not GPU/end-to-end speedups and
must not be multiplied together.

## Included files and provenance

- `fifth42-sieve-findings-and-reproduction-20261106.tar.gz`: unchanged original
  source/evidence bundle. SHA-256:
  `49fffe13be7d569c54164be0850d5d13107dfd1646cb2aaacd9fb75d0a575075`.
  This already contains the reconstructed coordinator source, base archive and
  ordered patches. Do not reapply those patches to the reconstructed tree.
- `prepare_low64.py`, `low64.patch`: new scratch-only fixed-cap filter.
- `build_cpu.sh`, `build_gpu.sh`: independent baseline/candidate binaries.
- `probe.py`: complete packet-count/hit-record comparisons, synthetic bigint
  controls, persistent-engine error recovery and raw calibration vectors.
- `predicate_audit.py`: independent UBSan/bigint test of the new helper.
- `ada_guard.py`: manual, nonwaiting execution gate using the existing ADA
  resource guard and leases; stops only its own process group.
- `test_handoff_guard.py`: five local service-state and process-cleanup tests.
- `validation/`: actual local results, compiler/dependency state and source hashes.
- `SHA256SUMS`: every delivered file except this checksum list.

The new helper uses unsigned arithmetic: with `u = r mod 2^64`, accept the
necessary condition `(u+C) <= 2*C` for the actual fixed cap C. The existing reader
requires `C <= INT64_MAX`. It handles C=0 and negative residuals, is inserted
after the canonical coordinate checks, and retains the full exact I192 residual
test. Mode 1 (`5*c*c`) bypasses this new filter entirely. The existing documented
2*10^11 scratch range overlay is used unchanged; no production guard is edited.

## 1. Transfer and verify, without touching live files

Download this handoff archive, transfer it manually to a **new scratch directory**
on ADA, and extract it there. Do not use the production checkout, environment,
launchers, publisher or checkpoint directories. From the extracted handoff:

```bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
sha256sum -c SHA256SUMS
H="$PWD"
tar -xzf fifth42-sieve-findings-and-reproduction-20261106.tar.gz
B="$H/fifth42-sieve-findings-20261106"
(cd "$B" && sha256sum -c SHA256SUMS)
AB="$H/low64-ab"
python3 prepare_low64.py --bundle "$B" --output "$AB"
```

Every result directory must be new. Preserve failed/partial outputs and use a
new name for a retry. No command starts a background service, schedules a retry
or publishes results. Verify the checksum list before running any supplied code.

## 2. ADA safety gate and dependencies

Required for native checks: Linux, Python 3.12, `g++` C++17 with unsigned 128-bit
support, UBSan, GNU `timeout`, `sha256sum`, `bash`. Here: Python 3.12.14, g++ 14.2.0.
For GPU: an accessible NVIDIA device, compatible driver/toolkit/compiler,
`nvcc`, `nvidia-smi`, and the correct architecture target. Do not infer the target
from the name ADA: the archived build used sm_86; an Ada-generation GPU can need
sm_89. Query the actual device and choose the supported target.

The gate requires the archived service name to be loaded, inactive and dead,
and no `overnight_service.py`, `overnight_search.py` or `github_status.py` process
to remain. That means the final publisher has exited, not that publication
succeeded. Separately inspect the final search/publisher results before deciding
what work is new. Do not stop or kill a live job to make this gate pass.

It imports ADA's existing resource helper at
`/home/pnord/fifth-lattice-optimizations-ada-20261105/benchmark_ada.py`, takes its
ordinary nonblocking leases through the archived benchmark helper, checks GPU
idleness and rechecks service/production/load/memory blockers while running.
It requires the existing `/home/pnord/fifth-lattice-gpu` lease directory too.
Missing or changed service paths, helper APIs, compiler paths, or tool support
are blockers, not reasons to bypass the gate. No GPU idle snapshot alone is an
authorization or sufficient exclusion lock. A check-only pass releases leases;
each actual command reacquires them.

```bash
python3 "$H/ada_guard.py" --bundle "$B" \
  --output "$H/preflight" --check-only
cat "$H/preflight/guard-report.json"
```

Do not run the remaining ADA commands if the preflight defers. If the live
service was renamed or unloaded, verify its replacement and the final publisher
state with the owner before adapting the gate. Never omit the guard to work
around a refusal. Live ADA integration of this wrapper is untested here.

## 3. Build and verify CPU paths first

On ADA, invoke each command through the gate. On an unrelated local Linux machine
with no shared ADA job, the inner CPU commands can run directly under `timeout`.

```bash
python3 "$H/ada_guard.py" --bundle "$B" --seconds 120 \
  --output "$H/cpu-build-guard" -- bash "$H/build_cpu.sh" "$AB"
python3 "$H/ada_guard.py" --bundle "$B" --seconds 150 \
  --output "$H/cpu-probe-guard" -- python3 "$H/probe.py" \
  --work "$AB" --backend emulated --repeats 2 --output "$H/cpu-probe"
python3 "$H/ada_guard.py" --bundle "$B" --seconds 150 \
  --output "$H/ubsan-probe-guard" -- python3 "$H/probe.py" \
  --work "$AB" --backend emulated --ubsan --repeats 1 --output "$H/ubsan-probe"
python3 "$H/ada_guard.py" --bundle "$B" --seconds 90 \
  --output "$H/predicate-guard" -- python3 "$H/predicate_audit.py" \
  --work "$AB" --output "$H/predicate-audit"
```

Require all reports to say `passed` before proceeding. These commands never use
prebuilt archived binaries. Do not use Python `-O`; the probes refuse it.

## 4. First bounded low64 CUDA comparison

Read `preflight/guard-report.json` for the actual GPU compute capability. Set
the target accordingly; the example assignment below is intentionally absent
to prevent guessing the architecture.

```bash
# Set only after checking the queried device, for example:
# export CUDA_ARCH=sm_86
# or export CUDA_ARCH=sm_89
test -n "${CUDA_ARCH:-}" || { echo 'Set verified CUDA_ARCH first'; exit 2; }
python3 "$H/ada_guard.py" --bundle "$B" --seconds 180 \
  --output "$H/gpu-build-guard" -- bash "$H/build_gpu.sh" "$AB"
python3 "$H/ada_guard.py" --bundle "$B" --seconds 150 \
  --output "$H/gpu-probe-guard" -- python3 "$H/probe.py" \
  --work "$AB" --backend gpu --repeats 2 --output "$H/gpu-probe"
```

The probe has its own 120-second total deadline and at most 10 seconds per engine
request. The outer guard has a 150-second execution cap plus bounded cleanup.
Both variants use the same packet bytes, output capacity (65,536), 256-thread
launch configuration and source range limits. It runs fresh persistent sessions,
warms them, alternates AB/BA order, preserves all raw timings, and fails on any
count or complete-hit-record discrepancy. GPU responses must identify `gpu`.

Validation includes four immutable packets, positive and negative nonempty
controls, cap 0/1/12/42/960/2951/INT64_MAX, maximum-base controls, the deliberate
low64 alias (8192,8192,16384), mode 1 preservation, capacity overflow, malformed
requests and successful recovery in the same persistent session. Complete hit
records retain task and linear index, not just a deduplicated empty hit set.

This tests a kernel candidate on frozen packets, not fresh host preparation or
new search coverage. The high8/high32 packets cover the same narrow selected
ratio strip near 0.3 for 100000000001 <= c <= 200000000000. Small packets omit
direct low-c bands; synthetic point controls cover important omitted hits but
do not certify those whole bands. No full-shell or larger full-box claim follows.

Inspect `low64/cuda-build.stderr` versus `baseline/cuda-build.stderr` for ptxas
register/spill changes. The probe records CUDA event kernel time, engine time,
RPC wall time and host decode time. It does **not** separate transfers or measure
occupancy, device memory peaks or fresh preparation/commit cost. Two repetitions
are a smoke/calibration check, not a reliable performance conclusion. Only after
correctness passes, an optional second probe with `--repeats 6` in new output
directories gives a small balanced calibration. Do not expand into a long sweep.

## 5. Host and batch prototypes: runnable CPU checks, GPU work still required

Required optional pins are in the original bundle's `requirements-reproduction.txt`:
fpylll 0.6.4, cysignals 1.12.5, gmpy2 2.2.2, NumPy 2.3.5, SymPy 1.14.0.
Use an existing verified pinned environment or a **new scratch venv**, never
install into ADA's live overnight environment. A fresh install, if needed, is:

```bash
python3.12 -m venv "$H/venv"
"$H/venv/bin/python" -m pip install -r "$B/requirements-reproduction.txt"
PY="$H/venv/bin/python"
HOST="$H/host-recheck"
python3 "$H/ada_guard.py" --bundle "$B" --seconds 300 \
  --output "$H/host-tests-guard" -- "$PY" "$B/reproduce.py" host-tests --output "$HOST"
R="$HOST/fifth42-coordinator-20261105"
```

If dependencies are already available, set `PY` to that verified interpreter
instead of reinstalling. Venv/install steps should also wait until the job and
publisher finish. Stop on a package or compiler mismatch.

Bounded one-repeat CPU functional checks, all with fresh preparation and exact
verification, use the ordinary baseline CPU binary from the A/B source tree:

```bash
python3 "$H/ada_guard.py" --bundle "$B" --seconds 300 \
  --output "$H/host-arithmetic-guard" -- "$PY" "$R/lattice_gpu/host_optimization_benchmark.py" \
  --source "$R/lattice_prototype" --engine "$AB/baseline/bin/scaling_cpu" \
  --output "$H/host-arithmetic" --workers 4 --repeats 1
python3 "$H/ada_guard.py" --bundle "$B" --seconds 300 \
  --output "$H/coordinator-guard" -- "$PY" "$R/lattice_gpu/coordinator_benchmark.py" \
  --source "$R/lattice_prototype" --engine "$AB/baseline/bin/scaling_cpu" \
  --output "$H/coordinator" --lo 100000000001 --hi 200000000000 \
  --first 3751385984 --patches 1024 --bits 222 --workers 4 --engine-threads 1 \
  --repeats 1 --max-seconds 60
python3 "$H/ada_guard.py" --bundle "$B" --seconds 300 \
  --output "$H/batch-guard" -- "$PY" "$R/lattice_gpu/coordinator_batch_sweep.py" \
  --source "$R/lattice_prototype" --engine "$AB/baseline/bin/scaling_cpu" \
  --output "$H/batch" --workers 4 --repeats 1
```

Arithmetic checks compare reference/root/inverse/combined modes on the same
1,024 patches. Coordinator checks compare baseline/fused/packed/prefetch. The
batch script compares 256/512/1024/2048/4096 task caps on one 4,096-patch window,
preserving original 256-patch checkpoint commits and all native guards.
These are CPU functional controls. Their single-repeat timing is not a GPU or
statistically robust speed result. All core processes share the allocated CPUs;
this is not a verified 16-physical-core ADA production comparison.

Before a host/batch CUDA experiment exists, implementation must:
1. Add an explicit backend option, launch CUDA without CPU `--threads`, require
   the `gpu` handshake, and pass actual backend values into exact decoding.
2. Record GPU-specific event metrics honestly, leaving transfer/occupancy fields
   unavailable unless instrumented; correct CPU-only result/status labels.
3. Establish CPU/CUDA parity on the same canonical certificates, geometry,
   packet routing, complete counts, exact hit records and durable commits.
4. Retain a single engine/journal owner, bounded prefetch, original limits and
   recovery semantics, then repeat small same-work controls under ADA leases.

Do not work around the missing adapter by editing a reported backend string.
Do not benchmark 2x8 coordination or claim a fixed-time exploration result from
the current CPU prototypes. The prepared distinct-coverage plan has a
non-exhaustive prior ledger and no validated integrated executor. After small
controls, follow Paul's objective: distinct certified geometric coverage per
fixed total wall-time budget, not repeated regions or summed patch rates.

## Validation checklist and stop conditions

- [ ] Original archive and delivered script checksums match; fresh scratch only.
- [ ] Overnight search **and final publisher** exited; final evidence inspected.
- [ ] Current ADA service/guard paths verified; ordinary leases held continuously.
- [ ] GPU idle; CPU/memory limits pass; actual CUDA target/toolchain recorded.
- [ ] Rebuilt CPU/UBSan, bigint audit and CUDA probe all say `passed`.
- [ ] Nonempty +12 and -30 controls survive; the modular alias is rejected by
      the full residual check; cap zero and mode 1 are unchanged.
- [ ] Every expected point/task visited and full hit records agree; capacity or
      malformed-input failures produce no completed-coverage claim.
- [ ] Source/binary/packet hashes and raw timing vectors retained; no extrapolated
      GPU speedup from CPU timings and no multiplication of separate ratios.
- [ ] Guard/timeout/certificate/overflow failure stops the test. Preserve logs;
      never relax a guard, overwrite evidence, touch the live checkpoint or publish.
- [ ] Production recommendation waits for real CUDA compilation, controls and
      measurements. No new coverage is credited from this handoff's probes.

## What was checked here, and exact blockers

**Passed locally:** original bundle checksum verification; original native
reproduction (eight packet/mode audit comparisons, gcd parity checks, 100,008
bigint triples and 18,228 predicate/control checks); new baseline/low64 CPU and
UBSan complete-packet/control probes; new helper's 60,368 seeded bigint/UBSan
cases; Python syntax and shell syntax checks. Local reports are in `validation/`.
Five guard unit tests also passed, including a lingering publisher, false-finished
service states and a SIGTERM-resistant descendant after its group leader exited.

**Not run:** CUDA compile/run, live ADA lease/service integration, host/batch
reproduction with pinned optional dependencies in this executor. Here `nvcc` and
`nvidia-smi` are absent; fpylll, cysignals and gmpy2 are not installed. The original
archive reports its earlier 107 host tests passed, but that is not a fresh run
here. CUDA/compiler compatibility, actual device target and current live paths
must be established on ADA. All these are pending/unavailable checks, not denied
remote operations. No remote operation was attempted.

**Implementation blocker:** the host/batch CUDA adapter and integrated
distinct-coverage executor do not exist in this package. The low64 path is a
new proposed GPU candidate with tested CPU semantics, not a GPU-validated release.
