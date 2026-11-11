# Boole combined search

Updated: 2026-11-11T14:36:05.895826+00:00

State: **running**. Run **boole-preparation-20261110-17-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,113,645,312**.
New replicated logical patches: **25,645,312** in 100,177 chunks.
Combined verified selected patches, including parents: **25,645,312**.
Fresh interval: `[8088000000, 8152000000]`; replicated: `[8088000000, 8113645312]`.
Local cursor: 8,114,147,072; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15782342449529096, 'elapsed_seconds': 2701.800964284048, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683578, 'mean_ready_depth': 0.9991716691546214, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6369, 'prepare_wall_seconds': 2701.5647254073992, 'producer_wait_capacity_seconds': 0.008403791929595172, 'producer_wait_full_seconds': 1566.50016801554, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.237983046739828, '1': 2699.5629792072577}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 12752, 'flush_seconds': 89.6880300505436, 'pending_bytes': 115209, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,652 patches/s**; new independent GMP audits: 796.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
