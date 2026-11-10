# Boole combined search

Updated: 2026-11-10T06:49:23.858243+00:00

State: **stopped**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **299,326,976**.
New replicated logical patches: **199,326,976** in 778,621 chunks.
Combined verified selected patches, including parents: **199,326,976**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 299326976]`.
Local cursor: 300,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2481.9102070045774, 'elapsed_seconds': 11000.581962630968, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 547184, 'mean_ready_depth': 0.5547099390914889, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 781250, 'prepare_wall_seconds': 10997.824758315575, 'producer_wait_capacity_seconds': 0.47687321656849235, 'producer_wait_full_seconds': 1387.4000739699695, 'ready': 0, 'ready_depth_seconds': {'0': 8313.793526060646, '1': 883.4998316687997, '2': 191.23349000146845, '3': 1612.055112930073}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 97816, 'flush_seconds': 535.9066682014964, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,179 patches/s**; new independent GMP audits: 6,104.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
