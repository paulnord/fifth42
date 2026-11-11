# Boole combined search

Updated: 2026-11-11T17:52:16.315239+00:00

State: **stopped**. Run **boole-range-r3-20261111-18**; gpu with 16 preparation workers.
Verified replicated cursor: **8,216,000,000**.
New replicated logical patches: **26,382,080** in 103,055 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[8189617920, 8216000000]`; replicated: `[8189617920, 8216000000]`.
Local cursor: 8,216,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.17139336321270093, 'elapsed_seconds': 2812.0716141419834, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682831, 'mean_ready_depth': 0.998550616844679, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6441, 'prepare_wall_seconds': 2810.1137807115447, 'producer_wait_capacity_seconds': 0.008222190954256803, 'producer_wait_full_seconds': 1670.5469580680365, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 4.075766089139506, '1': 2807.99584491289}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 12908, 'flush_seconds': 92.16134169959696, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,381 patches/s**; new independent GMP audits: 806.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
