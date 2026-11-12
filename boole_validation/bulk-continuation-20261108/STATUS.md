# Boole combined search

Updated: 2026-11-12T05:44:07.733796+00:00

State: **running**. Run **boole-range-r3-20261111-23-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,510,336,768**.
New replicated logical patches: **38,336,768** in 149,753 chunks.
Combined verified selected patches, including parents: **38,336,768**.
Fresh interval: `[8472000000, 8536000000]`; replicated: `[8472000000, 8510336768]`.
Local cursor: 8,510,566,144; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15858709963504225, 'elapsed_seconds': 4502.81691855297, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682956, 'mean_ready_depth': 0.9992850674135523, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9394, 'prepare_wall_seconds': 4500.887759619043, 'producer_wait_capacity_seconds': 0.012738641700707376, 'producer_wait_full_seconds': 2833.447574918624, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.219208225957118, '1': 4499.597708007088}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 18823, 'flush_seconds': 145.7140705616912, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,543 patches/s**; new independent GMP audits: 1,175.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
