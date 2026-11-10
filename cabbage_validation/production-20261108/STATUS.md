# Cabbage combined search

Updated: 2026-11-10T09:10:25.571099+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **861,902,336**.
New replicated logical patches: **361,902,336** in 1,413,681 chunks.
Combined verified selected patches, including parents: **361,902,336**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 861902336]`.
Local cursor: 863,554,304; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6600.302915223059, 'elapsed_seconds': 16262.499776776996, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.1401556198839745, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1420071, 'prepare_wall_seconds': 16257.609579160402, 'producer_wait_capacity_seconds': 0.8724763183272444, 'producer_wait_full_seconds': 286.583408330509, 'ready': 1, 'ready_depth_seconds': {'0': 14635.415827649937, '1': 1284.0628696351196, '2': 33.84536844777176, '3': 309.1757101821713}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 177629, 'flush_seconds': 956.6927845135215, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,342 patches/s**; new independent GMP audits: 11,095.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
