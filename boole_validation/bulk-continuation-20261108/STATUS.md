# Boole combined search

Updated: 2026-11-10T18:43:11.275280+00:00

State: **running**. Run **boole-delegated-20261109-05**; gpu with 16 preparation workers.
Verified replicated cursor: **7,382,972,160**.
New replicated logical patches: **62,972,160** in 245,985 chunks.
Combined verified selected patches, including parents: **62,972,160**.
Fresh interval: `[7320000000, 7384000000]`; replicated: `[7320000000, 7382972160]`.
Local cursor: 7,383,590,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 62.50235244218493, 'elapsed_seconds': 5435.270648501988, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482507, 'mean_ready_depth': 2.259332139799645, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 248068, 'prepare_wall_seconds': 5433.289697887027, 'producer_wait_capacity_seconds': 0.16238441708264872, 'producer_wait_full_seconds': 2551.7847220491967, 'ready': 3, 'ready_depth_seconds': {'0': 629.2531060292968, '1': 748.2074284534901, '2': 641.5561029608361, '3': 3416.254010098346}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 31061, 'flush_seconds': 173.41328674246324, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,683 patches/s**; new independent GMP audits: 1,939.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
