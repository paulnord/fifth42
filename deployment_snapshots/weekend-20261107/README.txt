WEEKEND SEARCH DEPLOYMENT SNAPSHOT — 2026-11-07

This directory preserves the exact running Ada and Boole implementations and
their deployment recipe. The live progress pages remain separate:
  ada_validation/weekend-20261106/STATUS.md
  boole_validation/precision-weekend-20261107/STATUS.md

Contents
  ada/worker/                  Exact 174-file Ada runtime and supporting checks
  ada/external-helpers/        Ada's pinned legacy resource helpers
  ada/systemd/                 Actual active user service/timer definitions
  ada/nfs/                     Active Ada export configuration snapshots
  boole/worker/                Exact 158-file Boole runtime
  boole/captured-package/      Boole's native build, setup and environment capture
  boole/evidence/              Launch, validation and configuration evidence
  reporting/ada/               Ada's independent GitHub publisher and tests
  reporting/boole-on-ada/      Actual Ada-hosted Boole publisher bridge
  boole/collector-and-reference/  Boole collector and original bridge reference
  protocol-and-validation/     Shared locking/allocator tests and reports
  shared/                     Reservation ledger snapshot, not a new allocation
  tools/                      Read-only coverage audit and backup tools

The deployed source manifest identities are:
  Ada:   a7aea624ca71a44aeff905976f944573b036e2f7a6b614dc79fdc4aed587dffe
  Boole: 5053fb4c9709d037b6119e2e5b639dcd6f1caa382f40749c8dcd995b0fcc882b

Both use adaptive outward geometry precision, exact reduction certificates and
native count/reconstruction checks, with independent periodic GMP audits. Cube
pruning is not enabled. Coverage is selected partial coverage; no full-box bound
is claimed. Test enumeration is excluded from production totals.

Historical deployed allocation, all half-open patch indices:
  Boole:          [3000000000, 3750000000)
  Verified prior: [3750000000, 3917103232)
  Ada:            [3917103232, 11250000001)
The common reservation ledger and stable POSIX owner locks prevent overlapping
allocations. Patch 0 remains unsupported/uncovered, not silently completed.

SHA256SUMS covers every archived file except itself. From this directory run:
  sha256sum -c SHA256SUMS

BACKUP_INVENTORY.json records the captured files and original paths. RESTORE.txt
describes the layout, runtime, locking, service and reporting dependencies.
The fixed Git tag for this snapshot is recorded in BACKUP_METADATA.json.

This is a code/setup backup. Private SSH keys, tokens, virtual environments,
caches, growing coverage journals and live lock files are excluded. Small
configuration, audit and checkpoint metadata are historical evidence; they do
not replace the original journals required to verify/resume completed coverage.
