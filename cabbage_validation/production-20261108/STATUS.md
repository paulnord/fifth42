# Cabbage combined search

Updated: 2026-11-10T16:21:46.478897+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,425,495,552**.
New replicated logical patches: **419,659,776** in 1,639,296 chunks.
Combined verified selected patches, including parents: **925,495,552**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1425495552]`.
Local cursor: 1,425,931,520; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7740.269143143145, 'elapsed_seconds': 18955.381588410994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.15018435071037695, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1640330, 'prepare_wall_seconds': 18949.583749921992, 'producer_wait_capacity_seconds': 1.02018088393379, 'producer_wait_full_seconds': 348.8249631835497, 'ready': 0, 'ready_depth_seconds': {'0': 16946.323188820097, '1': 1549.3582163534593, '2': 81.65707937197294, '3': 378.04310040851124}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 205159, 'flush_seconds': 1170.4278607215965, 'pending_bytes': 53843, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,146 patches/s**; new independent GMP audits: 12,816.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
