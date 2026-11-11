# Boole combined search

Updated: 2026-11-11T15:36:16.427185+00:00

State: **running**. Run **boole-preparation-20261110-17-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,148,496,128**.
New replicated logical patches: **60,496,128** in 236,313 chunks.
Combined verified selected patches, including parents: **60,496,128**.
Fresh interval: `[8088000000, 8152000000]`; replicated: `[8088000000, 8148496128]`.
Local cursor: 8,148,586,240; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16942196589661762, 'elapsed_seconds': 6317.879261757014, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683578, 'mean_ready_depth': 0.9992316425303529, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14786, 'prepare_wall_seconds': 6316.217810188769, 'producer_wait_capacity_seconds': 0.019391928741242737, 'producer_wait_full_seconds': 3678.0102084126556, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.85438244312536, '1': 6313.024872033915}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 29618, 'flush_seconds': 215.18261538509978, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,584 patches/s**; new independent GMP audits: 1,849.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
