# Cabbage combined search

Updated: 2026-11-13T01:11:07.819551+00:00

State: **running**. Run **cabbage-extended-overnight-sharing-claim33-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,163,575,040**.
New replicated logical patches: **51,575,040** in 201,465 chunks.
Combined verified selected patches, including parents: **51,575,040**.
Fresh interval: `[9112000000, 9176000000]`; replicated: `[9112000000, 9163575040]`.
Local cursor: 9,163,755,264; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1065.3005420377012, 'elapsed_seconds': 4546.484245647094, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15360737, 'mean_ready_depth': 0.2914582353254177, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 12619, 'prepare_wall_seconds': 4546.353540790267, 'producer_wait_capacity_seconds': 0.0119364078855142, 'producer_wait_full_seconds': 524.7517171631334, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3221.373967008898, '1': 1325.110275171115}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 25255, 'flush_seconds': 206.58089343609754, 'pending_bytes': 176501, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,366 patches/s**; new independent GMP audits: 1,578.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
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
