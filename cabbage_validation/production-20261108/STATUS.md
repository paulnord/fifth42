# Cabbage combined search

Updated: 2026-11-10T17:23:17.540269+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T172254Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,496,174,336**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **996,174,336**.
Fresh interval: `[1496172288, 2250000000]`; replicated: `[1496172288, 1496174336]`.
Local cursor: 1,496,563,456; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7.320287797076162, 'elapsed_seconds': 16.063705269014463, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513792, 'mean_ready_depth': 0.09227010287251543, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1390, 'prepare_wall_seconds': 16.049507301766425, 'producer_wait_capacity_seconds': 0.000930089270696044, 'producer_wait_full_seconds': 0.0015029327478259802, 'ready': 0, 'ready_depth_seconds': {'0': 14.666593404253945, '1': 1.3159192558377981, '2': 0.07729373895563185, '3': 0.00389766797889024}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 173, 'flush_seconds': 0.9316639642929658, 'pending_bytes': 107667, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **17,702 patches/s**; new independent GMP audits: 11.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
