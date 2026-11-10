# Cabbage combined search

Updated: 2026-11-10T16:06:35.881492+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,404,284,928**.
New replicated logical patches: **398,449,152** in 1,556,442 chunks.
Combined verified selected patches, including parents: **904,284,928**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1404284928]`.
Local cursor: 1,406,093,056; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7372.087334918266, 'elapsed_seconds': 18052.65452917904, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.14953598132348261, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1563452, 'prepare_wall_seconds': 18046.104301123356, 'producer_wait_capacity_seconds': 0.9721211111173034, 'producer_wait_full_seconds': 329.5206189209712, 'ready': 3, 'ready_depth_seconds': {'0': 16142.321028058708, '1': 1478.340945321368, '2': 74.79719904751983, '3': 357.1953556993976}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 195546, 'flush_seconds': 1111.1824697605916, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,163 patches/s**; new independent GMP audits: 12,215.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
