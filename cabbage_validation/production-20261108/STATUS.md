# Cabbage combined search

Updated: 2026-11-12T21:27:11.876395+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-50**; gpu with 16 preparation workers.
Verified replicated cursor: **10,223,755,008**.
New replicated logical patches: **23,755,008** in 92,793 chunks.
Combined verified selected patches, including parents: **23,755,008**.
Fresh interval: `[10200000000, 10264000000]`; replicated: `[10200000000, 10223755008]`.
Local cursor: 10,224,246,528; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 301.2177316689631, 'elapsed_seconds': 2717.1243780680234, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15356723, 'mean_ready_depth': 0.4676905635773648, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 5906, 'prepare_wall_seconds': 2715.834013798507, 'producer_wait_capacity_seconds': 0.005120684276334941, 'producer_wait_full_seconds': 783.7514403803507, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1446.3509429536061, '1': 1270.7734316884307}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 11826, 'flush_seconds': 106.80666027218103, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,899 patches/s**; new independent GMP audits: 739.
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
