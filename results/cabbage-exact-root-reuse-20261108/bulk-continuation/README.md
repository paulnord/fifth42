# Cabbage bulk-disk continuation — 2026-11-08

**Fresh continuation running on `/mnt/fifth42-storage` with a 128 GiB per-run journal cap. The original reservation and Monday deadline are unchanged. Original parent bytes remain in place. Ada’s separate new publisher first push/readback is pending at this report snapshot.**

## Identity and lineage

- New run: `cabbage-bulk-20261108T234202Z`; new first patch **2263483008**.
- Original claim: `364221db0023ea69fa18b47eb512e9e83362f6d598fc19c101e74b72f4f3d1c8`, interval `[2250000000,3000000000)`, original reservation manifest `a0000b2ed70ea7566baa2c6c0a00bd8cdcbc726f53bdf1247b7b9587eb5d6932`. No new claim was created and no interval was reassigned.
- New frozen manifest: `8d54cb2f5d455e54c8c0ba423be59ec548bb46a4ef824e98c1717ae793d0d8ff`; config: `d9a162f6268a0bfcd710a9fc324ff1bdd45e7ead3873d12723d5ceec01c8e503`. All mathematical Python sources, finite-range native sources, and native binaries remain byte-identical to the prior tested candidate.
- Deadline remains **2026-11-09 09:00 America/Chicago**, with independent cleanup timer at 08:59:50. Nice19, 16 distinct physical CPUs, one GPU owner, minimum 8 GiB free reserve, no automatic restart/resume.
- Fresh output: `/mnt/fifth42-storage/runs/cabbage-saved-root-20261108T222040Z/cabbage-bulk-20261108T234202Z/run`. Coordinator and original exclusive job-owner POSIX lock remain on `/mnt/nfs_share/fifth42-shared-20261107`.
- Both actual Ada/Cabbage probes passed on the new export, with matching final checkpoint hash and lock inode. The exact bulk guard is pinned by SHA-256 `83c383b56a8489c7b451158f001c7713c0a430d6ad1afb9bcd263b5a1af4afcf`.

## Parent stop incident and recovery

The old unit used `KillMode=control-group`, which sent SIGTERM to preparation workers as well as the supervisor. The requested stop hit its eight-second timeout and systemd killed the remaining owned processes. The old status/supervisor records are stale; they were preserved verbatim and are **not presented as a clean stop**. No other host’s worker/service was stopped or changed.

The stopped parent was independently shown to be physically quiescent: MainPID=0, no CUDA compute processes, and both the original coordinator-owner lock and local GPU lease could be acquired. The journal’s exact length matched the committed checkpoint. A full streaming audit then reconciled every receipt hash, ordered patch interval, expected/visited native count, checkpoint total, hit record and saved periodic GMP receipt. No uncommitted suffix, missing interval or duplicate commit was found.

- Verified parent interval: `[2250000000,2263483008)`; **52,668 chunks**, **13,483,008 patches**, **412 GMP-audited chunks**.
- Raw journal bytes: **1,862,903,610**; SHA-256 `a6f7145e5868960137f4a7418132b7e9e0ec04b5cbe58fcfe2af9ce3b432e8d5`.
- Final checkpoint SHA-256: `fe2f8aff7a849f49490cbcfe26c8310cb4143d449b42ac6a793ed476323fb22b`; journal chain `2d1eadc05a4c74f0c2eae2481a1bae32bb40f548731cde805d8e1ff53fe2b7c8`.
- Readback-verified final archive: `/mnt/fifth42-storage/archives/CABBAGE-FINAL-20261108T233823Z`. It includes the journal, checkpoint, original stale status/supervisor, config, source manifest, controls, worker affinities, all GMP receipts, the original runtime review archive, full audit and quiescence receipt.
- A separately pinned recovery acceptance explicitly records the timeout and binds the exact archive/checkpoint/raw hashes. It permits a fresh writer only after all durable bytes and physical ownership are verified. Missing quiescence, changed bytes, gaps/overlaps, wrong original claims, wrong mounts and incomplete recovery checks reject. Original journal/status/config/source bytes were not edited, truncated or moved.

## Stop fix and actual validation

The new units use **`KillMode=mixed`**: systemd sends the initial termination signal to the supervisor, allowing it to stop its worker/pool gracefully, while retaining whole-cgroup forced cleanup if needed. An actual systemd regression test confirmed the child stayed alive long enough for protocol-driven shutdown; no direct group SIGTERM reached it.

Six continuation-policy test groups passed. Actual new-disk worker/supervisor tests used systemd units with the corrected stop mode, actual CUDA, nonempty exhaustive controls, independent GMP count/full-record checks, fresh TEST_ONLY journals and the original owner lock. No new production reservations were made for tests.

| Case | Chunks | Coefficient points | GMP-audited chunks | Result |
|---|---:|---:|---:|---|
| finite | 2 | 331480 | 1 | Bounded integration chunks completed |
| signal | 2 | 331480 | 1 | Stop requested |
| deadline | 115 | 19206978 | 1 | Stop requested |

Every case verified owned-process exit before its test deadline, GPU/owner lease release and exact journal-chain reconciliation. Reusing an existing output was rejected without modifying its checkpoint. Test enumeration is not production coverage.

The first production bootstrap attempt found a missing supervisor output-parent directory and exited before creating a journal. The parent directory was then created through the verified mount guard; the same frozen config started with no prior output reuse. This setup retry did not change the manifest, config, claim or first patch.

## Initial running evidence

A read-only audit of the first new committed prefix `[ 2263483008, 2263483264 )` passed its hash chain, complete native counts, GMP receipt, controls and 16-worker affinities. The parent/new boundary is exactly contiguous. Worker, collector and independent deadline timer were active; linger was enabled. Subsequent collector snapshots showed advancement without alerts.

The new collector and identity-pinned publication inputs are at `/mnt/nfs_share/cabbage-bulk-publishing-20261108/`. Ada’s publisher must match the ledger’s original identity to `reservation_manifest_sha256`, then bind the new manifest/config, parent audit/archive/recovery evidence and new source identity. Its first push/readback remains the separate Ada-side reporting step at this snapshot.

## Retained evidence and limitations

- [Cutover status](CUTOVER_STATUS.json), [frozen identity](frozen-identity.json), [config](production-config.json), [source manifest](worker/cabbage-release-manifest.json), [policy](worker/policy.py), [supervisor](worker/cabbage_supervisor.py).
- [Parent full audit](parent-audit.json), [archive receipt](parent-archive-receipt.json), [physical quiescence receipt](QUIESCENCE_RECEIPT.json), [pinned recovery acceptance](worker/recovery-acceptance.json).
- [Actual runtime/systemd validation](runtime-validation.json), [policy tests](policy-tests.txt), [systemd stop regression](stop-test/result.json), [initial live-prefix audit](live-prefix-audit.json).
- Runtime/dependencies and native toolchain are unchanged from the [earlier Cabbage report](../readiness/README.md): Python 3.12.16 with the exact Sympy/fpylll/cysignals/numpy/gmpy2 pins, CUDA 13.2.78, g++-13 13.4.0, RTX 3060.
- This is a dated handoff snapshot. Only the verified parent and initial fresh prefix are reported; the reserved interval is incomplete and no full-shell/full-box result is claimed. The parent audit reconciles durable receipts and saved periodic GMP checks, without re-enumerating every coefficient box.
- Raw journals, compiled binaries and large archives remain on the retained source/new disk. No original parent retirement is authorized by this report. [SHA256SUMS](SHA256SUMS) covers the published text evidence.
