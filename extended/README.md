# Exact 192-bit extension and detached jobs

This separate workspace extends the validated 35-million search. The production
and optimization workspaces remain unchanged. No extended full-box GPU run has
started. The parser accepts B<=100,000,000, but that arithmetic maximum is not an
execution recommendation or an approval of a long run.

## Arithmetic and validation

At B=70 million a fifth power exceeds signed and unsigned 128-bit storage.
This implementation stores signed two's-complement 192-bit integers in three
unsigned 64-bit limbs. Host fifth powers are formed with limb multiplication
whose individual intermediates fit unsigned 128 bits. At B<=100 million,
`3*B^5 + 2^63 < 2^191` bounds every actual search intermediate. No floating-point
powers or roots are used. Every returned candidate is independently verified
with Python integers before committing coverage.

The successful high-word-first approach now compares the upper **128** bits of
a sum, allowing for the unknown low-word carry. Ambiguous cases load the low
words and perform the full exact 192-bit comparison. Exact pruning and ordered
pair symmetry are retained. Default GPU variant is `highword`.

GMP headers/libraries are already installed on Ada; no installation is performed.
The CPU reference uses GMP arbitrary-precision arithmetic independently of the
GPU limb implementation. The existing CUDA 12.8 project-only header overlay is
used. Build paths remain g++-13, nvcc 12.8, and sm_86.

```bash
make test
```

Both CPU and CUDA binaries compile. Fourteen general test groups, eight kernel
groups and five detached-launch groups pass on the CPU. There are 13,689 limb
cases and 21,904 upper-word cases independently checked with Python, 375 extreme
power/sum cases, and 1,092 sparse large-power row comparisons against GMP under
UBSan. ASan/UBSan also check the shared row routines. Sparse inputs span both
signs at 44,275,339, 50 million, 70 million and 100 million; no enormous table
allocation is needed for these tests. None of that substitutes for actual GPU
validation. The device self-test includes the same sparse large-power scenarios
and compares all four row variants with independently computed GMP pair lists.

In a **normal GPU-visible Ada terminal**, run:

```bash
cd ~/fifth42/extended
make test-gpu
python3 calibrate.py
```

GPU validation is mandatory for the exact current sources and binaries. The
calibration then measures three 65,536-row samples at B=10 million with a total
30-second budget, records sample ranges/timings, and prints a rough 70-million
projection. It is not a full-box search. Incomplete timing returns nonzero;
neither calibration nor tests launch a long job.

## Proposed next search, pending approval

Proposed bound: **70,000,000**; resource/time limit: **one GPU for four hours**.
Approximate data allocations at chunks of 65,536 rows: **1.53 GB VRAM buffers**
and **3.31 GB host tables**, plus CUDA/process overhead. This doubles the old
bound in every coordinate. The original 35-million timing would project about
3.2 hours without the new width or optimization; those effects cannot be assumed
to cancel. The new calibration, rather than the small old benchmark, must guide
the estimate. No completion time is promised.

After reviewing those resources, the user can explicitly approve and launch:

```bash
python3 jobs.py start --bound 70000000 --hours 4 --approve --job runs/gpu-B70000000
```

The launcher checks GPU validation, calibration fingerprints, and absence of an
active project GPU job. It refuses when the timing projection does not fit the
budget with 10% reserve, suggesting a smaller bound for review. It never silently
extends the budget or changes the bound.

## Independence from chat and terminal

To put validation, calibration and the approved 70-million/four-hour launch in
the background as one sequence, run from the normal Ada terminal:

```bash
bash ~/fifth42/extended/start_background.sh
```

It immediately prints a startup PID and log path. The startup shell uses nohup
and a new OS session, checks for duplicate startup/job directories, validates
with a five-minute timeout, then calibrates and launches only if every check
passes. Startup output goes to `runs/startup-B70000000.log`; the search itself
has its separate `runs/gpu-B70000000/search.log`. Failure is logged and does not
start the long job. `--dry-run` displays the steps without consuming GPU time.

Run the launcher **from the normal Ada terminal**, not the restricted agent
environment. It creates a new OS session, closes terminal input, redirects output
to an ordinary log, and returns immediately with the worker PID and log path.
The detached worker ignores SIGHUP. Closing this chat, closing the launching
terminal, or disconnecting SSH does not own or stop that worker. Ada must remain
powered on. These properties are tested by exiting the launching parent and
sending the worker SIGHUP before checking a durable output marker.

The worker enforces the chosen wall budget. The inner runner reserves one minute
for startup/cleanup; at expiration it terminates the active engine and retains
the last committed row prefix, with up to ten seconds termination grace. Every
chunk is atomically checkpointed and writes a progress line. There is no automatic
continuation. Failed launches and exits are recorded even if no checkpoint exists.

From a normal Ada terminal, inspect or stop without this interface:

```bash
python3 jobs.py status --job runs/gpu-B70000000
tail -f runs/gpu-B70000000/search.log
python3 jobs.py stop --job runs/gpu-B70000000
```

Status reads atomic checkpoints without taking the writer's lock. PID start times
and process namespaces are checked before sending a signal, so stale/reused PIDs
do not cause a different process to be stopped. Raw checkpoints and logs remain
local and ignored by Git.

A separately approved continuation uses a **new attempt directory** and the old
compatible checkpoint, for example:

```bash
python3 jobs.py start --bound 70000000 --hours 4 --approve \
  --job runs/gpu-B70000000-attempt2 --resume-run runs/gpu-B70000000/coverage
```

Do not edit/rebuild the extended sources or binaries during a job: fingerprint
checks deliberately reject changed code. A partial prefix is not proof of the
whole configured box. See the final status for the coverage actually completed.

## Resuming an interrupted calibration

Calibration keeps completed, validated samples when the source/binary fingerprint
matches, and runs only missing regions. A new invocation has a fresh 30-second
budget. No full GPU validation is repeated when the two passing reports still
match; startup performs the saved-report check before deciding to run tests.

The initial 30-second attempt saved the negative-edge and middle samples, then
stopped before completing the positive edge. It did not launch the 70-million
search. Their timing suggests that 70 million may exceed a four-hour budget.
A more conservative proposed next bound is **50 million**, still beyond the
completed 35-million box, with the same **four-hour maximum**. Data buffers are
about **1.09 GB GPU** and **2.37 GB host**, plus runtime overhead. To explicitly
approve that bound and cap while resuming calibration in the background:

```bash
bash ~/fifth42/extended/start_background.sh --bound 50000000 --hours 4
```

The positive-edge sample is measured first. The long job starts only if the
completed calibration projects this chosen bound within the capped budget with
reserve. The bound is never changed silently. This attempt's startup log is
`runs/startup-B50000000.log`; its job directory is `runs/gpu-B50000000`. Use
`python3 jobs.py status --job runs/gpu-B50000000` after the job starts. Closing
the terminal or this chat does not stop the detached sequence.
