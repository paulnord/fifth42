# Boole combined search

Updated: 2026-11-11T09:25:34.871566+00:00

State: **running**. Run **boole-preparation-20261110-14-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,932,174,080**.
New replicated logical patches: **36,174,080** in 141,305 chunks.
Combined verified selected patches, including parents: **36,174,080**.
Fresh interval: `[7896000000, 7960000000]`; replicated: `[7896000000, 7932174080]`.
Local cursor: 7,932,436,224; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15823351358994842, 'elapsed_seconds': 3625.627076461038, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681255, 'mean_ready_depth': 0.9991103284382454, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8897, 'prepare_wall_seconds': 3625.4034749520943, 'producer_wait_capacity_seconds': 0.011395701265428215, 'producer_wait_full_seconds': 2027.5266192511772, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.2256148134474643, '1': 3622.4014591575833}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 17827, 'flush_seconds': 127.75808561843587, 'pending_bytes': 57179, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,049 patches/s**; new independent GMP audits: 1,112.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
