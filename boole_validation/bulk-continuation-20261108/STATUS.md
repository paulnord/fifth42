# Boole combined search

Updated: 2026-11-10T14:13:01.423867+00:00

State: **running**. Run **boole-delegated-20261109-03**; gpu with 16 preparation workers.
Verified replicated cursor: **7,192,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[7192000000, 7256000000]`; replicated: `[7192000000, 7192002048]`.
Local cursor: 7,192,186,368; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.13866763788973913, 'elapsed_seconds': 9.72810427704826, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481370, 'mean_ready_depth': 2.2447082776958847, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 484, 'prepare_wall_seconds': 9.71409243758535, 'producer_wait_capacity_seconds': 0.0003152416320517659, 'producer_wait_full_seconds': 4.243171006382909, 'ready': 1, 'ready_depth_seconds': {'0': 1.3211284203571267, '1': 1.2589006674825214, '2': 0.8663668881054036, '3': 6.281707251095213}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 60, 'flush_seconds': 0.3271999011049047, 'pending_bytes': 55221, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,276 patches/s**; new independent GMP audits: 4.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
