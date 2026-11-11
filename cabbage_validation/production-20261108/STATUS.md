# Cabbage combined search

Updated: 2026-11-11T19:06:42.076433+00:00

State: **running**. Run **cabbage-extended-r3-cap100-job-36-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,306,607,360**.
New replicated logical patches: **2,607,360** in 10,185 chunks.
Combined verified selected patches, including parents: **2,607,360**.
Fresh interval: `[9304000000, 9368000000]`; replicated: `[9304000000, 9306607360]`.
Local cursor: 9,306,652,416; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 84.48376698762877, 'elapsed_seconds': 252.93848532100674, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3843157, 'mean_ready_depth': 0.2618621553065522, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 2551, 'prepare_wall_seconds': 252.22335285198642, 'producer_wait_capacity_seconds': 0.0018729534931480885, 'producer_wait_full_seconds': 53.79679605655838, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 186.70346512884134, '1': 66.23501692613354}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 1278, 'flush_seconds': 13.287368310557213, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,309 patches/s**; new independent GMP audits: 80.
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
