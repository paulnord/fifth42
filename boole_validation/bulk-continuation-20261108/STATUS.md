# Boole combined search

Updated: 2026-11-10T00:00:59.941074+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,512,939,520**.
New replicated logical patches: **42,536,448** in 166,158 chunks.
Combined verified selected patches, including parents: **512,939,520**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3512939520]`.
Local cursor: 3,513,227,008; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 287.9241662856075, 'elapsed_seconds': 2344.8980234399787, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9697956829056804, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 166705, 'prepare_wall_seconds': 2344.305464364472, 'producer_wait_capacity_seconds': 0.10484239365905523, 'producer_wait_full_seconds': 434.86985761113465, 'ready': 0, 'ready_depth_seconds': {'0': 1304.231935190095, '1': 367.7266056351946, '2': 112.47306926321471, '3': 560.4664119415102}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 20867, 'flush_seconds': 120.10140940052224, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,190 patches/s**; new independent GMP audits: 1,303.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
