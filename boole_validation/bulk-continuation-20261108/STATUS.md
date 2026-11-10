# Boole combined search

Updated: 2026-11-10T12:44:58.146150+00:00

State: **running**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,128,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7128002048]`.
Local cursor: 7,128,260,096; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.28809352446114644, 'elapsed_seconds': 9.724297380016651, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481259, 'mean_ready_depth': 1.940173506976318, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 491, 'prepare_wall_seconds': 9.713825747079682, 'producer_wait_capacity_seconds': 0.00032074208138510585, 'producer_wait_full_seconds': 4.066056108509656, 'ready': 0, 'ready_depth_seconds': {'0': 2.17737567628501, '1': 1.5201089889742434, '2': 0.7337195625877939, '3': 5.293092012172565}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 61, 'flush_seconds': 0.3551469002268277, 'pending_bytes': 55234, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,484 patches/s**; new independent GMP audits: 4.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
