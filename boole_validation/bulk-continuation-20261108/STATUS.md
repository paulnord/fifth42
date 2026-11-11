# Boole combined search

Updated: 2026-11-11T14:06:00.666975+00:00

State: **running**. Run **boole-preparation-20261110-17-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,096,552,448**.
New replicated logical patches: **8,552,448** in 33,408 chunks.
Combined verified selected patches, including parents: **8,552,448**.
Fresh interval: `[8088000000, 8152000000]`; replicated: `[8088000000, 8096552448]`.
Local cursor: 8,096,755,456; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15196184068918228, 'elapsed_seconds': 894.5182708760258, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680702, 'mean_ready_depth': 0.9989609764863765, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2114, 'prepare_wall_seconds': 892.9604119984433, 'producer_wait_capacity_seconds': 0.002839479479007423, 'producer_wait_full_seconds': 517.3792041040142, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.9294223968172446, '1': 893.5888453592197}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4234, 'flush_seconds': 27.0865497024497, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,668 patches/s**; new independent GMP audits: 265.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
