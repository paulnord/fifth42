# Boole combined search

Updated: 2026-11-12T20:20:56.207031+00:00

State: **running**. Run **boole-range-r3-20261111-30-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,926,519,040**.
New replicated logical patches: **6,519,040** in 25,465 chunks.
Combined verified selected patches, including parents: **6,519,040**.
Fresh interval: `[8920000000, 8984000000]`; replicated: `[8920000000, 8926519040]`.
Local cursor: 8,926,713,600; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14850081142503768, 'elapsed_seconds': 902.6447634060169, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680345, 'mean_ready_depth': 0.9991249845157999, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1634, 'prepare_wall_seconds': 900.284615042503, 'producer_wait_capacity_seconds': 0.002204065560363233, 'producer_wait_full_seconds': 613.0415173784131, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.7898251047590747, '1': 901.8549352613045}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3270, 'flush_seconds': 24.58886334032286, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,403 patches/s**; new independent GMP audits: 205.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
