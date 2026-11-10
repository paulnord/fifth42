# Cabbage combined search

Updated: 2026-11-10T01:01:27.468384+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,712,029,568**.
New replicated logical patches: **139,536,640** in 545,065 chunks.
Combined verified selected patches, including parents: **462,029,568**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2712029568]`.
Local cursor: 2,713,713,024; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1906.4648276076186, 'elapsed_seconds': 6120.141251018969, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.33093078077151444, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 551360, 'prepare_wall_seconds': 6118.215822876256, 'producer_wait_capacity_seconds': 0.3560511656687595, 'producer_wait_full_seconds': 233.58966579282423, 'ready': 0, 'ready_depth_seconds': {'0': 4858.731375183328, '1': 822.2457404754241, '2': 114.39502167142928, '3': 324.76911293779267}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 68956, 'flush_seconds': 397.83418961579446, 'pending_bytes': 109322, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,055 patches/s**; new independent GMP audits: 4,308.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
