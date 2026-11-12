# Cabbage combined search

Updated: 2026-11-12T07:27:29.936655+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-43**; gpu with 16 preparation workers.
Verified replicated cursor: **9,761,140,480**.
New replicated logical patches: **9,140,480** in 35,705 chunks.
Combined verified selected patches, including parents: **9,140,480**.
Fresh interval: `[9752000000, 9816000000]`; replicated: `[9752000000, 9761140480]`.
Local cursor: 9,761,316,608; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 167.1339088458335, 'elapsed_seconds': 900.1696613359964, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355761, 'mean_ready_depth': 0.3686394631546582, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2251, 'prepare_wall_seconds': 899.7923357343534, 'producer_wait_capacity_seconds': 0.002002477878704667, 'producer_wait_full_seconds': 181.22224629635457, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 568.3315984989749, '1': 331.83806070301216}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 4503, 'flush_seconds': 38.1767548925709, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,237 patches/s**; new independent GMP audits: 282.
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
