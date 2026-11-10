# Boole combined search

Updated: 2026-11-10T06:00:54.530517+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **245,497,600**.
New replicated logical patches: **145,497,600** in 568,350 chunks.
Combined verified selected patches, including parents: **145,497,600**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 245497600]`.
Local cursor: 246,860,544; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1882.0303867598996, 'elapsed_seconds': 8124.36501878401, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 547184, 'mean_ready_depth': 0.541833808781196, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 573678, 'prepare_wall_seconds': 8120.481851781951, 'producer_wait_capacity_seconds': 0.3490958053153008, 'producer_wait_full_seconds': 1001.3920678821742, 'ready': 3, 'ready_depth_seconds': {'0': 6186.223621453857, '1': 635.136874059448, '2': 142.0947994449525, '3': 1160.9097230357002}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 71828, 'flush_seconds': 394.1222388216993, 'pending_bytes': 17360, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,075 patches/s**; new independent GMP audits: 4,482.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
