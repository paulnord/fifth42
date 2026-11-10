Production source snapshot — 10 November 2026
===========================================

This snapshot adds the verified Boole delegated-queue handoff, all 67 queued
stage overlays, and the current/finished Boole and Cabbage successor sources,
configuration identities and validation evidence. It complements Ada's source
at ada_validation/suballocation-20261109 and the original combined snapshots
at ada_validation/overnight-20261109.

Boole's archive is stored as common source plus per-stage overlays. Reconstruct
a stage by copying boole/handoff/source/common, then applying the matching
boole/handoff/source/stages/<run_id> overlay. Preserve the stage's manifest and
configuration hashes. The controller source and frozen plan are in
boole/handoff/source/controller. Actual started runs also have independent
per-run snapshots under boole/runs.

Cabbage's controller, startup sources, tested first successor and handoff are
in cabbage/handoff. Its completed and current rotated runs have independent
source snapshots and exact manifests under cabbage/runs. Rotation does not
change the original logical grid or confer coverage on skipped intervals.

The source audit reads the nine delivered archives and verifies every declared
source/native hash against its manifest. It also checks each active publication
specification. Every regular UTF-8 source/evidence file is included; native
executables are omitted from Git and remain in the verified NFS archives.
source-audit.json lists archive locations, SHA256 identities and excluded
executable hashes. This operation neither edits nor restarts production.

Progress reports continue on handoff/fifth-lattice-optimizations-20261105:
  ada_validation/weekend-20261106
  boole_validation/bulk-continuation-20261108
  cabbage_validation/production-20261108
They publish source/configuration identities, committed cursors and coverage
receipts every fifteen minutes, with immediate startup/terminal updates.

Full append-only coverage journals and GMP response archives remain in local
durable storage plus verified NFS replicas. They are not committed to Git.
All current computation retains the November 10, 2026 17:00 Central deadline.

These files are frozen review/reproduction evidence. Continue using each
node's validated service and allocator; do not run a snapshot with stale
ownership, paths, deadlines or source identities.
