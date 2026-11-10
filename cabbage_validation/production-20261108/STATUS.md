# Cabbage combined search

Updated: 2026-11-10T03:47:14.384132+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,937,771,392**.
New replicated logical patches: **365,278,464** in 1,426,869 chunks.
Combined verified selected patches, including parents: **687,771,392**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2937771392]`.
Local cursor: 2,938,637,696; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4969.415808701189, 'elapsed_seconds': 16062.58800766099, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.3421043677555125, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1429448, 'prepare_wall_seconds': 16057.603304095916, 'producer_wait_capacity_seconds': 0.9247000723262317, 'producer_wait_full_seconds': 677.5829231292009, 'ready': 0, 'ready_depth_seconds': {'0': 12716.138801996422, '1': 2119.155616671371, '2': 305.9548659166903, '3': 921.338722124463}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 178774, 'flush_seconds': 1043.5656396953855, 'pending_bytes': 54675, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,779 patches/s**; new independent GMP audits: 11,168.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
