# Cabbage combined search

Updated: 2026-11-10T14:21:17.793055+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,266,524,672**.
New replicated logical patches: **260,688,896** in 1,018,316 chunks.
Combined verified selected patches, including parents: **766,524,672**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1266524672]`.
Local cursor: 1,267,558,144; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4788.516507042164, 'elapsed_seconds': 11732.594611669017, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.1473798806396607, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1022122, 'prepare_wall_seconds': 11728.996373314352, 'producer_wait_capacity_seconds': 0.6341710906708613, 'producer_wait_full_seconds': 209.34188118652673, 'ready': 1, 'ready_depth_seconds': {'0': 10495.96454166784, '1': 969.3117231742362, '2': 42.11836709768977, '3': 225.1999786972301}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 127845, 'flush_seconds': 715.7504215996014, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,290 patches/s**; new independent GMP audits: 7,986.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
