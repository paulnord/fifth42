# Boole combined search

Updated: 2026-11-12T10:27:57.274876+00:00

State: **running**. Run **boole-range-r3-20261111-25-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,651,394,816**.
New replicated logical patches: **51,394,816** in 200,761 chunks.
Combined verified selected patches, including parents: **51,394,816**.
Fresh interval: `[8600000000, 8664000000]`; replicated: `[8600000000, 8651394816]`.
Local cursor: 8,651,912,960; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.17581949185114354, 'elapsed_seconds': 6318.866971818963, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682614, 'mean_ready_depth': 0.9993260510730215, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 12674, 'prepare_wall_seconds': 6316.741671000258, 'producer_wait_capacity_seconds': 0.01659728994127363, 'producer_wait_full_seconds': 4068.2962436109083, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.258591405348852, '1': 6314.608378203586}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 25402, 'flush_seconds': 196.8837788143428, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,214 patches/s**; new independent GMP audits: 1,585.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
