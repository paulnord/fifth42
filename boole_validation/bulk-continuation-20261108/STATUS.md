# Boole combined search

Updated: 2026-11-12T06:49:48.659468+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,543,436,544**.
New replicated logical patches: **7,436,544** in 29,049 chunks.
Combined verified selected patches, including parents: **7,436,544**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8543436544]`.
Local cursor: 8,543,698,688; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15167598892003298, 'elapsed_seconds': 899.4312916509807, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680725, 'mean_ready_depth': 0.9990293496634375, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1866, 'prepare_wall_seconds': 897.5083938123425, 'producer_wait_capacity_seconds': 0.0025000368477776647, 'producer_wait_full_seconds': 568.2637005562428, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.8730305159697309, '1': 898.5582583650248}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3732, 'flush_seconds': 26.987489114049822, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,486 patches/s**; new independent GMP audits: 234.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
