# Cabbage combined search

Updated: 2026-11-10T15:51:34.149669+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,384,722,176**.
New replicated logical patches: **378,886,400** in 1,480,025 chunks.
Combined verified selected patches, including parents: **884,722,176**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1384722176]`.
Local cursor: 1,386,352,384; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7002.87247742078, 'elapsed_seconds': 17150.310467556003, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.1495521579187801, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1486294, 'prepare_wall_seconds': 17145.064742563118, 'producer_wait_capacity_seconds': 0.9239285789080895, 'producer_wait_full_seconds': 314.6143983355141, 'ready': 0, 'ready_depth_seconds': {'0': 15334.807029073942, '1': 1405.9499615327222, '2': 69.74445027473848, '3': 339.8090257726144}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 185896, 'flush_seconds': 1056.858576301136, 'pending_bytes': 89727, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,177 patches/s**; new independent GMP audits: 11,612.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
