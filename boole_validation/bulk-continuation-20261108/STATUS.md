# Boole combined search

Updated: 2026-11-10T04:45:42.403555+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **164,527,616**.
New replicated logical patches: **64,527,616** in 252,061 chunks.
Combined verified selected patches, including parents: **64,527,616**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 164527616]`.
Local cursor: 165,583,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 834.0327177921426, 'elapsed_seconds': 3610.889925658994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 546826, 'mean_ready_depth': 0.539413660856423, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 256005, 'prepare_wall_seconds': 3610.0110572302365, 'producer_wait_capacity_seconds': 0.1560324304155074, 'producer_wait_full_seconds': 441.48856006597634, 'ready': 1, 'ready_depth_seconds': {'0': 2750.5015822422574, '1': 285.24638611084083, '2': 62.908901789283846, '3': 512.2330546866287}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 32054, 'flush_seconds': 174.79821346135577, 'pending_bytes': 17093, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,145 patches/s**; new independent GMP audits: 2,001.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
