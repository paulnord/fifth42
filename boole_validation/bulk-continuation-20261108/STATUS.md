# Boole combined search

Updated: 2026-11-10T20:49:25.400625+00:00

State: **running**. Run **boole-preparation-20261110-07-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,453,449,984**.
New replicated logical patches: **5,449,984** in 21,289 chunks.
Combined verified selected patches, including parents: **5,449,984**.
Fresh interval: `[7448000000, 7512000000]`; replicated: `[7448000000, 7453449984]`.
Local cursor: 7,454,225,152; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14981182804331183, 'elapsed_seconds': 539.0054797109915, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680957, 'mean_ready_depth': 0.9971134985120562, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1506, 'prepare_wall_seconds': 537.5840541807702, 'producer_wait_capacity_seconds': 0.0019580938387662172, 'producer_wait_full_seconds': 266.25736700644484, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.555837709165644, '1': 537.4496395917959}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3015, 'flush_seconds': 19.266749559668824, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,423 patches/s**; new independent GMP audits: 189.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
