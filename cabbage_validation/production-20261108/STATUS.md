# Cabbage combined search

Updated: 2026-11-10T04:54:37.888672+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **519,294,208**.
New replicated logical patches: **19,294,208** in 75,368 chunks.
Combined verified selected patches, including parents: **19,294,208**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 519294208]`.
Local cursor: 520,734,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 368.7263627850916, 'elapsed_seconds': 913.8886304689804, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513710, 'mean_ready_depth': 0.1405715058143116, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 80879, 'prepare_wall_seconds': 913.5992308282293, 'producer_wait_capacity_seconds': 0.049730844621080905, 'producer_wait_full_seconds': 14.955810849845875, 'ready': 0, 'ready_depth_seconds': {'0': 819.4398318415042, '1': 76.55352892819792, '2': 1.7726350483717397, '3': 16.122633968887385}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 10113, 'flush_seconds': 54.62373966618907, 'pending_bytes': 103569, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,438 patches/s**; new independent GMP audits: 632.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
