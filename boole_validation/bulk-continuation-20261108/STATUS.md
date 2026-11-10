# Boole combined search

Updated: 2026-11-10T19:14:45.860004+00:00

State: **running**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,404,945,152**.
New replicated logical patches: **20,945,152** in 81,817 chunks.
Combined verified selected patches, including parents: **20,945,152**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7404945152]`.
Local cursor: 7,405,047,552; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 32.23915487161139, 'elapsed_seconds': 1835.1641909609898, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481977, 'mean_ready_depth': 2.1086397840653, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 82052, 'prepare_wall_seconds': 1833.8174004780012, 'producer_wait_capacity_seconds': 0.05280813144054264, 'producer_wait_full_seconds': 844.0467172596836, 'ready': 3, 'ready_depth_seconds': {'0': 295.6335351752932, '1': 279.19729243562324, '2': 190.49715646350523, '3': 1069.836205996573}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 10276, 'flush_seconds': 61.48724700225284, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,444 patches/s**; new independent GMP audits: 642.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
