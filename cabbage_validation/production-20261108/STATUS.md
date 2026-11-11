# Cabbage combined search

Updated: 2026-11-11T21:35:12.826712+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-37**; gpu with 16 preparation workers.
Verified replicated cursor: **9,397,686,016**.
New replicated logical patches: **29,686,016** in 115,961 chunks.
Combined verified selected patches, including parents: **29,686,016**.
Fresh interval: `[9368000000, 9432000000]`; replicated: `[9368000000, 9397686016]`.
Local cursor: 9,397,784,320; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 582.5934209461557, 'elapsed_seconds': 2704.6296529959654, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358239, 'mean_ready_depth': 0.32078718939921524, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 7266, 'prepare_wall_seconds': 2703.9697192893364, 'producer_wait_capacity_seconds': 0.006166830426082015, 'producer_wait_full_seconds': 402.66390287911054, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1837.0191053806338, '1': 867.6105447503505}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 14537, 'flush_seconds': 117.88694135320839, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,000 patches/s**; new independent GMP audits: 909.
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
