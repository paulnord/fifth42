# Boole combined search

Updated: 2026-11-10T17:42:50.816152+00:00

State: **running**. Run **boole-delegated-20261109-05**; gpu with 16 preparation workers.
Verified replicated cursor: **7,341,139,712**.
New replicated logical patches: **21,139,712** in 82,577 chunks.
Combined verified selected patches, including parents: **21,139,712**.
Fresh interval: `[7320000000, 7384000000]`; replicated: `[7320000000, 7341139712]`.
Local cursor: 7,341,297,408; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 20.36391641863156, 'elapsed_seconds': 1811.353770265996, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482507, 'mean_ready_depth': 2.267415759625196, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 82692, 'prepare_wall_seconds': 1810.0231133315829, 'producer_wait_capacity_seconds': 0.054300570918712765, 'producer_wait_full_seconds': 851.7368973544217, 'ready': 3, 'ready_depth_seconds': {'0': 205.2673863178934, '1': 248.38125868176576, '2': 214.40454664308345, '3': 1143.3005776632344}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 10359, 'flush_seconds': 57.76435524196131, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,685 patches/s**; new independent GMP audits: 647.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
