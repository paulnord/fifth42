# Cabbage combined search

Updated: 2026-11-10T17:38:19.280924+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T172254Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,515,356,160**.
New replicated logical patches: **19,183,872** in 74,937 chunks.
Combined verified selected patches, including parents: **1,015,356,160**.
Fresh interval: `[1496172288, 2250000000]`; replicated: `[1496172288, 1515356160]`.
Local cursor: 1,516,838,912; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 365.86733350821305, 'elapsed_seconds': 917.0262840480427, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514613, 'mean_ready_depth': 0.17570039823417308, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 80530, 'prepare_wall_seconds': 916.7339274422266, 'producer_wait_capacity_seconds': 0.05006664904067293, 'producer_wait_full_seconds': 15.859046691679396, 'ready': 0, 'ready_depth_seconds': {'0': 804.1596054604743, '1': 83.99662550789071, '2': 9.484898805385455, '3': 19.385153393261135}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 10072, 'flush_seconds': 55.515223725291435, 'pending_bytes': 17938, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,384 patches/s**; new independent GMP audits: 630.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
