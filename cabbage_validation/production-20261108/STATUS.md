# Cabbage combined search

Updated: 2026-11-10T10:40:38.672043+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **981,858,304**.
New replicated logical patches: **481,858,304** in 1,882,259 chunks.
Combined verified selected patches, including parents: **481,858,304**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 981858304]`.
Local cursor: 982,649,856; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8811.939249039977, 'elapsed_seconds': 21673.055822741997, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.13885819764135984, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1885052, 'prepare_wall_seconds': 21666.55982108903, 'producer_wait_capacity_seconds': 1.1616836194880307, 'producer_wait_full_seconds': 379.09085198509274, 'ready': 0, 'ready_depth_seconds': {'0': 19528.056321242417, '1': 1689.2924986971775, '2': 46.93203538178932, '3': 408.7749664885923}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 235786, 'flush_seconds': 1275.676967402338, 'pending_bytes': 87284, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,257 patches/s**; new independent GMP audits: 14,727.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
