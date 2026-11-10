# Cabbage combined search

Updated: 2026-11-10T20:59:31.716065+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,710,479,360**.
New replicated logical patches: **171,630,336** in 670,431 chunks.
Combined verified selected patches, including parents: **1,210,479,360**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1710479360]`.
Local cursor: 1,712,861,440; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 709.4984038589173, 'elapsed_seconds': 4070.1058934559696, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838766, 'mean_ready_depth': 0.14898565717936693, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 42429, 'prepare_wall_seconds': 4069.9369758100365, 'producer_wait_capacity_seconds': 0.031040558125823736, 'producer_wait_full_seconds': 125.99267082690494, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3463.7184905368485, '1': 606.387401326152}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 84946, 'flush_seconds': 496.8645910661435, 'pending_bytes': 9912, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,640 patches/s**; new independent GMP audits: 5,304.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
