# Cabbage combined search

Updated: 2026-11-12T04:24:39.942771+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-41**; gpu with 16 preparation workers.
Verified replicated cursor: **9,652,178,688**.
New replicated logical patches: **28,178,688** in 110,073 chunks.
Combined verified selected patches, including parents: **28,178,688**.
Fresh interval: `[9624000000, 9688000000]`; replicated: `[9624000000, 9652178688]`.
Local cursor: 9,652,520,704; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 531.8785599393304, 'elapsed_seconds': 2718.3959079550114, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15360276, 'mean_ready_depth': 0.351695588893928, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 6946, 'prepare_wall_seconds': 2717.577858829638, 'producer_wait_capacity_seconds': 0.006556420121341944, 'producer_wait_full_seconds': 495.3801707542734, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1762.3480546928477, '1': 956.0478496950818}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 13896, 'flush_seconds': 115.44638572609983, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,462 patches/s**; new independent GMP audits: 869.
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
