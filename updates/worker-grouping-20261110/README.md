# Worker grouping update and safe-stop repair

**No live system has been changed.** This is a staged update package, not an auto-updater.
CPU policy/controller regression tests pass. Live systemd/NFS canary validation must run
on the destination before any authorized deployment. No GPU algorithm changes here.

## What is promoted

- Existing group4 remains the default on **Ada, Boole and Cabbage**.
- Group8 + dispatch_chunksize2 is a gated opt-in for a locally measured, bounded
  canary; group4 uses dispatch_chunksize4. Group16 is not promoted.
- Cabbage controller final-report race repair is included, with fail-closed tests.
- Warm reductions, sealed-packet caching and overlap are **not** enabled.
- No CUDA CGBN/cuPQC roots, fused GPU work or mathematical coverage changes.

## Crucial coordinate distinction

The result at commit `6870fa557510159f9f0c23232568867860a52963` is a 48.2%
whole-pipeline gain on Cabbage hardware for original logical cells
**[2,572,492,928, 2,572,525,696)** (three alternating repeats). This is not all
of Cabbage's reserved space. The latest reconciled stopped cursor is **1,538,849,024**,
outside that tested window. Do not promote group8 there based on the host name.
Ada/dense samples favored group4. Do not transfer a Cabbage hardware result to Ada/Boole.

## Commands (in an isolated checkout)

`bash updates/worker-grouping-20261110/check.sh`

The ready-made benchmark uses the *existing isolated test installation* from the
previous speed-test handoff (its `venv`, `worker`, `controls.py`, `trial_groups.py`
and `experiment-manifest.json`). Cabbage already has that installation. For a
new host, use the pinned setup at commit `cb908547e6cefd51713da9595073e576eaca6950`,
`experiments/production-speed-tests-20261110/setup.sh` in a fresh clone; select
its locally verified CUDA/compiler wrappers. This update does not install system packages.

```
python3 updates/worker-grouping-20261110/benchmark_current.py --host cabbage --harness /ABS/ISOLATED/HARNESS --checkpoint /ABS/FINAL/checkpoint.json --out /ABS/NEW/TEST/RESULTS
python3 updates/worker-grouping-20261110/plan_update.py --host cabbage --config /ABS/OLD/production-config.json --checkpoint /ABS/FINAL/checkpoint.json --replica-checkpoint /ABS/NFS/checkpoint.json --supervisor /ABS/FINAL/supervisor.json --receipt /ABS/NEW/TEST/RESULTS/receipt.json --output /ABS/NEW/update-proposal.json
```

The Codex worker resolves these absolute paths from its verified local records; Paul
should not need to fill them. For Ada/Boole use their corresponding host value.
The benchmark only runs with a quiescent GPU and CPU load <=4, bounded cooldown,
16 workers, 3 alternating repeats, 32768 original cells, and at most20min. It holds
no production ledger claim and records **zero production coverage**. Codex must hold
the host's existing GPU/CPU test lease before invoking it. Never run concurrently
with production. Only stop production through an already authorized graceful stop;
otherwise wait for the natural stop/checkpoint boundary.

The planner reads inputs and writes a **new proposal file only**. It validates
local/NFS checkpoint equality, clean supervisor exit+leases, config fingerprint,
manifest hash and sample binding. Group8 needs >=10% median gain and exact/audit/
durability gates. Missing/mismatched evidence blocks promotion; omit receipt to
retain group4. Full harness-to-current-worker compute-source comparison is a
mandatory deployment review, not something inferred from a config fingerprint.

## Installation/restart gates

1. Snapshot actual current configs, source manifests, service states and deadline.
   Reject any unknown local edits or immutable-manifest mismatch. Existing running
   Ada/Boole work stays untouched until its authorized stopped boundary.
2. Reconcile final checkpoint/digest/cursor and NFS replica/final-copy receipt,
   released leases and exit0. Cabbage's published r1 reconciliation provides evidence,
   but re-read its current local files rather than trust that snapshot indefinitely.
3. Compare current Cabbage controller to the archived base and stage the small
   derived fix in `controller/` via a **new frozen controller release**. Preserve
   source history and regenerate its manifest through the local freeze workflow.
   Never overwrite a frozen live file or suppress manifest validation. Ada/Boole
   do not receive a blind replacement of their structurally different controllers.
4. Run the controller delay/failure tests, then a bounded TEST_ONLY service lifecycle:
   delayed terminal report, graceful stop, final replica, leases, seal. Confirm no
   reservation advance on signal/deadline. Do not invent production success from unit tests.
5. Run the current-cursor benchmark, compare its compute sources and installed
   runtime versions to the target worker; if different, benchmark a matching copy
   before promoting. Read-only plan_update emits proposed fields, not a runnable config.
6. Use the worker's existing audited seal/freeze/continuation workflow for a **fresh
   journal and new immutable identity** starting exactly at verified committed cursor.
   Set group8+dispatch2 only if the local gate passes; retain remaining safety fields,
   audit cadence, ledger claim, nonoverlap, publisher and **original deadline**.
   First rollout is a bounded <=1,048,576-cell canary (range_end capped inside current
   claim; do not mark the whole claim completed at that bound). Archive remaining claim
   ownership for the next continuation. Use an explicit local test/stop bound if the
   controller requires reservation endpoint equality; never falsify claim metadata.
7. Validate nonempty controls and GMP audits, final drain/local-NFS equality and
   actual throughput. Extend group8 only after explicit canary acceptance, using
   periodic matched sampling for future different regions. Otherwise revert group4
   via another fresh continuation. No in-place journal reuse or silent fallback.
8. Publish source/config hashes, decisions, timing samples, predecessor/successor
   cursors and validation receipts to GitHub. **Do not automatically start production
   as part of this package.** Startup requires Paul's worker-side go-ahead and unexpired
   original authorization. This update does not extend the Nov10 17:00 Central deadline.

## Verification scope

`published-samples.json` preserves the 27 selected evidence records, and
`benchmark-evidence.md` the source report. Their checked-in hashes are verified.
Controller unit tests stub all service actions. No live GPU/systemd/NFS tests were
performed here. This is intentionally conservative: a measured speedup in one sample
is not blanket proof of a faster region, and selected-grid coverage is not full-box coverage.
