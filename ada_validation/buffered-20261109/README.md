# Certified task caching and durable buffered search

This release resumes the existing fifth42 search using an in-process cache of
checked immutable task bytes, bounded ready queues, explicit pool dispatch sizes,
and an eight-record durable journal buffer. Each scientific receipt still covers
256 original width-8 cells. Only persisted records advance the checkpoint.

The native low64 kernel and exact lattice arithmetic are inherited from the
previous tested integration. The primary new runtime modules are
`worker/buffered_pipeline.py` and `worker/scheduling.py`; the concrete integration
is in `worker/packed_worker.py`. Per-host policies and configurations must retain
their own parent lineage, reservations, device guards and resource leases.

Selected settings are 16 physical preparation workers, group2/dispatch8 on Ada,
and current group4/dispatch4 on Boole and Cabbage. Preparation remains one window
at a time and GPU requests retain their existing format. Local durable journals
replicate captured verified prefixes to the bulk export every minute.

Five-repeat held-out trials on Ada measured 1.254x, 1.294x and 1.320x throughput
relative to the earlier combined local-journal pipeline, on Ada, current Boole,
and Cabbage representative strips respectively. These are input-region tests on
Ada, rather than timings measured on the peer hardware. All exact task/certificate/
packet signatures, native counts and candidate sets matched. Timing includes
final journal drain; RAM-only results are explicitly volatile comparisons.

`results/` contains every timing sample, summaries, correctness results and actual
finite/signal/deadline service tests. `experiments/` contains the tested alternatives
and reproduction scripts. Run the selected tests with the pinned Python 3.12
environment and the supplied worker layout. The existing per-host CPU/GPU resource
guard must cover GPU tests. Set `SCALING_LATTICE_SOURCE` to the staged lattice source.

The actually compiled native source is `worker/native-baseline/src/scaling_gpu.cu`
and its local `kernel.hpp` (SHA256
`3715d7636b404e172371a3828c2b7f112de8351d0b1c7b53c0f36f75fe2a9def`).
The independent reference is `worker/independent/gmp_reference.cpp`. Reuse a matching
validated host binary or rebuild with that host's already validated toolchain.
Ada used CUDA 13.4, g++13 and sm_86. The release manifest records the actual binary
hashes; compiled binaries are distributed in the private checksummed NFS bundle.

For an upgrade, follow `UPGRADE_COMMON.txt` and the node-specific handoff. Stop the
current owner cleanly, audit/seal its actual final prefix, and create a fresh run
under the unchanged original reservation. Never substitute a wider grid's IDs or
claim RAM buffers as committed coverage.

Today's production deadline remains 2026-11-09 17:00 America/Chicago. The independent
compute stop begins ten seconds earlier; separate final-copy cleanup may continue
after computation stops.
