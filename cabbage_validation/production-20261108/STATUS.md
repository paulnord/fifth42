# Cabbage combined search

Updated: 2026-11-11T18:45:40.338650+00:00

State: **running**. Run **cabbage-extended-r3-cap100-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,301,989,120**.
New replicated logical patches: **61,989,120** in 242,145 chunks.
Combined verified selected patches, including parents: **61,989,120**.
Fresh interval: `[9240000000, 9304000000]`; replicated: `[9240000000, 9301989120]`.
Local cursor: 9,302,290,176; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2024.719041802222, 'elapsed_seconds': 6049.578221638978, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3844354, 'mean_ready_depth': 0.2611516600097341, 'outstanding': 1, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 60734, 'prepare_wall_seconds': 6049.30475840671, 'producer_wait_capacity_seconds': 0.04376041243085638, 'producer_wait_full_seconds': 1287.789176847029, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 4469.7208260782645, '1': 1579.8573949397542}, 'ready_limit': 1, 'reserved_bytes': 12582912}; buffer: {'flush_count': 30416, 'flush_seconds': 312.4831854471704, 'pending_bytes': 246998, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,280 patches/s**; new independent GMP audits: 1,898.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
