# Boole combined search

Updated: 2026-11-11T21:30:12.174352+00:00

State: **running**. Run **boole-range-r3-20261111-19-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,248,848,128**.
New replicated logical patches: **32,848,128** in 128,313 chunks.
Combined verified selected patches, including parents: **32,848,128**.
Fresh interval: `[8216000000, 8280000000]`; replicated: `[8216000000, 8248848128]`.
Local cursor: 8,249,487,104; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1505247433669865, 'elapsed_seconds': 3617.536608105991, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682227, 'mean_ready_depth': 0.9992415784231499, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8157, 'prepare_wall_seconds': 3617.3660108242766, 'producer_wait_capacity_seconds': 0.010753973212558776, 'producer_wait_full_seconds': 2167.263180798618, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.7436154586612247, '1': 3614.7929902873584}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 16348, 'flush_seconds': 121.82262524915859, 'pending_bytes': 57664, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,233 patches/s**; new independent GMP audits: 1,020.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
