# Cabbage combined search

Updated: 2026-11-10T17:53:29.980833+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T172254Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,536,372,992**.
New replicated logical patches: **40,200,704** in 157,034 chunks.
Combined verified selected patches, including parents: **1,036,372,992**.
Fresh interval: `[1496172288, 2250000000]`; replicated: `[1496172288, 1536372992]`.
Local cursor: 1,537,091,584; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 723.186102337786, 'elapsed_seconds': 1829.3569207550026, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514669, 'mean_ready_depth': 0.18124038513773966, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 159787, 'prepare_wall_seconds': 1828.7887109459843, 'producer_wait_capacity_seconds': 0.09952214948134497, 'producer_wait_full_seconds': 34.968458454241045, 'ready': 0, 'ready_depth_seconds': {'0': 1600.4575989412842, '1': 168.2019289204036, '2': 18.740751965437084, '3': 41.95664000691613}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 19984, 'flush_seconds': 110.71407258242834, 'pending_bytes': 35892, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,312 patches/s**; new independent GMP audits: 1,249.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
