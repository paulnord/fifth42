# Cabbage combined search

Updated: 2026-11-12T03:54:37.162945+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-41**; gpu with 16 preparation workers.
Verified replicated cursor: **9,633,369,856**.
New replicated logical patches: **9,369,856** in 36,601 chunks.
Combined verified selected patches, including parents: **9,369,856**.
Fresh interval: `[9624000000, 9688000000]`; replicated: `[9624000000, 9633369856]`.
Local cursor: 9,633,677,056; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 179.33473023457918, 'elapsed_seconds': 913.3240072389599, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355245, 'mean_ready_depth': 0.352352186434593, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2338, 'prepare_wall_seconds': 912.5484253801405, 'producer_wait_capacity_seconds': 0.0022165075642988086, 'producer_wait_full_seconds': 166.52771074441262, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 591.5122929791687, '1': 321.81171087385155}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 4675, 'flush_seconds': 37.49997937993612, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,473 patches/s**; new independent GMP audits: 293.
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
