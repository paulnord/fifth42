# Tested preparation upgrade, 10 November 2026

This release adds bounded preparation across16 original windows and optional GPU lattice proposals. Original native GPU requests, exact CPU certificates, grouped coverage records, local durable journals, NFS ownership locks, verified60-second replicas and final copies remain in place.

On Cabbage's actual stopped frontier1,538,849,024,18 balanced finite trials with the actual production enumeration binary measured median logical cells/s:

| Setting | Rate |
| --- | ---: |
| Group4, CPU preparation, one window (old) |23,899|
| Group4, CPU preparation,16 windows |23,785|
| Group4, GPU preparation,16 windows |25,465|
| Group8, CPU preparation, one window |42,271|
| Group8, CPU preparation,16 windows (selected) |47,102|
| Group8, GPU preparation,16 windows |47,433|

The selected setting is about97% faster than the old setting in these finite trials. GPU preparation did not show a consistent extra gain here. Each mode had three32,768-cell trials, exact native count/hit checks, independent first-window GMP audit and final durable flush. Startup and final journal audit were excluded. These preliminary timings are not an overnight production-rate guarantee. Other regions/hardware can prefer different choices; previous27-trial results and the root prototypes remain in `experiments/gpu-preparation-20261110` on this branch.

Cabbage's full stopped parent passed all166,706 receipt checks and1,303 saved GMP audits, with both2,991,510,848-byte journal hashes verified. It is sealed at cursor1,538,849,024 under the existing [500,000,000,2,250,000,000) reservation. The new continuation never imports TEST_ONLY benchmark coverage.

Actual-release acceptance passed CPU and GPU finite17-window runs, an actual graceful service stop, and an actual independent deadline timer. Every case used the original ownership/GPU leases, local durable journals and NFS replicas. Final buffers drained; both copies passed the unchanged journal audit; checkpoint bytes matched; leases released and output reuse was refused. Additional checks:25 controller regressions,14 policy tests,7 preparation contracts,3 frozen-template/rotation tests. Full test results/logs, initial policy type failures, matched timing samples and retained-journal hashes are included.

The controller fix waits for inactive+MainPID0 before reading the final supervisor, requires complete clean final reports and a checkpoint-matching verified replica, and persists stop intent before stopping a worker. It prevents automatic retry after manual/error stops. This continuation marks the original pending reservation consumed, so finishing the current reservation cannot replay it. Rotation copies the upgraded immutable template and preserves selected settings; new allocations still require the existing atomic NFS ownership allocator.

The authorized hard stop is **11 November2026,17:00 America/Chicago**, epoch1794438000. Independent stop timers fire ten seconds earlier,2026-11-11 22:59:50UTC. Installers must retire old November10 timers before rebinding active configurations. Final-copy services may finish after compute stops.

Read `HANDOFF_ADA.txt` or `HANDOFF_BOOLE.txt` and `INSTALL_COMMON.txt`. They preserve each host's own actual checkpoint, original ownership and host/resource policies. `source.tar.gz` is the exact complete Cabbage runtime, including sources, headers, small tested binaries, frozen configurations and manifests. Its Cabbage policy/configuration is not a peer host configuration. `common-changes.patch` applies the shared source changes to a fresh copy of the current worker; it was checked against the actual Cabbage baseline with zero patch fuzz. A differing peer baseline must resolve/review its own merge, then pass the supplied actual-release checks.

CPU preparation is the default and uses the existing native enumeration binary. Optional GPU preparation requires a host-specific build of `gpu_candidate/gpu_lll.cu` and must pass exact native/GMP/nonempty gates first. No adaptive Newton root path is enabled in production because its complete request+proof path lost to GMP.

Wait for the shared `READY.json` before installation:
`/mnt/nfs_share/fifth42-integration-20261109/combined/preparation-r1-20261110/READY.json`.
It records the immutable source commit, source archive and manifests. `STATUS.json` alone is not a completion marker.
