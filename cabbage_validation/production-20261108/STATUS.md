# Cabbage combined search

Updated: 2026-11-10T01:31:39.473221+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,753,210,752**.
New replicated logical patches: **180,717,824** in 705,929 chunks.
Combined verified selected patches, including parents: **503,210,752**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2753210752]`.
Local cursor: 2,754,964,096; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2459.5284549755743, 'elapsed_seconds': 7933.802030761959, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.33518852272001287, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 712544, 'prepare_wall_seconds': 7931.317138076702, 'producer_wait_capacity_seconds': 0.4601850301842205, 'producer_wait_full_seconds': 309.4109626910649, 'ready': 0, 'ready_depth_seconds': {'0': 6285.321615490422, '1': 1067.5966501864605, '2': 150.92856094159652, '3': 429.95520339149516}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 89115, 'flush_seconds': 516.9111066453625, 'pending_bytes': 109331, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,985 patches/s**; new independent GMP audits: 5,567.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
