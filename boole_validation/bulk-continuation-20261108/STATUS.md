# Boole combined search

Updated: 2026-11-12T01:40:32.141585+00:00

State: **running**. Run **boole-range-r3-20261111-21-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,383,844,096**.
New replicated logical patches: **39,844,096** in 155,641 chunks.
Combined verified selected patches, including parents: **39,844,096**.
Fresh interval: `[8344000000, 8408000000]`; replicated: `[8344000000, 8383844096]`.
Local cursor: 8,384,448,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15936351846903563, 'elapsed_seconds': 4509.970874942956, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683246, 'mean_ready_depth': 0.999252695425846, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9874, 'prepare_wall_seconds': 4508.166296077776, 'producer_wait_capacity_seconds': 0.012676272075623274, 'producer_wait_full_seconds': 2763.41655953601, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.3703190841479227, '1': 4506.60055307881}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 19775, 'flush_seconds': 148.65312827855814, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,965 patches/s**; new independent GMP audits: 1,235.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
