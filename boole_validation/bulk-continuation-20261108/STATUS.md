# Boole combined search

Updated: 2026-11-10T10:50:30.253134+00:00

State: **running**. Run **boole-delegated-20261109-00**; gpu with 16 preparation workers.
Verified replicated cursor: **7,044,177,664**.
New replicated logical patches: **44,177,664** in 172,569 chunks.
Combined verified selected patches, including parents: **44,177,664**.
Fresh interval: `[7000000000, 7064000000]`; replicated: `[7000000000, 7044177664]`.
Local cursor: 7,044,787,968; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 67.56637390801916, 'elapsed_seconds': 3609.233307952003, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482240, 'mean_ready_depth': 2.0760797927475414, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 174714, 'prepare_wall_seconds': 3608.61109644355, 'producer_wait_capacity_seconds': 0.11213809537002817, 'producer_wait_full_seconds': 1579.7124557523057, 'ready': 1, 'ready_depth_seconds': {'0': 603.0840744692832, '1': 572.9821717564482, '2': 379.4270165847265, '3': 2053.740044341539}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 21870, 'flush_seconds': 123.83896176487906, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,391 patches/s**; new independent GMP audits: 1,365.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
