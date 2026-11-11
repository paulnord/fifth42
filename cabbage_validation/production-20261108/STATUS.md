# Cabbage combined search

Updated: 2026-11-11T18:15:38.036531+00:00

State: **running**. Run **cabbage-extended-r3-cap100-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,283,585,792**.
New replicated logical patches: **43,585,792** in 170,257 chunks.
Combined verified selected patches, including parents: **43,585,792**.
Fresh interval: `[9240000000, 9304000000]`; replicated: `[9240000000, 9283585792]`.
Local cursor: 9,283,862,272; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1427.349017680157, 'elapsed_seconds': 4248.254262653994, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3843959, 'mean_ready_depth': 0.26003043483529675, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 42744, 'prepare_wall_seconds': 4248.0779926970135, 'producer_wait_capacity_seconds': 0.03070955438306555, 'producer_wait_full_seconds': 899.8721442102105, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3143.5788579021464, '1': 1104.675403208821}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 21408, 'flush_seconds': 217.90808746771654, 'pending_bytes': 141134, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,302 patches/s**; new independent GMP audits: 1,336.
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
