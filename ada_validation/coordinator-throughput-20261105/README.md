# Coordinator and GPU pipeline investigation

Status: **plan for after the overnight run; no benchmark or automatic launch scheduled**.
Requested by Dot via Paul on November 5, 2026. The active search, its source,
configuration, service, checkpoints and publisher remain unchanged.

## Question and existing evidence

Dot observed PID 42468 at roughly 72% of one CPU, its 16 workers at roughly
25% each, and light GPU use. These are reported observations, not controlled
benchmark measurements. Packing/hashing/verification is a hypothesis.

Source inspection confirms that each chunk completes preparation, certification,
assembly, GPU requests, exact output verification, geometry hashing and a durable
checkpoint before the next chunk starts. Pool maps introduce stage barriers.
The GPU process already persists and reuses buffers. A prepared-frame queue and
device-resident buffering are additional features, not existing behavior.

A read-only snapshot of the last 256 committed records at
2026-11-05T23:42:10.530696+00:00 found 254 ordinary records after excluding
CPU audit, sphere fallback and guarded cases. Their recorded processing time was
60.963167 s; summed native GPU RPC wall time was 0.155186 s
(**0.255%**). Median ordinary chunk processing was
0.238719 s.
The preserved records and recomputable values are in
[passive-chunks.jsonl](passive-chunks.jsonl) and
[passive-observation.json](passive-observation.json).

This does not measure GPU utilization or identify which host operation limits
throughput. Chunk timing excludes checkpoint serialization/write/fsync. RPC wall
time includes transfers and delivery. Hiding GPU wait alone has little exposed
time to hide in this sample; overlapping CPU stages, improving load balance or
using a second Python coordinator could have a different effect. Measure them.

## Preserve the overnight search

Do not alter or restart the active service or attach an intrusive profiler.
Do not edit its root launchers: the publisher rereads those files later.
After its 9:00 a.m. Central deadline, verify that the search and final publisher
have exited and acquire the normal CPU/GPU leases. Work only in a new scratch
directory copied from the frozen validated workspace. Defer if production is
busy. An initial one-hour experimental cap bounds the investigation.

## Diagnose before optimizing

Instrument a scratch copy. Time specification generation; each pool map;
preparation and certification inside workers; assembly/canonical hashing/packet
encoding; broker queue wait; GPU request/upload/kernel time; exact output
verification; geometry hashing; and checkpoint JSON/write/fsync. Measure both
wall and CPU time where possible. Collect worker task-duration distributions,
stragglers, coordinator CPU and IPC/pickle costs. A separate short profiler run
may locate hotspots; exclude its timings from performance trials.

## Compare fixed work

| Mode | Coordinators | Pool workers | GPU path |
|---|---:|---:|---|
| Current baseline | 1 | 16 | Existing persistent engine, sequential chunks |
| Bounded pipeline | 1 | 16 | Certified chunks prepared ahead; one GPU owner |
| Multiple coordinators | 2 | 8 each | Disjoint ranges; one shared GPU owner/broker |

Keep all coordinators, workers, the broker and monitoring within the same
16-physical-core allocation. Give the two coordinators disjoint eight-core
affinities and record all affinity/CPU-budget settings. Include broker and
coordinator CPU usage in resource totals. Keep width 8, precision, exact arithmetic,
modular/coverage checks, packet limits and checkpoint policy identical. Start
with the current 256-patch chunk size and record total in-flight work.

Choose deterministic representative windows from the completed overnight
records: early, middle and late, including a documented higher-cost window.
Record selection rules and fallback/guard cases; do not silently select only
easy work. Calibrate window lengths once to roughly 30–60 seconds for the
baseline, then freeze the same patch IDs for every mode. Generate and certify
fresh tasks for every timed search; this is not a prepared-geometry reuse test.
Run five counterbalanced repeats with no simultaneous benchmark variants.

For each window [start, stop), the single coordinator gets the whole interval;
the two get [start, split) and [split, stop). Use a synchronized start and finish
at the last completion. Aggregate throughput is verified union patches divided
by that wall interval, never a sum of individual rates or suite totals.
Report startup/shutdown separately from steady-state and include actual total
trial time. Schedule CPU/CUDA audits by global patch IDs so the modes audit the
same work. Preserve independent outputs, journals, checkpoints and timing logs
for each coordinator and repetition.

## Queue useful GPU work safely

Use one persistent GPU-process owner. Each request/reply must carry trial,
coordinator, range and batch identity. Serialize ownership of the existing
EngineSession; it cannot accept concurrent callers safely. Bound queue depth,
bytes, coefficient points and outstanding replies. Start with two ready chunks
and compare measured starvation/backpressure; tune depth only in separately
reported trials. Preserve native per-patch/packet and candidate-output guards.
Preparation ahead of a checkpoint must not advance committed coverage.
On stop/failure, uncommitted queued tasks are replayed from the last checkpoint.

Measure a one-coordinator broker control if needed to quantify broker IPC cost.
If two coordinators improve throughput, test whether a larger single-coordinator
batch or CPU-stage pipelining explains the gain before adding production
complexity. GPU memory capacity alone is not throughput: aim to keep certified
work available whenever the GPU can consume it. Host-ready queues and actual
GPU-resident double buffering are separate changes. Device buffering, pinned
memory or asynchronous uploads require their own source snapshot, exact tests,
bounded memory allocation and measured gain before adoption.

## Correctness and reporting

Verify the partition manifest has exactly the baseline union, with no missing
or duplicate patch IDs. Compare per-patch canonical geometry/certificate
identities and coefficient counts across modes. Decode every response with the
existing complete-count and exact-integer checks. Match exact hit sets to the
serial reference, retain nonempty independent-oracle controls, and crosscheck
selected high-range packets on CPU. Guarded/incomplete patches are explicit
failures or gaps and cannot count as completed benchmark coverage. Test stale
replies, reordered completion, bounded-queue shutdown and checkpoint recovery.

Report aggregate patches/s and coefficient-points/s, wall time, repeat spread,
coordinator/worker/broker CPU use, GPU sampled utilization plus event-timed
kernel duty, stage timings, queue-empty/full time, peak host/GPU memory, failures
and contention. Sample utilization consistently in every mode; do not add
overlapping stage medians to invent a total. Compare CPU-stage overlap and GPU
waiting directly. Make a measured recommendation versus the best one-coordinator
configuration before any production change. No full-box bound follows from
these selected patch windows.

## Source and handoff

The [GPU source snapshot](../../lattice_gpu/) includes the launchers, native
engines, exact host checks, tests, publisher and docs. The [ADA tools](../../ada_tools/)
include the CPU benchmark/resource helpers required by those launchers.
The existing pinned `lattice_prototype/` remains a dependency. See
[HANDOFF.md](HANDOFF.md) and [source-manifest.json](source-manifest.json).
