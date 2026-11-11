# Ada combined search

Updated: 2026-11-11T16:01:26.802757+00:00

State: **failed**. Run **ada-preparation-rotation-01-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,882,696,576**.
New replicated logical patches: **40,042,752** in 156,417 chunks.
Combined verified selected patches, including parents: **3,132,696,576**.
Fresh interval: `[6842653824, 7000000000]`; replicated: `[6842653824, 6882696576]`.
Local cursor: 6,882,696,576; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 468.69806533603696, 'elapsed_seconds': 2459.858213827014, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685285, 'mean_ready_depth': 0.43948960296598627, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9778, 'prepare_wall_seconds': 2458.67693903076, 'producer_wait_capacity_seconds': 0.009162068774458021, 'producer_wait_full_seconds': 734.5516578398529, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1378.7761004225467, '1': 1081.0821097474545}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 19553, 'flush_seconds': 124.67170330137014, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **16,278 patches/s**; new independent GMP audits: 1,223.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: ['RuntimeError: Another active fifth service: fifth42-range-extension-parent-r3-20261111.service loaded active running [systemd-run] /usr/bin/python3 -B -u /home/pnord/fifth42-range-extension-20261111/parent_coordinator.py --grant /mnt/nfs_share/fifth42-integration-20261109/combined/range-extension-r3-20261111/GRANT-r3.json --grant-sha256 14cd2aca8cafafc80799473cb9497e9c86be4b6f866a8b72c4d6b67a1c696df9 --wait'].

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
