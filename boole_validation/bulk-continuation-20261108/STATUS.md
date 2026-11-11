# Boole combined search

Updated: 2026-11-11T16:27:51.365089+00:00

State: **running**. Run **boole-preparation-20261110-18-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,177,454,848**.
New replicated logical patches: **25,454,848** in 99,433 chunks.
Combined verified selected patches, including parents: **25,454,848**.
Fresh interval: `[8152000000, 8216000000]`; replicated: `[8152000000, 8177454848]`.
Local cursor: 8,177,688,320; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16118810954503715, 'elapsed_seconds': 2714.612981849001, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681453, 'mean_ready_depth': 0.9991909383274257, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6268, 'prepare_wall_seconds': 2714.458256797574, 'producer_wait_capacity_seconds': 0.008182091638445854, 'producer_wait_full_seconds': 1602.824726716557, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.1962872495059855, '1': 2712.416692529514}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 12551, 'flush_seconds': 92.4131907436531, 'pending_bytes': 134500, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,454 patches/s**; new independent GMP audits: 784.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
