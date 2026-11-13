# Cabbage combined search

Updated: 2026-11-13T00:10:58.368025+00:00

State: **running**. Run **cabbage-extended-overnight-sharing-claim33-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,122,287,360**.
New replicated logical patches: **10,287,360** in 40,185 chunks.
Combined verified selected patches, including parents: **10,287,360**.
Fresh interval: `[9112000000, 9176000000]`; replicated: `[9112000000, 9122287360]`.
Local cursor: 9,122,819,840; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 220.7642636775272, 'elapsed_seconds': 943.1458919260185, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358541, 'mean_ready_depth': 0.28947816941682747, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2642, 'prepare_wall_seconds': 942.5853887654375, 'producer_wait_capacity_seconds': 0.002502317656762898, 'producer_wait_full_seconds': 106.6849279999733, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 670.1257419713074, '1': 273.02014628774486}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 5284, 'flush_seconds': 42.50469705776777, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,462 patches/s**; new independent GMP audits: 331.
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
