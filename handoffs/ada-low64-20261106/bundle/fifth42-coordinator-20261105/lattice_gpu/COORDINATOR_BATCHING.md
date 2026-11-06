# Larger packets without losing patch identity

Paul's additional question is whether tiny GPU calls leave the device underfed.
`coordinator_batching.py` and the CPU-only `coordinator_batch_sweep.py` prepare
that experiment without changing ADA's running engine or publisher.

The native engine already receives contiguous arrays of exact task transforms
and coefficient-range descriptors. It enumerates candidate coefficients on the
GPU. Building every coefficient value on the CPU would add expansion, memory
traffic and transfers; the implemented candidate instead coalesces many existing
certified task descriptors into the same native packet. This leaves arithmetic,
enumeration order within a task and all native guards unchanged.

The sweep holds the selected 4,096-patch union fixed and tests task ceilings of
256, 512, 1,024, 2,048 and 4,096. It regenerates and certifies every task for each
trial. It never exceeds 4,096 descriptors, 50 million coefficient points or the
16 MiB payload frame allowance per packet. A smaller configured byte/point
limit splits packets; an impossible single task fails. The ready work is bounded
at 4,096 patches and 128 MiB of canonical serialized payload/packet bytes. That
bound is not a claim about Python RSS.

Routes preserve full source-window identity, chunk index, patch ID, certificate
and point count for every packet-local native ID. Combined replies are checked
for complete native counts and exact hits, then routed and decoded through the
same host checks for each original chunk. Checkpoints still commit in original
256-patch intervals; coalescing does not silently weaken checkpoint frequency or
advance coverage before all associated work verifies.

The local command is deliberately CPU-only. Use a separately built and validated
high-range scratch CPU engine with the committed running-overlay header:

```sh
python lattice_gpu/coordinator_batch_sweep.py \
  --engine /scratch/validated-high-range/scaling_cpu \
  --output /new/scratch/batch-sweep --workers 4 --repeats 1
```

This is a diagnostic sweep, not a statistical GPU performance result. The local
report contains fresh-preparation, aggregation, RPC, native CPU engine, exact
host decode, per-chunk durable-commit and end-to-end times. The engine's aggregate
compute time is not called kernel time. Transfer and GPU kernel times are null,
not inferred from RPC subtraction.

## ADA measurement still required

Do not start while the overnight search or final publisher is running. After
both exit, the normal resource guard must grant CPU and GPU leases for a new
scratch-only experiment within the approved budget. Keep one engine owner.

For the same frozen patch union and each packet size:

1. Record actual tasks, coefficient points, descriptor bytes and packets. Keep
   per-patch geometry/certificate identity and original checkpoint boundaries.
2. Measure host preparation, packet assembly, queue starvation/backpressure,
   exact decode, durable commits, startup/shutdown and complete wall time.
3. Use the existing CUDA event-timed `kernel_seconds`. In a separately validated
   instrumentation copy, add explicit task/chunk upload and result/count download
   timings and byte counters, plus allocation/growth time. Do not call
   `RPC - kernel` transfer time: it also contains parsing, resets, synchronization,
   result encoding and host process communication. Synchronous host copy timers
   and device event timers measure different things and must be labeled.
4. Report sampled GPU utilization and event-timed kernel duty alongside complete
   verified patches/second. Five counterbalanced repeats and representative
   early/middle/late/high-cost windows remain required for a production decision.
5. Compare larger packets against the best single-coordinator one-pass host
   configuration. A fuller individual launch does not establish better complete
   throughput if waiting to fill the packet leaves the GPU idle longer.

No pinned-memory, asynchronous-copy, device double-buffering or multiple-GPU-owner
change is included. No CUDA build or execution was available in this local
workspace; transfer/kernel instrumentation has not been compiled or validated.
