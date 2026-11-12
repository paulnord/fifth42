# Boole combined search

Updated: 2026-11-12T19:57:45.785802+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,916,432,640**.
New replicated logical patches: **60,432,640** in 236,065 chunks.
Combined verified selected patches, including parents: **60,432,640**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8916432640]`.
Local cursor: 8,916,815,616; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16936501825693995, 'elapsed_seconds': 8135.401038137032, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682238, 'mean_ready_depth': 0.9994166860744754, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14834, 'prepare_wall_seconds': 8132.8852070394205, 'producer_wait_capacity_seconds': 0.01997730357106775, 'producer_wait_full_seconds': 5520.1062248375965, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.74549006531015, '1': 8130.65554542176}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 29729, 'flush_seconds': 221.6623042782303, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,467 patches/s**; new independent GMP audits: 1,855.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
