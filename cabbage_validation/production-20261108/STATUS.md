# Cabbage combined search

Updated: 2026-11-12T14:29:18.931406+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-46**; gpu with 16 preparation workers.
Verified replicated cursor: **10,003,697,408**.
New replicated logical patches: **59,697,408** in 233,193 chunks.
Combined verified selected patches, including parents: **59,697,408**.
Fresh interval: `[9944000000, 10008000000]`; replicated: `[9944000000, 10003697408]`.
Local cursor: 10,004,242,176; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 861.1057200322393, 'elapsed_seconds': 6333.694954706007, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15356505, 'mean_ready_depth': 0.4250286090571736, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 14706, 'prepare_wall_seconds': 6332.609650696977, 'producer_wait_capacity_seconds': 0.01377232070080936, 'producer_wait_full_seconds': 1556.8469315666007, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3641.693394267815, '1': 2692.0015567911323}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 29444, 'flush_seconds': 261.6220076326281, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,509 patches/s**; new independent GMP audits: 1,839.
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
