# Boole combined search

Updated: 2026-11-11T08:55:27.134838+00:00

State: **running**. Run **boole-preparation-20261110-14-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,914,053,376**.
New replicated logical patches: **18,053,376** in 70,521 chunks.
Combined verified selected patches, including parents: **18,053,376**.
Fresh interval: `[7896000000, 7960000000]`; replicated: `[7896000000, 7914053376]`.
Local cursor: 7,914,315,520; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.15236571559216827, 'elapsed_seconds': 1814.3531680470333, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681075, 'mean_ready_depth': 0.9990395526089516, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4463, 'prepare_wall_seconds': 1814.1177939569461, 'producer_wait_capacity_seconds': 0.005748877709265798, 'producer_wait_full_seconds': 1013.3143238030025, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.7425883866962977, '1': 1812.610577280342}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 8943, 'flush_seconds': 63.54674478038214, 'pending_bytes': 133360, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,070 patches/s**; new independent GMP audits: 558.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
