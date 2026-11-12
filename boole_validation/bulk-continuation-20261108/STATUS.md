# Boole combined search

Updated: 2026-11-12T04:28:39.077942+00:00

State: **stopped**. Run **boole-range-r3-20261111-22-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,472,000,000**.
New replicated logical patches: **64,000,000** in 250,000 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[8408000000, 8472000000]`; replicated: `[8408000000, 8472000000]`.
Local cursor: 8,472,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.17466673080343753, 'elapsed_seconds': 7339.798744996078, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7688034, 'mean_ready_depth': 0.9990274428099232, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15625, 'prepare_wall_seconds': 7337.557175330585, 'producer_wait_capacity_seconds': 0.020844149868935347, 'producer_wait_full_seconds': 4569.619744280586, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7.138370743137784, '1': 7332.660370952915}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 31309, 'flush_seconds': 237.42034222756047, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,719 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
