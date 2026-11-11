# Cabbage combined search

Updated: 2026-11-11T22:05:21.042742+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-37**; gpu with 16 preparation workers.
Verified replicated cursor: **9,416,816,384**.
New replicated logical patches: **48,816,384** in 190,689 chunks.
Combined verified selected patches, including parents: **48,816,384**.
Fresh interval: `[9368000000, 9432000000]`; replicated: `[9368000000, 9416816384]`.
Local cursor: 9,417,531,136; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 967.986750077107, 'elapsed_seconds': 4514.597105958033, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15360396, 'mean_ready_depth': 0.32226570479079675, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 12092, 'prepare_wall_seconds': 4514.464964608895, 'producer_wait_capacity_seconds': 0.010283531504683197, 'producer_wait_full_seconds': 677.6196113018086, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3059.6972856159555, '1': 1454.899818198057}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 24198, 'flush_seconds': 197.27564772614278, 'pending_bytes': 105901, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,969 patches/s**; new independent GMP audits: 1,512.
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
