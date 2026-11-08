# Cabbage admission preparation — 2026-11-08

**Local compute, actual NFS and staged-worker checks passed. Production admission is pending: the coordinated cross-host probe was interrupted by unrelated CPU work. No production claim, launch or new production coverage.**

This continues the [initial report](../README.md) and [CUDA follow-up](../followup/README.md). Ada supplied `/mnt/nfs_share/cabbage-admission-20261108/JOIN.txt`, proposing the half-open interval **[2,250,000,000, 3,000,000,000)** and an initial **2 GiB journal cap**. Those remain proposals; the production ledger was not inspected or changed in this session.

## Completed checks

- Cabbage was idle before each stage: RTX 3060, no CUDA compute process, 16 physical / 32 logical Ryzen 5950X CPUs, about 120 GiB available RAM. All compute stages used the same pinned Python 3.12.16 and exact dependencies/toolchain recorded in the previous report. External resource monitoring remained active.
- Finished the five missing higher-cost baseline/candidate GPU timing pairs in fresh directories. All packet/task/certificate/geometry signatures, expected/visited counts, full native candidate records, decoded exact hit sets, first-chunk GMP hit audits and local durable journal recovery matched. Together with the ten earlier complete pairs, the planned **15 pairs / 30 GPU trials** are complete across two idle sessions. The old interrupted pair and its unpaired sample are excluded.
- Actual NFSv4 mount verified as `ada:/mnt/nfs_share` on `/mnt/nfs_share`, `local_lock=none`. Fresh TEST_ONLY directories only. Baseline/candidate real GPU counts, certificates and hits matched GMP and each other. Nonempty exhaustive controls passed. Reservation overlap, immutable identities, server-coherent interprocess POSIX lock exclusion, stable inode preservation, own lock-holder death/release, durable chunk roll-forward, incomplete append preservation/recovery, changed identities, incomplete counts and journal tampering were exercised.
- The initial NFS harness attempt used different receipt/journal trial labels. The existing journal guard rejected that harness setup before committing. A corrected harness used a new `_v2` namespace and passed. No mathematical baseline/candidate discrepancy occurred; both attempts are retained.
- Verified all six Ada admission-package hashes and all 186 portable-source content hashes. Archive SHA-256: `ada1389682daa5265c0602f731dd312d354b33e6508645db4481c2c98ea5f455`. Verified the Store allocator AST is unchanged. Ada's supplied seven-check report includes mocked Cabbage tests; it is not substituted for actual client checks.
- Staged a new actual Cabbage worker/supervisor derivative using the saved-root candidate, the finite-200-billion native overlay, the **exact Ada admission adapter** `8bc5556a99ee12ffbd7a5bcce9569b22b2af479706b26f5a2b3067fe9a9a61e9`, 16 distinct physical CPUs 0–15, nice19, a 2 GiB journal cap and 8 GiB minimum shared free-space reserve. Policy/supervisor derive from the archived Boole worker with Cabbage identity, interval and fresh-allocation metadata; no historical production config or journal was reused.
- The actual staged worker passed real start/middle/end samples in the proposed interval, nonempty controls on every run, independent GMP count/full-record audits, journal-chain/count/cursor reconciliation, SIGTERM stop, absolute-deadline stop, own-process cleanup and lease release before the deadline. Policy rejected oversized journal caps, automatic resume, invalid geometry/ranges/CPU lists and expired deadlines.

## Remaining timing samples

These are steady pipeline seconds, including host preparation/certification, persistent CUDA execution, exact verification, first-chunk GMP audit and local durable commits. Startup/shutdown are separate in [results.json](remaining-gpu/results.json). These short samples do not establish production speedup or a kernel improvement.

| Higher-cost window | Five raw steady samples (s) | Median (s) |
|---|---|---|
| baseline | 0.859651038, 0.851633471, 0.881940042, 0.853880722, 0.850988652 | 0.853880722 |
| candidate | 0.842907677, 0.837701300, 0.837018780, 0.842407690, 0.846567315 | 0.842407690 |

Median pipeline throughput ratio: **1.013619x** (about 1.4%). The two earlier windows measured 1.033958x and 1.037110x. Do not combine or multiply these ratios. Raw per-trial kernel/engine/RPC times are retained; the kernel is unchanged and short-event timing varies.

## Actual staged-worker runs

All runs used separate TEST_ONLY NFS ledgers and fresh journals. Test enumeration does not enter production totals.

| Run | Half-open committed patch interval | Chunks | Coefficient points | GMP-audited chunks | Stop reason |
|---|---|---:|---:|---:|---|
| start | [2250000000, 2250000512) | 2 | 333200 | 1 | Bounded integration chunks completed |
| middle | [2625000000, 2625000512) | 2 | 469604 | 1 | Bounded integration chunks completed |
| end | [2999999488, 3000000000) | 2 | 646714 | 1 | Bounded integration chunks completed |
| signal | [2625000000, 2625001024) | 4 | 944484 | 1 | Stop requested |
| deadline | [2625000000, 2625025856) | 101 | 23728906 | 1 | Absolute deadline reached; final cleanup |

[runtime-acceptance-results.json](runtime-acceptance-results.json) retains control hits, stop attribution and the supervisor's all-owned-processes-exited timestamps. No automatic resume/restart or publisher was started.

