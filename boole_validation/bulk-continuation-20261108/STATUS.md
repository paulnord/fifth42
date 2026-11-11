# Boole combined search

Updated: 2026-11-11T02:48:35.400195+00:00

State: **running**. Run **boole-preparation-20261110-10-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,687,595,776**.
New replicated logical patches: **47,595,776** in 185,921 chunks.
Combined verified selected patches, including parents: **47,595,776**.
Fresh interval: `[7640000000, 7704000000]`; replicated: `[7640000000, 7687595776]`.
Local cursor: 7,688,331,008; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16035614407155663, 'elapsed_seconds': 4536.232991504017, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7684274, 'mean_ready_depth': 0.9989231327137029, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11786, 'prepare_wall_seconds': 4534.873723777302, 'producer_wait_capacity_seconds': 0.015151752508245409, 'producer_wait_full_seconds': 2405.0984721059795, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.8849185015424155, '1': 4531.348070592445}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 23607, 'flush_seconds': 158.88122589915292, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,640 patches/s**; new independent GMP audits: 1,474.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
