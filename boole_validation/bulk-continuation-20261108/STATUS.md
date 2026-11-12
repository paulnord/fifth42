# Boole combined search

Updated: 2026-11-12T17:23:36.702673+00:00

State: **running**. Run **boole-range-r3-20261111-28-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,847,685,376**.
New replicated logical patches: **55,685,376** in 217,521 chunks.
Combined verified selected patches, including parents: **55,685,376**.
Fresh interval: `[8792000000, 8856000000]`; replicated: `[8792000000, 8847685376]`.
Local cursor: 8,847,965,952; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1614899004343897, 'elapsed_seconds': 7220.8342584799975, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681953, 'mean_ready_depth': 0.9993962683815393, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13642, 'prepare_wall_seconds': 7218.514416096266, 'producer_wait_capacity_seconds': 0.01798388478346169, 'producer_wait_full_seconds': 4820.06397785875, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.359443593537435, '1': 7216.474812526489}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 27335, 'flush_seconds': 204.00672425422817, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,737 patches/s**; new independent GMP audits: 1,706.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
