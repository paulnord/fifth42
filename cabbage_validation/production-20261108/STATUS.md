# Cabbage combined search

Updated: 2026-11-10T02:46:53.776233+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,855,917,696**.
New replicated logical patches: **283,424,768** in 1,107,128 chunks.
Combined verified selected patches, including parents: **605,917,696**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2855917696]`.
Local cursor: 2,857,341,568; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3856.512245440972, 'elapsed_seconds': 12444.561163508974, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.3392260988998191, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1112112, 'prepare_wall_seconds': 12440.689660710515, 'producer_wait_capacity_seconds': 0.7186338805477135, 'producer_wait_full_seconds': 507.19595319015207, 'ready': 1, 'ready_depth_seconds': {'0': 9855.794084301917, '1': 1653.9721446436015, '2': 236.837009733601, '3': 697.9579239688464}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 139089, 'flush_seconds': 809.818718379247, 'pending_bytes': 91105, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,874 patches/s**; new independent GMP audits: 8,689.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
