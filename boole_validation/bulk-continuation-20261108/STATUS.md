# Boole combined search

Updated: 2026-11-10T05:30:51.378427+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **212,897,280**.
New replicated logical patches: **112,897,280** in 441,005 chunks.
Combined verified selected patches, including parents: **112,897,280**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 212897280]`.
Local cursor: 214,360,320; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1461.5890886461711, 'elapsed_seconds': 6319.96239075996, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 546935, 'mean_ready_depth': 0.5435481149865407, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 446578, 'prepare_wall_seconds': 6318.423617412685, 'producer_wait_capacity_seconds': 0.27184069610666484, 'producer_wait_full_seconds': 783.0514054447412, 'ready': 3, 'ready_depth_seconds': {'0': 4807.758223266224, '1': 495.3575745195267, '2': 110.69370696879923, '3': 906.1528852754273}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 55915, 'flush_seconds': 306.63406004267745, 'pending_bytes': 120225, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,086 patches/s**; new independent GMP audits: 3,489.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
