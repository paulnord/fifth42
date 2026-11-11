# Cabbage combined search

Updated: 2026-11-11T22:20:21.949152+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-37**; gpu with 16 preparation workers.
Verified replicated cursor: **9,426,714,368**.
New replicated logical patches: **58,714,368** in 229,353 chunks.
Combined verified selected patches, including parents: **58,714,368**.
Fresh interval: `[9368000000, 9432000000]`; replicated: `[9368000000, 9426714368]`.
Local cursor: 9,427,369,728; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1158.7280818821164, 'elapsed_seconds': 5409.87567572901, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15360396, 'mean_ready_depth': 0.32283855800759315, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 14478, 'prepare_wall_seconds': 5409.782042290899, 'producer_wait_capacity_seconds': 0.012331042787991464, 'producer_wait_full_seconds': 815.733753284323, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3663.3592118333327, '1': 1746.5164621527074}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 28975, 'flush_seconds': 236.3244651738787, 'pending_bytes': 35301, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,960 patches/s**; new independent GMP audits: 1,810.
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
