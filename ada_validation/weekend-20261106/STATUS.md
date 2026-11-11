# Ada combined search

Updated: 2026-11-11T22:12:24.183062+00:00

State: **running**. Run **ada-allocated-r3-02-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,336,328,960**.
New replicated logical patches: **8,328,960** in 32,535 chunks.
Combined verified selected patches, including parents: **8,328,960**.
Fresh interval: `[10328000000, 10392000000]`; replicated: `[10328000000, 10336328960]`.
Local cursor: 10,336,654,848; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1148.5340033813845, 'elapsed_seconds': 1795.5312864859588, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923609, 'mean_ready_depth': 0.21252718067082563, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 33637, 'prepare_wall_seconds': 1795.2698282243218, 'producer_wait_capacity_seconds': 0.02280497213359922, 'producer_wait_full_seconds': 85.42254423501436, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1628.0308648765786, '1': 53.14619890204631, '2': 14.609662887873128, '3': 99.74455914844293}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 4742, 'flush_seconds': 42.123664234997705, 'pending_bytes': 489309, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **4,795 patches/s**; new independent GMP audits: 263.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
