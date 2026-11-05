> Historical baseline document. The published-library adaptation and newer bounded measurements are documented in ADAPTATION.md, THIRD_PARTY.md, MODULAR_FILTERS.md and ENUMERATION_OPTIMIZATIONS.md. This document does not authorize any new ADA activity.

# Publication scope and source snapshot

Published on 2026-11-04 to the private `paulnord/fifth42` repository for Codex on ADA.
Branch: `handoff/fifth-lattice-prototype`.
Directory: `lattice_prototype/`.

The branch is based on main commit `853fd98fc91968987fcb3e9e4c43b4fe880c8246` ("Publish running four133 status and ADA review evidence"). Only this new directory is added. No production file, four133 file, main branch or existing handoff branch is modified. The main head was checked before publication; later independent ADA updates may advance main.

Every deliverable is an individual UTF-8 text file. There are no archives, compiled binaries, Python bytecode or run checkpoints. `SHA256SUMS` covers every other file in this directory. `vendor/SOURCES.json` identifies all seven frozen upstream files by their original Git blob SHA-1 and SHA-256 values. They are intentionally a frozen comparison baseline, not imports from whichever upstream version happens to be checked out later.

`results/` preserves the original raw cloud test logs, exact hit lists, timings, guard output and upstream comparisons. The timing numbers describe the cloud prototype, not ADA. Documentation was adjusted only to explain this GitHub handoff; the tested algorithm, tests, upstream source snapshots and raw result bytes are unchanged.

Coverage and performance must remain separate: the tested coverage machinery passed the bounded checks, but this Python prototype has not demonstrated a speedup. Large-number examples are fixture-selected single patches, never complete large-shell searches. No new production run was launched or authorized as part of publication.
