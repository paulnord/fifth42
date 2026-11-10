# Cabbage combined search

Updated: 2026-11-10T04:39:36.264097+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **500,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 500002048]`.
Local cursor: 500,331,776; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4.621031777001917, 'elapsed_seconds': 11.20149012899492, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513010, 'mean_ready_depth': 0.08905726519936864, 'outstanding': 1, 'peak_outstanding': 4, 'peak_ready': 2, 'peak_reserved_bytes': 33554432, 'preparation_batches': 1039, 'prepare_wall_seconds': 11.187204847286921, 'producer_wait_capacity_seconds': 0.000603390159085393, 'producer_wait_full_seconds': 0.0009645865065976977, 'ready': 0, 'ready_depth_seconds': {'0': 10.213105273898691, '1': 0.9791931671206839, '2': 0.009190454962663352}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 129, 'flush_seconds': 0.6757434029132128, 'pending_bytes': 120776, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **13,202 patches/s**; new independent GMP audits: 9.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
