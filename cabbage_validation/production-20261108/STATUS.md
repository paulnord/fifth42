# Cabbage combined search

Updated: 2026-11-10T15:06:21.197006+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,325,827,840**.
New replicated logical patches: **319,992,064** in 1,249,969 chunks.
Combined verified selected patches, including parents: **825,827,840**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1325827840]`.
Local cursor: 1,327,091,456; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5896.883794829948, 'elapsed_seconds': 14437.27559221402, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.1475874050666327, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1254821, 'prepare_wall_seconds': 14432.853891285718, 'producer_wait_capacity_seconds': 0.7791747556184418, 'producer_wait_full_seconds': 256.9997584067751, 'ready': 0, 'ready_depth_seconds': {'0': 12916.021842578019, '1': 1188.934302403708, '2': 55.13260036089923, '3': 277.1868459203979}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 156948, 'flush_seconds': 881.6060942861368, 'pending_bytes': 71784, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,241 patches/s**; new independent GMP audits: 9,804.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
