# Cabbage combined search

Updated: 2026-11-12T14:36:38.869328+00:00

State: **stopped**. Run **cabbage-extended-memory-r2-cap100-20261111-job-46**; gpu with 16 preparation workers.
Verified replicated cursor: **10,008,000,000**.
New replicated logical patches: **64,000,000** in 250,000 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[9944000000, 10008000000]`; replicated: `[9944000000, 10008000000]`.
Local cursor: 10,008,000,000; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 914.8646451223176, 'elapsed_seconds': 6731.239888668992, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357401, 'mean_ready_depth': 0.42495033988316355, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 15625, 'prepare_wall_seconds': 6729.796326260082, 'producer_wait_capacity_seconds': 0.014632619800977409, 'producer_wait_full_seconds': 1656.0610734604998, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3870.7972064180067, '1': 2860.442678524996}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 31288, 'flush_seconds': 277.8040171227185, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,507 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
