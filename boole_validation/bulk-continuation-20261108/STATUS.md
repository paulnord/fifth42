# Boole combined search

Updated: 2026-11-10T15:28:08.713651+00:00

State: **running**. Run **boole-delegated-20261109-03**; gpu with 16 preparation workers.
Verified replicated cursor: **7,245,631,232**.
New replicated logical patches: **53,631,232** in 209,497 chunks.
Combined verified selected patches, including parents: **53,631,232**.
Fresh interval: `[7192000000, 7256000000]`; replicated: `[7192000000, 7245631232]`.
Local cursor: 7,246,309,120; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 58.22546880861046, 'elapsed_seconds': 4521.335372010013, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482211, 'mean_ready_depth': 2.208989341092275, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 212108, 'prepare_wall_seconds': 4520.564357166993, 'producer_wait_capacity_seconds': 0.134589935594704, 'producer_wait_full_seconds': 2062.4706964991055, 'ready': 3, 'ready_depth_seconds': {'0': 572.820949552115, '1': 663.7208969914936, '2': 530.5198260271573, '3': 2754.2736984092626}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 26569, 'flush_seconds': 149.69625120115234, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,009 patches/s**; new independent GMP audits: 1,658.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
