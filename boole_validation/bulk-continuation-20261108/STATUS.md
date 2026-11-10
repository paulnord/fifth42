# Boole combined search

Updated: 2026-11-10T10:20:24.448499+00:00

State: **running**. Run **boole-delegated-20261109-00**; gpu with 16 preparation workers.
Verified replicated cursor: **7,022,051,072**.
New replicated logical patches: **22,051,072** in 86,137 chunks.
Combined verified selected patches, including parents: **22,051,072**.
Fresh interval: `[7000000000, 7064000000]`; replicated: `[7000000000, 7022051072]`.
Local cursor: 7,022,444,288; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 33.26724126224872, 'elapsed_seconds': 1799.705125499051, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482003, 'mean_ready_depth': 2.0825620236004996, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 87217, 'prepare_wall_seconds': 1799.3934738191892, 'producer_wait_capacity_seconds': 0.056115484330803156, 'producer_wait_full_seconds': 787.6435643273289, 'ready': 1, 'ready_depth_seconds': {'0': 295.75187859433936, '1': 286.9340551412897, '2': 189.99408004793804, '3': 1027.025110935443}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 10909, 'flush_seconds': 61.56892555928789, 'pending_bytes': 128893, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,403 patches/s**; new independent GMP audits: 682.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
