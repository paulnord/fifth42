# Boole combined search

Updated: 2026-11-12T17:08:30.757099+00:00

State: **running**. Run **boole-range-r3-20261111-28-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,840,834,816**.
New replicated logical patches: **48,834,816** in 190,761 chunks.
Combined verified selected patches, including parents: **48,834,816**.
Fresh interval: `[8792000000, 8856000000]`; replicated: `[8792000000, 8840834816]`.
Local cursor: 8,841,051,904; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15924815472681075, 'elapsed_seconds': 6324.20576748508, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681953, 'mean_ready_depth': 0.9993904087399174, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11970, 'prepare_wall_seconds': 6321.8923084241105, 'producer_wait_capacity_seconds': 0.015783292474225163, 'producer_wait_full_seconds': 4218.918391892454, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.855177932768129, '1': 6320.350586922257}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 23980, 'flush_seconds': 178.1211604111595, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,751 patches/s**; new independent GMP audits: 1,497.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
