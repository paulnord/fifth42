# Boole combined search

Updated: 2026-11-12T00:11:33.943145+00:00

State: **running**. Run **boole-range-r3-20261111-20-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,336,473,856**.
New replicated logical patches: **56,473,856** in 220,601 chunks.
Combined verified selected patches, including parents: **56,473,856**.
Fresh interval: `[8280000000, 8344000000]`; replicated: `[8280000000, 8336473856]`.
Local cursor: 8,337,165,056; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15959888382349163, 'elapsed_seconds': 6308.87561970402, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682926, 'mean_ready_depth': 0.9992838399866589, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13947, 'prepare_wall_seconds': 6308.67376270704, 'producer_wait_capacity_seconds': 0.0199666537810117, 'producer_wait_full_seconds': 3831.6058604191057, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.518161757965572, '1': 6304.357455256046}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 27955, 'flush_seconds': 211.01935832377058, 'pending_bytes': 115312, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,053 patches/s**; new independent GMP audits: 1,744.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
