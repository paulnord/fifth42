# Boole combined search

Updated: 2026-11-11T10:10:38.447746+00:00

State: **running**. Run **boole-preparation-20261110-14-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,959,273,216**.
New replicated logical patches: **63,273,216** in 247,161 chunks.
Combined verified selected patches, including parents: **63,273,216**.
Fresh interval: `[7896000000, 7960000000]`; replicated: `[7896000000, 7959273216]`.
Local cursor: 7,959,414,528; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16708774241851643, 'elapsed_seconds': 6327.137544624042, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681255, 'mean_ready_depth': 0.9991365578808173, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15474, 'prepare_wall_seconds': 6325.614587423508, 'producer_wait_capacity_seconds': 0.019862124288920313, 'producer_wait_full_seconds': 3545.4248761087656, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.463114499871153, '1': 6321.674427574151}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 30994, 'flush_seconds': 223.73342764761765, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,016 patches/s**; new independent GMP audits: 1,935.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