## Cross-host probe: incomplete

The user confirmed Ada's matching probe was running. Cabbage joined with Ada's exact `protocol_probe.py cabbage`, exact static adapter and actual hostname/mount guard. It used only `/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/ledger` with synthetic zero-point records. This is storage/protocol testing, not mathematical validation.

At **51.525 seconds**, the resource monitor detected unrelated Java PIDs 330463 and 330468 using about **2.63 and 2.72 CPU cores**. It terminated Cabbage's test group immediately, leaving those processes and Ada's processes untouched. Handshake evidence reached mutual owner-exclusion/recovery stages, but neither complete result file was available: **no cross-host PASS is claimed**. The user was told Ada's peer had exited. The failed/incomplete probe directory is preserved and was not retried.

A fresh version is prepared, **not executed**, at:

```text
/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk/readiness-handoff/probe-v2-package/
```

The new probe changes only ROOT to a fresh child namespace. Its actual-role, mount, static adapter, locking and recovery checks remain unchanged. [PREPARED.json](probe-v2-package/PREPARED.json) provides both Ada/Cabbage commands and hashes. Both real hosts must run it in a coordinated idle window; both results must PASS. No remote Ada or Boole command was started from Cabbage.

## Frozen candidate and launch intent

- Tested source/binary manifest: **`a0000b2ed70ea7566baa2c6c0a00bd8cdcbc726f53bdf1247b7b9587eb5d6932`**, covering 149 files. [Manifest](cabbage-runtime/cabbage-release-manifest.json), [Cabbage policy](cabbage-runtime/policy.py), [supervisor](cabbage-runtime/cabbage_supervisor.py), [actual adapter](cabbage-runtime/ada_export_store.py) and [worker](cabbage-runtime/packed_worker.py) are available for review.
- Local candidate archive: `/home/pnord/scratch/saved-root-readiness-Ija5nMHk/cabbage-candidate-review-20261108.tar.gz`. It contains only the exact manifested sources/binaries and manifest, excluding test journals/configs/leases. Archive SHA-256: `e77c60eaff23ce103a1c5ef47930d802d2440c3e7bd19793163cbcd8a31f5b4e`.
- A shared copy, checksums, readiness evidence and launch intent are at `/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk/readiness-handoff/` for Ada's owner to review.
- [LAUNCH-INTENT.json](LAUNCH-INTENT.json) proposes a fresh job and journal for the proposed interval, a fixed Monday 2026-11-09 09:00 America/Chicago deadline, cleanup at 08:59:50, an independent deadline timer, Restart=no, no automatic resume, one GPU owner and a separate `cabbage_validation/production-20261108` publisher path. It is not a runnable approved production config.
- `loginctl show-user pnord -p Linger` returned **Linger=no**. Linger must be enabled and verified at authorized admission before relying on logout-independent user services. No linger setting or service was changed.

Before launch: complete the fresh cross-host probe; obtain explicit launch authorization; refresh disjoint common-ledger allocation and aggregate disk headroom without changing other jobs' caps; create the final immutable config/claim/collector identity; enable/verify Cabbage linger and a new service/deadline timer; and have Ada's owner verify the separate publisher's first push/readback and 15-minute cadence. A production claim, current storage reservation and final production config do not yet exist.

## Commands and evidence

Working directory was `/home/pnord/scratch/saved-root-readiness-Ija5nMHk`. The interpreter was `/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python`. Each monitored stage invoked the retained `resource_runner.py` from the prior follow-up, with ~0.5-second resource sampling and finite stage/request budgets.

```sh
# Previously pinned comparison sources/engine; five fresh missing pairs:
python resource_runner.py remaining-gpu python remaining_gpu.py
# New private NFS namespace, actual GPU/GMP output, fault/recovery checks:
python prepare_review.py
python resource_runner.py nfs-acceptance-v2 timeout 240 python -B nfs_acceptance.py
# Verified portable bundle; frozen Cabbage derivative; actual staged worker:
python -B prepare_runtime.py
python resource_runner.py runtime-acceptance timeout 180 python -B runtime_acceptance.py
# Coordinated peer; interrupted by resource conflict, not retried:
python resource_runner.py cross-host-probe timeout 590 python -B /mnt/nfs_share/cabbage-admission-20261108/protocol_probe.py cabbage
python -B seal_readiness.py
loginctl show-user pnord -p Linger
python -B prepare_probe_v2.py
```

The exact resolved commands, exit status and wall times are in `*-execution.json` or `*-failure.json`; stdout and complete resource traces are retained alongside them. Tests wrote only into newly created TEST_ONLY namespaces. Production code, services, journals, checkpoints, shared reservations and existing storage caps were not changed. No cross-host failover/reboot claim is made.

[CABBAGE_READINESS.json](CABBAGE_READINESS.json) is the machine-readable status. [publication-manifest.json](publication-manifest.json) records copied/original file identities; [SHA256SUMS](SHA256SUMS) covers every published evidence file. Full raw test journals, per-worker stage arrays, binaries and toolkits remain in the local/shared test artifacts. The two NFS result JSONs retain every value with whitespace compacted for the repository.
