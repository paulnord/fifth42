# Boole combined search

Updated: 2026-11-11T11:27:11.211159+00:00

State: **running**. Run **boole-preparation-20261110-15-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,003,940,096**.
New replicated logical patches: **43,940,096** in 171,641 chunks.
Combined verified selected patches, including parents: **43,940,096**.
Fresh interval: `[7960000000, 8024000000]`; replicated: `[7960000000, 8003940096]`.
Local cursor: 8,004,601,600; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16506104730069637, 'elapsed_seconds': 4504.3234124379815, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681938, 'mean_ready_depth': 0.9991627978538429, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10881, 'prepare_wall_seconds': 4504.063730952155, 'producer_wait_capacity_seconds': 0.013979019073303789, 'producer_wait_full_seconds': 2557.564817165374, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.7710271378746256, '1': 4500.552383210103}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 21815, 'flush_seconds': 155.26201526622754, 'pending_bytes': 114678, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,893 patches/s**; new independent GMP audits: 1,360.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
