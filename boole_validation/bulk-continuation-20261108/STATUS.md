# Boole combined search

Updated: 2026-11-10T06:30:54.929043+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **278,529,792**.
New replicated logical patches: **178,529,792** in 697,382 chunks.
Combined verified selected patches, including parents: **178,529,792**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 278529792]`.
Local cursor: 280,049,920; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2260.5037276016083, 'elapsed_seconds': 9918.480008278973, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 547184, 'mean_ready_depth': 0.5502466740186597, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 703074, 'prepare_wall_seconds': 9916.070535077539, 'producer_wait_capacity_seconds': 0.4286966227227822, 'producer_wait_full_seconds': 1241.0941103294608, 'ready': 0, 'ready_depth_seconds': {'0': 7515.264055955922, '1': 789.6898199314601, '2': 172.65757955011213, '3': 1440.868552281463}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 88028, 'flush_seconds': 482.404556938156, 'pending_bytes': 68986, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,145 patches/s**; new independent GMP audits: 5,493.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
