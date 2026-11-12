# Boole combined search

Updated: 2026-11-12T16:53:30.226345+00:00

State: **running**. Run **boole-range-r3-20261111-28-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,834,039,552**.
New replicated logical patches: **42,039,552** in 164,217 chunks.
Combined verified selected patches, including parents: **42,039,552**.
Fresh interval: `[8792000000, 8856000000]`; replicated: `[8792000000, 8834039552]`.
Local cursor: 8,834,105,088; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15700186614412814, 'elapsed_seconds': 5417.376698244014, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681953, 'mean_ready_depth': 0.9993825155436655, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10266, 'prepare_wall_seconds': 5412.448328764876, 'producer_wait_capacity_seconds': 0.013529520714655519, 'producer_wait_full_seconds': 3609.5254331826, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.345143055310473, '1': 5414.03155233874}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 20559, 'flush_seconds': 151.28601105464622, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,760 patches/s**; new independent GMP audits: 1,284.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
