# Boole combined search

Updated: 2026-11-10T00:31:11.678834+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,544,981,504**.
New replicated logical patches: **74,578,432** in 291,322 chunks.
Combined verified selected patches, including parents: **544,981,504**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3544981504]`.
Local cursor: 3,545,950,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 516.1079233126948, 'elapsed_seconds': 4156.245149214985, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9661828948467988, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 294511, 'prepare_wall_seconds': 4155.2080041902955, 'producer_wait_capacity_seconds': 0.1851560139330104, 'producer_wait_full_seconds': 770.2947879076819, 'ready': 0, 'ready_depth_seconds': {'0': 2318.7218686430133, '1': 648.6772421901114, '2': 199.52238500420935, '3': 989.3236525876564}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 36873, 'flush_seconds': 212.85766302794218, 'pending_bytes': 91107, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,134 patches/s**; new independent GMP audits: 2,301.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
