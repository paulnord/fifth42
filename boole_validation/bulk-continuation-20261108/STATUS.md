# Boole combined search

Updated: 2026-11-10T14:27:58.264494+00:00

State: **running**. Run **boole-delegated-20261109-03**; gpu with 16 preparation workers.
Verified replicated cursor: **7,202,680,576**.
New replicated logical patches: **10,680,576** in 41,721 chunks.
Combined verified selected patches, including parents: **10,680,576**.
Fresh interval: `[7192000000, 7256000000]`; replicated: `[7192000000, 7202680576]`.
Local cursor: 7,203,000,064; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11.607525747618638, 'elapsed_seconds': 906.6822438700474, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482001, 'mean_ready_depth': 2.1982784907465325, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 42740, 'prepare_wall_seconds': 906.5242953063571, 'producer_wait_capacity_seconds': 0.027097698650322855, 'producer_wait_full_seconds': 411.7834794719238, 'ready': 1, 'ready_depth_seconds': {'0': 114.82591905113077, '1': 137.0702161573572, '2': 108.28846462065121, '3': 546.4976430808892}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 5353, 'flush_seconds': 30.289089862722903, 'pending_bytes': 36831, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,063 patches/s**; new independent GMP audits: 334.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
