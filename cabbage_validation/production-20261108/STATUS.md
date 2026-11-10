# Cabbage combined search

Updated: 2026-11-10T00:31:31.421831+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,672,076,672**.
New replicated logical patches: **99,583,744** in 388,999 chunks.
Combined verified selected patches, including parents: **422,076,672**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2672076672]`.
Local cursor: 2,672,542,336; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1347.9752864465117, 'elapsed_seconds': 4327.294916143001, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.3286058972125747, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 390683, 'prepare_wall_seconds': 4325.930385259388, 'producer_wait_capacity_seconds': 0.25220638659084216, 'producer_wait_full_seconds': 162.0311754840077, 'ready': 1, 'ready_depth_seconds': {'0': 3436.4245433249744, '1': 585.2171732886927, '2': 80.20214047800982, '3': 225.45105805929052}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 48862, 'flush_seconds': 282.7297368059517, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,101 patches/s**; new independent GMP audits: 3,053.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
