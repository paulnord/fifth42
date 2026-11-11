# Boole combined search

Updated: 2026-11-11T04:44:21.849342+00:00

State: **running**. Run **boole-preparation-20261110-11-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,760,453,376**.
New replicated logical patches: **56,453,376** in 220,521 chunks.
Combined verified selected patches, including parents: **56,453,376**.
Fresh interval: `[7704000000, 7768000000]`; replicated: `[7704000000, 7760453376]`.
Local cursor: 7,761,000,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16527079604566097, 'elapsed_seconds': 5418.234994549013, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681946, 'mean_ready_depth': 0.9990123887016201, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13898, 'prepare_wall_seconds': 5416.825621596363, 'producer_wait_capacity_seconds': 0.01845419517485425, 'producer_wait_full_seconds': 2914.810706043616, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.351107547874562, '1': 5412.883884451119}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 27848, 'flush_seconds': 192.35622388805496, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,504 patches/s**; new independent GMP audits: 1,738.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
