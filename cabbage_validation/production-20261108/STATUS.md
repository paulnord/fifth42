# Cabbage combined search

Updated: 2026-11-10T12:05:45.675165+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,086,040,320**.
New replicated logical patches: **80,204,544** in 313,299 chunks.
Combined verified selected patches, including parents: **586,040,320**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1086040320]`.
Local cursor: 1,086,938,880; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1459.957300142094, 'elapsed_seconds': 3597.901629363012, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14395829865351267, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 316399, 'prepare_wall_seconds': 3596.7887560622185, 'producer_wait_capacity_seconds': 0.19574261736124754, 'producer_wait_full_seconds': 61.64389790472342, 'ready': 0, 'ready_depth_seconds': {'0': 3221.6335354296607, '1': 300.37104391120374, '2': 10.114394585893024, '3': 65.78265473427018}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 39573, 'flush_seconds': 219.85490448202472, 'pending_bytes': 107506, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,473 patches/s**; new independent GMP audits: 2,472.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
