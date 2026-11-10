# Boole combined search

Updated: 2026-11-10T17:27:42.965393+00:00

State: **running**. Run **boole-delegated-20261109-05**; gpu with 16 preparation workers.
Verified replicated cursor: **7,329,922,816**.
New replicated logical patches: **9,922,816** in 38,761 chunks.
Combined verified selected patches, including parents: **9,922,816**.
Fresh interval: `[7320000000, 7384000000]`; replicated: `[7320000000, 7329922816]`.
Local cursor: 7,330,680,576; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 10.245740393351298, 'elapsed_seconds': 906.2931148839998, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482144, 'mean_ready_depth': 2.277986098399861, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 41368, 'prepare_wall_seconds': 906.1365695924615, 'producer_wait_capacity_seconds': 0.027207726729102433, 'producer_wait_full_seconds': 427.05434669042006, 'ready': 1, 'ready_depth_seconds': {'0': 100.9727559396415, '1': 120.17859785573091, '2': 111.08076140022604, '3': 574.060998708359}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 5186, 'flush_seconds': 29.230791720969137, 'pending_bytes': 110482, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,680 patches/s**; new independent GMP audits: 324.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
