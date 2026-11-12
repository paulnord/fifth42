# Boole combined search

Updated: 2026-11-12T19:12:29.094973+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,896,140,800**.
New replicated logical patches: **40,140,800** in 156,800 chunks.
Combined verified selected patches, including parents: **40,140,800**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8896140800]`.
Local cursor: 8,896,665,088; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16272745421156287, 'elapsed_seconds': 5419.189114548033, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681661, 'mean_ready_depth': 0.9993972823666584, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9914, 'prepare_wall_seconds': 5416.859483233653, 'producer_wait_capacity_seconds': 0.013339265948161483, 'producer_wait_full_seconds': 3673.7618364751106, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.266238317708485, '1': 5415.922873710282}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 19870, 'flush_seconds': 148.83668106934056, 'pending_bytes': 19823, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,491 patches/s**; new independent GMP audits: 1,240.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
