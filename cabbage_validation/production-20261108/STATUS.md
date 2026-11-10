# Cabbage combined search

Updated: 2026-11-10T08:40:18.090052+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **821,735,936**.
New replicated logical patches: **321,735,936** in 1,256,781 chunks.
Combined verified selected patches, including parents: **321,735,936**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 821735936]`.
Local cursor: 823,599,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5859.3481244912255, 'elapsed_seconds': 14450.438965901965, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514228, 'mean_ready_depth': 0.14049844131320882, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1263642, 'prepare_wall_seconds': 14446.084885255259, 'producer_wait_capacity_seconds': 0.7764402914326638, 'producer_wait_full_seconds': 254.28646649623988, 'ready': 0, 'ready_depth_seconds': {'0': 12998.627505746437, '1': 1147.4703514028224, '2': 30.22952389717102, '3': 274.111583934573}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 158063, 'flush_seconds': 850.6823385200696, 'pending_bytes': 69814, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,373 patches/s**; new independent GMP audits: 9,873.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
