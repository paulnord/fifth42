# Boole combined search

Updated: 2026-11-11T14:21:02.765777+00:00

State: **running**. Run **boole-preparation-20261110-17-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,105,103,104**.
New replicated logical patches: **17,103,104** in 66,809 chunks.
Combined verified selected patches, including parents: **17,103,104**.
Fresh interval: `[8088000000, 8152000000]`; replicated: `[8088000000, 8105103104]`.
Local cursor: 8,105,463,552; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1549335249583237, 'elapsed_seconds': 1802.3537297290168, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682297, 'mean_ready_depth': 0.9991228550342435, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4256, 'prepare_wall_seconds': 1802.2846175573068, 'producer_wait_capacity_seconds': 0.005668008234351873, 'producer_wait_full_seconds': 1044.4771029509138, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.580923060537316, '1': 1800.7728042284725}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 8523, 'flush_seconds': 58.07094576518284, 'pending_bytes': 38375, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,666 patches/s**; new independent GMP audits: 532.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
