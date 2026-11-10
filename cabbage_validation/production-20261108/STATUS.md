# Cabbage combined search

Updated: 2026-11-10T07:25:04.155948+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **722,124,288**.
New replicated logical patches: **222,124,288** in 867,673 chunks.
Combined verified selected patches, including parents: **222,124,288**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 722124288]`.
Local cursor: 723,414,784; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4019.6182938158163, 'elapsed_seconds': 9932.610244719952, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514182, 'mean_ready_depth': 0.140551335383339, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 871864, 'prepare_wall_seconds': 9929.596827161673, 'producer_wait_capacity_seconds': 0.5358620136976242, 'producer_wait_full_seconds': 172.90900722175138, 'ready': 0, 'ready_depth_seconds': {'0': 8927.670910596033, '1': 799.7102909683017, '2': 19.355784354615025, '3': 185.87325802003033}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 109054, 'flush_seconds': 584.4777349032811, 'pending_bytes': 104578, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,451 patches/s**; new independent GMP audits: 6,812.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
