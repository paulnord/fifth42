# Cabbage combined search

Updated: 2026-11-12T13:14:04.219776+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-46**; gpu with 16 preparation workers.
Verified replicated cursor: **9,960,908,288**.
New replicated logical patches: **16,908,288** in 66,048 chunks.
Combined verified selected patches, including parents: **16,908,288**.
Fresh interval: `[9944000000, 10008000000]`; replicated: `[9944000000, 9960908288]`.
Local cursor: 9,961,428,480; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 251.1634075982729, 'elapsed_seconds': 1811.4255352559267, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355535, 'mean_ready_depth': 0.42061557153480955, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 4234, 'prepare_wall_seconds': 1810.5030506749172, 'producer_wait_capacity_seconds': 0.003953549428842962, 'producer_wait_full_seconds': 436.8046055175364, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1049.5117455865256, '1': 761.9137868044199}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 8473, 'flush_seconds': 71.55897826410364, 'pending_bytes': 35923, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,568 patches/s**; new independent GMP audits: 530.
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
