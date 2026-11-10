# Boole combined search

Updated: 2026-11-10T16:57:42.386081+00:00

State: **running**. Run **boole-delegated-20261109-04**; gpu with 16 preparation workers.
Verified replicated cursor: **7,309,082,368**.
New replicated logical patches: **53,082,368** in 207,353 chunks.
Combined verified selected patches, including parents: **53,082,368**.
Fresh interval: `[7256000000, 7320000000]`; replicated: `[7256000000, 7309082368]`.
Local cursor: 7,309,784,832; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 56.439662111748476, 'elapsed_seconds': 4523.502459897019, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482260, 'mean_ready_depth': 2.2232161689474412, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 209924, 'prepare_wall_seconds': 4521.740449320467, 'producer_wait_capacity_seconds': 0.1335565114277415, 'producer_wait_full_seconds': 2077.980136733211, 'ready': 3, 'ready_depth_seconds': {'0': 560.8454440865316, '1': 649.1574001448462, '2': 532.9324349352391, '3': 2780.567179700418}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 26274, 'flush_seconds': 147.15705027338117, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,879 patches/s**; new independent GMP audits: 1,641.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
