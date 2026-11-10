# Cabbage combined search

Updated: 2026-11-10T10:25:38.339381+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **961,598,720**.
New replicated logical patches: **461,598,720** in 1,803,120 chunks.
Combined verified selected patches, including parents: **461,598,720**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 961598720]`.
Local cursor: 962,860,288; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8440.903462099901, 'elapsed_seconds': 20771.80405945296, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.13910346833182025, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1807664, 'prepare_wall_seconds': 20765.569484463893, 'producer_wait_capacity_seconds': 1.1141843622317538, 'producer_wait_full_seconds': 363.83765176456654, 'ready': 0, 'ready_depth_seconds': {'0': 18711.473038007738, '1': 1623.4455229901941, '2': 44.67202738346532, '3': 392.21347014058847}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 226105, 'flush_seconds': 1222.4128194618388, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,269 patches/s**; new independent GMP audits: 14,123.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
