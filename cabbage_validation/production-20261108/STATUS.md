# Cabbage combined search

Updated: 2026-11-10T23:30:05.049064+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,090,653,184**.
New replicated logical patches: **551,804,160** in 2,155,485 chunks.
Combined verified selected patches, including parents: **1,590,653,184**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2090653184]`.
Local cursor: 2,092,019,200; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1958.233028400049, 'elapsed_seconds': 13108.002644778986, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.22271762320712526, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 135042, 'prepare_wall_seconds': 13107.400008082448, 'producer_wait_capacity_seconds': 0.0993103992077522, 'producer_wait_full_seconds': 380.77037541766185, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 10188.619448927057, '1': 2919.3831940378877}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 270364, 'flush_seconds': 1551.5405699180556, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,180 patches/s**; new independent GMP audits: 16,881.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
