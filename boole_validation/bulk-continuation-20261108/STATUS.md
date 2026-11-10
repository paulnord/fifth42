# Boole combined search

Updated: 2026-11-10T09:36:16.485560+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **483,890,944**.
New replicated logical patches: **183,890,944** in 718,324 chunks.
Combined verified selected patches, including parents: **183,890,944**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 483890944]`.
Local cursor: 485,373,184; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2073.3024699905654, 'elapsed_seconds': 9925.730000926007, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514009, 'mean_ready_depth': 0.5799241453873828, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 723556, 'prepare_wall_seconds': 9923.233696620213, 'producer_wait_capacity_seconds': 0.4433845493476838, 'producer_wait_full_seconds': 1290.3086883081123, 'ready': 0, 'ready_depth_seconds': {'0': 7359.800212991366, '1': 883.8502196508343, '2': 173.91843426931882, '3': 1508.1611333144829}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 90587, 'flush_seconds': 480.0010922672227, 'pending_bytes': 120756, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,660 patches/s**; new independent GMP audits: 5,653.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
