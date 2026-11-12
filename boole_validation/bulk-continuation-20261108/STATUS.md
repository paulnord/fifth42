# Boole combined search

Updated: 2026-11-12T04:26:22.160704+00:00

State: **running**. Run **boole-range-r3-20261111-22-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,470,630,144**.
New replicated logical patches: **62,630,144** in 244,649 chunks.
Combined verified selected patches, including parents: **62,630,144**.
Fresh interval: `[8408000000, 8472000000]`; replicated: `[8408000000, 8470630144]`.
Local cursor: 8,471,043,840; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.17431987926829606, 'elapsed_seconds': 7216.650670142029, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7688034, 'mean_ready_depth': 0.9993004405176062, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15370, 'prepare_wall_seconds': 7214.6983404972125, 'producer_wait_capacity_seconds': 0.020503719919361174, 'producer_wait_full_seconds': 4492.02402071387, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.048474427429028, '1': 7211.602193734609}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 30791, 'flush_seconds': 233.37566940952092, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,722 patches/s**; new independent GMP audits: 1,922.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
