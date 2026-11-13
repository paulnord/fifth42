# Boole combined search

Updated: 2026-11-13T01:41:31.608263+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,092,857,600**.
New replicated logical patches: **44,857,600** in 175,225 chunks.
Combined verified selected patches, including parents: **44,857,600**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9092857600]`.
Local cursor: 9,093,158,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16380504262633622, 'elapsed_seconds': 6431.935638586059, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7687191, 'mean_ready_depth': 0.99943566420241, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11010, 'prepare_wall_seconds': 6429.313880542642, 'producer_wait_capacity_seconds': 0.013842702261172235, 'producer_wait_full_seconds': 4478.310017935117, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.629769298597239, '1': 6428.30586705741}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 22053, 'flush_seconds': 172.39264456334058, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,010 patches/s**; new independent GMP audits: 1,377.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
