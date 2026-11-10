# Cabbage combined search

Updated: 2026-11-10T13:05:59.940547+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,166,673,664**.
New replicated logical patches: **160,837,888** in 628,273 chunks.
Combined verified selected patches, including parents: **666,673,664**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1166673664]`.
Local cursor: 1,167,486,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2938.370150105562, 'elapsed_seconds': 7214.201857537031, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.1468876262097369, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 631177, 'prepare_wall_seconds': 7211.982765877212, 'producer_wait_capacity_seconds': 0.3912553563131951, 'producer_wait_full_seconds': 129.43695663817925, 'ready': 0, 'ready_depth_seconds': {'0': 6453.296877265442, '1': 600.3897976303124, '2': 22.25835735659348, '3': 138.25682450266322}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 78949, 'flush_seconds': 439.62544129876187, 'pending_bytes': 35889, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,378 patches/s**; new independent GMP audits: 4,932.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
