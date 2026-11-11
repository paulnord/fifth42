# Boole combined search

Updated: 2026-11-11T07:40:12.097525+00:00

State: **running**. Run **boole-preparation-20261110-13-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,868,290,816**.
New replicated logical patches: **36,290,816** in 141,761 chunks.
Combined verified selected patches, including parents: **36,290,816**.
Fresh interval: `[7832000000, 7896000000]`; replicated: `[7832000000, 7868290816]`.
Local cursor: 7,868,858,112; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16087304818211123, 'elapsed_seconds': 3604.454303480976, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681125, 'mean_ready_depth': 0.9991117008807275, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8978, 'prepare_wall_seconds': 3603.0372226464096, 'producer_wait_capacity_seconds': 0.011631525470875204, 'producer_wait_full_seconds': 1997.8352523175417, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.201831173268147, '1': 3601.252469897736}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 17995, 'flush_seconds': 125.65999395196559, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,199 patches/s**; new independent GMP audits: 1,123.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
