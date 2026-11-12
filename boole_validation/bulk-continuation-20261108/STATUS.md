# Boole combined search

Updated: 2026-11-12T01:25:31.302515+00:00

State: **running**. Run **boole-range-r3-20261111-21-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,375,881,472**.
New replicated logical patches: **31,881,472** in 124,537 chunks.
Combined verified selected patches, including parents: **31,881,472**.
Fresh interval: `[8344000000, 8408000000]`; replicated: `[8344000000, 8375881472]`.
Local cursor: 8,376,444,672; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15679887286387384, 'elapsed_seconds': 3607.604803840979, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683246, 'mean_ready_depth': 0.999235780468162, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7914, 'prepare_wall_seconds': 3605.824590151082, 'producer_wait_capacity_seconds': 0.010154590243473649, 'producer_wait_full_seconds': 2208.268220169819, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.756998904282227, '1': 3604.847801786731}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 15850, 'flush_seconds': 120.0058283774415, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,982 patches/s**; new independent GMP audits: 990.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
