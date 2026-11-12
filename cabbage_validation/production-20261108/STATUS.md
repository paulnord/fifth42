# Cabbage combined search

Updated: 2026-11-12T00:43:09.048687+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-39**; gpu with 16 preparation workers.
Verified replicated cursor: **9,515,323,136**.
New replicated logical patches: **19,323,136** in 75,481 chunks.
Combined verified selected patches, including parents: **19,323,136**.
Fresh interval: `[9496000000, 9560000000]`; replicated: `[9496000000, 9515323136]`.
Local cursor: 9,515,654,912; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 369.3386445000069, 'elapsed_seconds': 1814.8474728040164, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355397, 'mean_ready_depth': 0.34216878668426526, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 4778, 'prepare_wall_seconds': 1814.135273607215, 'producer_wait_capacity_seconds': 0.004175062756985426, 'producer_wait_full_seconds': 307.3329935276415, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1193.863311941619, '1': 620.9841577863554}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 9564, 'flush_seconds': 75.6023000975838, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,777 patches/s**; new independent GMP audits: 598.
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
