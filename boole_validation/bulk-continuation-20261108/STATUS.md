# Boole combined search

Updated: 2026-11-10T08:21:09.284662+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **400,719,360**.
New replicated logical patches: **100,719,360** in 393,435 chunks.
Combined verified selected patches, including parents: **100,719,360**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 400719360]`.
Local cursor: 401,648,128; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1138.0982417284395, 'elapsed_seconds': 5424.7171092100325, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513930, 'mean_ready_depth': 0.579783742759612, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 396637, 'prepare_wall_seconds': 5423.342031766311, 'producer_wait_capacity_seconds': 0.24317798897391185, 'producer_wait_full_seconds': 707.6868341235677, 'ready': 0, 'ready_depth_seconds': {'0': 4024.6692749390495, '1': 481.25057818111964, '2': 92.4795553307631, '3': 826.3177000490832}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 49663, 'flush_seconds': 259.04112865013303, 'pending_bytes': 103498, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,714 patches/s**; new independent GMP audits: 3,099.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
