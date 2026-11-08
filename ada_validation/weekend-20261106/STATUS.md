# ADA adaptive-precision weekend search

Last GitHub snapshot: **2026-11-08T05:33:33.725288+00:00**.
Search state: **running**. Worker status refreshed: **2026-11-08T05:33:30.457387+00:00**.

The original weekend search started Friday, November 6, 2026 at 5:19:57 p.m. Central.
This fresh adaptive-precision continuation starts at verified cursor **3,917,103,232**.
Current service active since: **Sat 2026-11-07 16:01:06 CST**.
Stop deadline: **Monday, November 9 at 9:00 a.m. Central**.
The independent cleanup timer is **active/waiting**;
next firing: **Mon 2026-11-09 08:59:50 CST**.
The search runs as a systemd user service with login linger enabled.
Automatic restart/resume of the search is disabled.

| Measurement | Saved value |
|---|---:|
| New committed patches in this continuation | 119,499,008 |
| New committed chunks in this continuation | 466,793 |
| Next patch cursor | 4,036,602,240 |
| Cumulative selected patches including prior runs | 286,602,240 |
| Coefficient points in this continuation | 301,282,067,850 |
| Average search throughput at worker status timestamp | 4,403.1 patches/s |
| Search elapsed at worker status timestamp | 7.54 hours |
| Recorded hits | 0 |
| Periodic independent GMP audits at worker status timestamp | 3,647 |
| Preparation pacing | 0.0 seconds |

Configuration: 16 workers pinned to physical CPUs 0–15, optimized packed/prefetched
preparation, one CUDA owner and journal writer, width 8, adaptive geometry, cap 42,
denominators in [100000000001, 200000000000]. Geometry uses the validated adaptive
precision policy with 222-bit fallback; actual per-patch precision is recorded in
the journal. Exact certificates, native bounds and residual checks are retained.
First and every 128th chunk receive independent GMP checks. The range reservation
and fresh journal use Ada's shared export. The original journal is preserved.

Matched short Ada tests measured **1,260.5 patches/s baseline** and
**4,135.5 adaptive**, a **3.28x** ratio,
including pipeline, journal and checkpoint costs. These selected trials do not
guarantee constant weekend throughput. Cube pruning is not enabled.

Coverage is **selected partial patch coverage**. No completed full-box bound is
claimed: `completed_bound` is null and `independent_oracle_verified_through` is 0.
Periodic GMP audits do not constitute an exhaustive oracle of the whole domain.

Alerts: **None reported**.
Worker reason: **None**. Worker error: **None**.
Supervisor error: **None**.
Worker/service stderr sizes: **0 / 0 bytes**.
Free disk: **145.1 GiB**;
available memory: **118.0 GiB**.

This separate publisher aims to update every 15 minutes and after the search
stops. The timestamp is the freshness indicator. It reads saved JSON and service
state; it does not audit the full coverage journal or certify new mathematics.
Checkpoint totals and the worker's ten-second status counters can differ slightly.
The frozen search's internal publication setting remains disabled; this separate
reporting service performs publication without changing the running search.
See [status.json](status.json) for the captured checkpoint, digest, service state,
audit timestamps, provenance and resource measurements.
The [verified handoff](precision/final-coverage.json),
[GPU validation](precision/gpu-validation-report.json), and
[frozen source manifest](precision/release-manifest.json) describe this continuation.
The [original run's final snapshot](precision/pre-precision-final.json) is preserved.

[Previous overnight run](../overnight-20261105/STATUS.md).
