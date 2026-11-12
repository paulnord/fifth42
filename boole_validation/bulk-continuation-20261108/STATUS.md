# Boole combined search

Updated: 2026-11-12T19:27:42.111881+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,903,380,736**.
New replicated logical patches: **47,380,736** in 185,081 chunks.
Combined verified selected patches, including parents: **47,380,736**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8903380736]`.
Local cursor: 8,903,446,272; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1649807601934299, 'elapsed_seconds': 6335.848431707011, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681661, 'mean_ready_depth': 0.9994057561355821, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11578, 'prepare_wall_seconds': 6333.418229124742, 'producer_wait_capacity_seconds': 0.015600076294504106, 'producer_wait_full_seconds': 4296.674386467668, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.765036586439237, '1': 6332.0833926505875}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 23202, 'flush_seconds': 174.47007847379427, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,483 patches/s**; new independent GMP audits: 1,448.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
