# Boole combined search

Updated: 2026-11-10T18:12:58.989561+00:00

State: **running**. Run **boole-delegated-20261109-05**; gpu with 16 preparation workers.
Verified replicated cursor: **7,362,105,088**.
New replicated logical patches: **42,105,088** in 164,473 chunks.
Combined verified selected patches, including parents: **42,105,088**.
Fresh interval: `[7320000000, 7384000000]`; replicated: `[7320000000, 7362105088]`.
Local cursor: 7,362,420,480; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 41.30056480207713, 'elapsed_seconds': 3625.782544012007, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482507, 'mean_ready_depth': 2.264228403591124, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 165508, 'prepare_wall_seconds': 3624.1444604799035, 'producer_wait_capacity_seconds': 0.10851939715212211, 'producer_wait_full_seconds': 1703.2139985873364, 'ready': 3, 'ready_depth_seconds': {'0': 415.4521110046189, '1': 496.1124595651636, '2': 429.1665562449489, '3': 2285.0514164472697}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 20726, 'flush_seconds': 116.02646520506823, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,685 patches/s**; new independent GMP audits: 1,294.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
