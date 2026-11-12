# Boole combined search

Updated: 2026-11-12T12:09:17.213319+00:00

State: **running**. Run **boole-range-r3-20261111-26-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,700,305,152**.
New replicated logical patches: **36,305,152** in 141,817 chunks.
Combined verified selected patches, including parents: **36,305,152**.
Fresh interval: `[8664000000, 8728000000]`; replicated: `[8664000000, 8700305152]`.
Local cursor: 8,700,692,224; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16181605216115713, 'elapsed_seconds': 4515.80716207705, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7684363, 'mean_ready_depth': 0.9993398180890265, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8954, 'prepare_wall_seconds': 4513.666661542258, 'producer_wait_capacity_seconds': 0.0119133380940184, 'producer_wait_full_seconds': 2938.951148093678, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.9812510318588465, '1': 4512.825907875202}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 17946, 'flush_seconds': 137.84273000562098, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,119 patches/s**; new independent GMP audits: 1,120.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
