# Boole combined search

Updated: 2026-11-12T02:40:59.471579+00:00

State: **running**. Run **boole-range-r3-20261111-22-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,415,790,848**.
New replicated logical patches: **7,790,848** in 30,433 chunks.
Combined verified selected patches, including parents: **7,790,848**.
Fresh interval: `[8408000000, 8472000000]`; replicated: `[8408000000, 8415790848]`.
Local cursor: 8,415,962,624; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1563488213578239, 'elapsed_seconds': 900.8935892230365, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681137, 'mean_ready_depth': 0.9990072234940347, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1938, 'prepare_wall_seconds': 899.1206997244153, 'producer_wait_capacity_seconds': 0.002579738269560039, 'producer_wait_full_seconds': 556.6791707924567, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.8943829598138109, '1': 899.9992032332812}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3878, 'flush_seconds': 28.571556515526026, 'pending_bytes': 19217, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,799 patches/s**; new independent GMP audits: 243.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
