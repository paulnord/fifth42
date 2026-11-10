# Cabbage combined search

Updated: 2026-11-10T12:20:53.328749+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,105,934,336**.
New replicated logical patches: **100,098,560** in 391,010 chunks.
Combined verified selected patches, including parents: **605,934,336**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1105934336]`.
Local cursor: 1,107,201,536; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1832.1928947098204, 'elapsed_seconds': 4509.297921910009, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14468335063337462, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 395839, 'prepare_wall_seconds': 4507.906352577382, 'producer_wait_capacity_seconds': 0.24504768510814756, 'producer_wait_full_seconds': 77.4543746735435, 'ready': 0, 'ready_depth_seconds': {'0': 4036.37418583245, '1': 376.6049450234277, '2': 13.140983883815352, '3': 83.17780651833164}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 49507, 'flush_seconds': 277.5214476247784, 'pending_bytes': 125424, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,440 patches/s**; new independent GMP audits: 3,093.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
