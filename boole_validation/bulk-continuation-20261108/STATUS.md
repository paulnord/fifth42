# Boole combined search

Updated: 2026-11-10T10:35:28.533266+00:00

State: **running**. Run **boole-delegated-20261109-00**; gpu with 16 preparation workers.
Verified replicated cursor: **7,032,676,096**.
New replicated logical patches: **32,676,096** in 127,641 chunks.
Combined verified selected patches, including parents: **32,676,096**.
Fresh interval: `[7000000000, 7064000000]`; replicated: `[7000000000, 7032676096]`.
Local cursor: 7,033,585,408; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 50.90951282688184, 'elapsed_seconds': 2709.4320226430427, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482240, 'mean_ready_depth': 2.075999181088279, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 131099, 'prepare_wall_seconds': 2708.959643745562, 'producer_wait_capacity_seconds': 0.08411981485551223, 'producer_wait_full_seconds': 1187.5708098280593, 'ready': 2, 'ready_depth_seconds': {'0': 452.2601465078769, '1': 430.79545306565706, '2': 285.1460590828792, '3': 1541.2303629966336}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 16410, 'flush_seconds': 93.04351596377091, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,385 patches/s**; new independent GMP audits: 1,025.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
