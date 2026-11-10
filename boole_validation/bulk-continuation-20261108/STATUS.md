# Boole combined search

Updated: 2026-11-10T07:36:01.697677+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **350,550,016**.
New replicated logical patches: **50,550,016** in 197,461 chunks.
Combined verified selected patches, including parents: **50,550,016**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 350550016]`.
Local cursor: 351,148,800; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 572.6181237927522, 'elapsed_seconds': 2719.4703537190217, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513863, 'mean_ready_depth': 0.5754221186945168, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 199571, 'prepare_wall_seconds': 2718.779187788721, 'producer_wait_capacity_seconds': 0.12248461047420278, 'producer_wait_full_seconds': 352.82944480958395, 'ready': 1, 'ready_depth_seconds': {'0': 2023.2100678248098, '1': 239.7035877617309, '2': 44.53028700512368, '3': 412.02641029731603}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 24991, 'flush_seconds': 128.9884491492412, 'pending_bytes': 34503, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,780 patches/s**; new independent GMP audits: 1,560.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
