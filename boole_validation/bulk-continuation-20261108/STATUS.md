# Boole combined search

Updated: 2026-11-10T18:59:32.441168+00:00

State: **running**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,394,082,560**.
New replicated logical patches: **10,082,560** in 39,385 chunks.
Combined verified selected patches, including parents: **10,082,560**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7394082560]`.
Local cursor: 7,394,639,616; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 16.478790906781796, 'elapsed_seconds': 923.7884593349881, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481942, 'mean_ready_depth': 2.109112683400558, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 41476, 'prepare_wall_seconds': 922.5878141866415, 'producer_wait_capacity_seconds': 0.026691508654039353, 'producer_wait_full_seconds': 422.9941664500511, 'ready': 3, 'ready_depth_seconds': {'0': 150.17362874903483, '1': 138.34956374787726, '2': 95.77140513970517, '3': 539.4938607783988}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 5193, 'flush_seconds': 30.85575807117857, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,490 patches/s**; new independent GMP audits: 325.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
