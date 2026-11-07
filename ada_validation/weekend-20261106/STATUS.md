# ADA fifth-power weekend search

Last GitHub snapshot: **2026-11-07T21:03:44.522837+00:00**.
Search state: **running**. Worker status refreshed: **2026-11-07T21:03:35.718921+00:00**.

Started Friday, November 6, 2026 at 5:19:57 p.m. Central.
Stop deadline: **Monday, November 9 at 9:00 a.m. Central**.
The independent cleanup timer is **active/waiting**;
next firing: **Mon 2026-11-09 08:59:50 CST**.
The search runs as a systemd user service with login linger enabled.
Automatic restart/resume of the search is disabled.

| Measurement | Saved value |
|---|---:|
| New committed patches this weekend | 99,993,600 |
| New committed chunks | 390,600 |
| Next patch cursor | 3,912,959,616 |
| Cumulative selected patches including prior runs | 162,959,616 |
| Coefficient points this weekend | 234,205,467,840 |
| Average search throughput at worker status timestamp | 1,278.3 patches/s |
| Search elapsed at worker status timestamp | 21.73 hours |
| Recorded hits | 0 |
| Periodic independent GMP audits at worker status timestamp | 3,052 |
| Preparation pacing | 0.0 seconds |

Configuration: 16 workers pinned to physical CPUs 0–15, optimized packed/prefetched
preparation, one CUDA owner and journal writer, width 8, 222-bit geometry, cap 42,
denominators in [100000000001, 200000000000]. First and every 128th chunk receive
independent GMP checks. New work continues from cursor 3,812,966,016.

Coverage is **selected partial patch coverage**. No completed full-box bound is
claimed: `completed_bound` is null and `independent_oracle_verified_through` is 0.
Periodic GMP audits do not constitute an exhaustive oracle of the whole domain.

Alerts: **None reported**.
Worker reason: **None**. Worker error: **None**.
Supervisor error: **None**.
Worker/service stderr sizes: **0 / 0 bytes**.
Free disk: **174.8 GiB**;
available memory: **118.0 GiB**.

This separate publisher aims to update every 15 minutes and after the search
stops. The timestamp is the freshness indicator. It reads saved JSON and service
state; it does not audit the full coverage journal or certify new mathematics.
Checkpoint totals and the worker's ten-second status counters can differ slightly.
The frozen search's internal publication setting remains disabled; this separate
reporting service performs publication without changing the running search.
See [status.json](status.json) for the captured checkpoint, digest, service state,
audit timestamps, provenance and resource measurements.

[Previous overnight run](../overnight-20261105/STATUS.md).
