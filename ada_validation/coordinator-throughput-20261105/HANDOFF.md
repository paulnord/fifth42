# Handoff for Dot — November 5, 2026

Tonight's search remains running unchanged. Its live status and 15-minute
updates are [here](../overnight-20261105/STATUS.md). It stops at 9:00 a.m.
Central on November 6. It searches selected patches with
100,000,000,001 <= c <= 200,000,000,000, near ratio a/c=0.3, using width 8,
256-patch chunks, 16 CPU workers and a persistent CUDA engine. These selected
patches do not establish a new full-box bound.

For tomorrow, review [the experiment plan](README.md): first profile host
stages in a scratch copy; then compare 1x16, 1x16 with bounded prefetch, and 2x8
over identical patches. Keep one GPU owner, use disjoint ranges/checkpoints,
and verify the full selected patch union and exact results before making a
production recommendation. No follow-up experiment is scheduled or running.

The passive evidence snapshot found 0.255% of recorded ordinary chunk
processing time in GPU RPCs. This is not GPU utilization and does not identify
the CPU hotspot. It motivates measuring IPC, serial work and worker barriers
alongside CPU/GPU overlap.

All GPU source and tests are copied byte-for-byte into `lattice_gpu/`; CPU
resource/benchmark/publication helpers are in `ada_tools/`. The original
`lattice_prototype/` dependency is already on this branch. Source files include
ADA-specific absolute paths and pinned environments: this is a reproducible
review snapshot, not an automatic deployment. Do not copy it over the active
ADA launchers, publisher, source or checkpoints while tonight's job is active.

The running scratch kernel differs from the root source only in the documented
native base guard from 10^11 to 2*10^11. Its exact header is retained in
`running-overlay/src/kernel.hpp`, with the CPU/sanitized/CUDA arithmetic
validation report. The launcher creates and validates that isolated copy.
The live runner source identity is `b4a14a719e28452488c01ea05dddf8121df6a3c5ff0c1521bb490a3f7be844d3`.
The latest local host suite passed 29 tests before the overnight launch.
The width experiment passed 80 timed CPU/CUDA observations. Its results are
[here](../lattice-width-20261105/README.md).

Only source, docs, manifests and the bounded read-only evidence sample are
published. Deployment authentication stays on ADA. No current service,
search setting, checkpoint or production source was changed for this handoff.
