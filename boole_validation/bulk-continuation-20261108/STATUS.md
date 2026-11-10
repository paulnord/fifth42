# Boole combined search

Updated: 2026-11-10T13:14:57.822024+00:00

State: **running**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,149,846,272**.
New replicated logical patches: **21,846,272** in 85,337 chunks.
Combined verified selected patches, including parents: **21,846,272**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7149846272]`.
Local cursor: 7,150,198,528; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 27.621709241881035, 'elapsed_seconds': 1816.310171124991, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482055, 'mean_ready_depth': 2.159715377734192, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 86548, 'prepare_wall_seconds': 1815.999695845414, 'producer_wait_capacity_seconds': 0.056737538950983435, 'producer_wait_full_seconds': 812.8819516454823, 'ready': 2, 'ready_depth_seconds': {'0': 259.3639766041306, '1': 271.46425977081526, '2': 205.19705373729812, '3': 1080.2848800227512}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 10832, 'flush_seconds': 60.75715547258733, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,196 patches/s**; new independent GMP audits: 677.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
