# Isolated coordinator experiment

This opt-in experiment adds no production launcher and changes no existing
source file. Do not replace ADA's overnight sources, publisher or checkpoint.
The command below is CPU-only and is **not** an ADA launch command: it does
not acquire ADA's leases. On ADA, first finish the overnight search and final
publisher, use the normal resource guard, and follow the existing
[coordinator experiment plan](../ada_validation/coordinator-throughput-20261105/README.md).

## Implemented candidates

- `baseline`: instrumented separate preparation/certification pool maps and
  separate certificate/geometry serialization, matching the existing algorithm.
- `fused`: one prepare-and-certify worker call. The independent exact certificate
  reconstruction still runs; no check or coefficient is skipped.
- `packed`: fused workers plus one canonical serialization per task, reused for
  its certificate check and geometry hash. All packet and total-work guards,
  direct-work handling and canonical bytes match `packing_opt.assemble`.
- `prefetch`: packed preparation in one background thread, with one consuming
  thread owning the sequential `EngineSession`. The background thread never
  invokes the engine or commits coverage.

`--ready-chunks 2` reserves at most three chunks: one active consumer chunk
plus two ready/in-flight chunks. Each chunk is limited to 8 MiB of canonical
serialized payload/packet bytes and the existing 250-million total coefficient
allowance. These are explicit finite reservations, **not** a host RSS bound.
Native packet/per-patch guards remain 50 million/10 million coefficient points.
The queue reserves before preparation and checks actual size before delivery.
Pool calls have a shared finite trial deadline; shutdown is cooperative and
can wait for that bounded callback, not interrupt an arbitrary Python function.

## Exactness and recovery

Every timed trial prepares fresh tasks. The comparison checks ordered patch IDs,
canonical per-patch certificates, geometry and packet hashes, coefficient counts,
and exact hit sets. Response field types are checked before the existing native
complete-count and exact Python-integer decoder. Truncated/tampered plans fail
before engine work. Sphere/guarded patches fail the experiment explicitly and
are never counted as completed coverage; the production fallback is unchanged.

Trial identity includes the exact source/binary fingerprint. Batch records keep
trial, coordinator, full shell/range, batch and packet identity. Patch IDs alone
are shell-relative and native IDs are packet-local, so neither is used as a
global routing key. Disjoint partition and global-patch audit helpers are tested,
but a two-coordinator broker is **not implemented**.

Only the single journal owner can advance a contiguous prefix after full exact
verification. Its journal and atomic fsynced checkpoint live in a new trial
folder. Recovery verifies the hash chain, cursor and totals; uncommitted suffixes
are preserved and replayed. A failed durable write poisons that instance: it
must close and reopen to reconcile an uncertain replace/fsync outcome. A closed
instance cannot write behind another owner's lock. Ahead-prepared work has no
coverage effect. Selected windows never confer a new full-box bound.

## Local reproduction

Use Python 3.12 with the unchanged pins checked by `scaling_core.initialize`:
SymPy 1.14.0, fpylll 0.6.4, cysignals 1.12.5, NumPy 2.3.5 and gmpy2 2.2.2.
Install dependencies only in an isolated scratch environment, not on ADA's
running environment. Set `SCALING_LATTICE_SOURCE` to this checkout's
`lattice_prototype` and make `lattice_gpu` importable on `PYTHONPATH`.

```sh
cd lattice_gpu
make -f scaling.mk scaling-host
make bin/emulated bin/emulated-sanitized
SCALING_LATTICE_SOURCE="$PWD/../lattice_prototype" \
  python -m unittest discover -s tests -v
python coordinator_benchmark.py --output /new/scratch/cpu-window \
  --lo 8192 --hi 16383 --first 307 --patches 512 \
  --workers 4 --engine-threads 1 --repeats 5 --max-seconds 60
python coordinator_diagnostics.py --output /new/scratch/diagnostics
```

The output directory must not exist. All coordinator/worker/CPU-engine processes
share the recorded affinity set. This is not a verified physical-core topology
or the required ADA 1×16 versus 2×8 comparison. Startup waits until every worker
reports its identity and is separate from steady state; shutdown and total trial
time are also recorded. Warm-up and profiling are outside performance trials.
Modes rotate between repeats; five repeats are not fully position-balanced for
four modes. Queue reservations, parent/thread CPU, per-task worker CPU/wall,
assembly/hash/encoding, RPC, exact decode and durable-commit timings are recorded.
Overlapping stage sums are not advertised as total wall time.

For selected high-range CPU validation, the ordinary native header still caps
bases at 10^11. In another scratch directory, copy the source and the already
published `running-overlay/src/kernel.hpp`, build a separate CPU engine, and
verify its arithmetic first. Point `--engine` at that binary and use `--lo
100000000001 --hi 200000000000 --first 3751385984 --patches 1024 --bits 222`.
Alternatively `--host-only` tests fresh preparation without engine work or a
completed-coverage claim. No source guard is rewritten by this program.

## Still required before production

Actual CUDA comparisons, 1×16 and 2×8 controlled trials on ADA, post-run
representative early/middle/late/high-cost windows, 30–60-second calibrated
trials, GPU event/utilization metrics, observed peak RSS/device memory, measured
broker/IPC transport overhead, and a production-safe lease-aware launcher are
pending. No device buffering, pinned memory or asynchronous transfer is added.
The experiment is a reviewable local candidate, not a production recommendation.
