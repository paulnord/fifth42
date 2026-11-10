# Cabbage combined search

Updated: 2026-11-10T14:51:19.445622+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,305,361,408**.
New replicated logical patches: **299,525,632** in 1,170,022 chunks.
Combined verified selected patches, including parents: **805,361,408**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1305361408]`.
Local cursor: 1,307,211,264; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5526.773821530864, 'elapsed_seconds': 13535.23479560099, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.1476627898630049, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1177115, 'prepare_wall_seconds': 13531.08377419709, 'producer_wait_capacity_seconds': 0.730867377074901, 'producer_wait_full_seconds': 241.99970721785212, 'ready': 0, 'ready_depth_seconds': {'0': 12108.34980554413, '1': 1115.7696685706615, '2': 50.46509916707873, '3': 260.6502214881475}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 147229, 'flush_seconds': 827.2500474121189, 'pending_bytes': 53843, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,253 patches/s**; new independent GMP audits: 9,197.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
