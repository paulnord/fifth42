# Cabbage combined search

Updated: 2026-11-10T05:09:44.523725+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **540,486,144**.
New replicated logical patches: **40,486,144** in 158,149 chunks.
Combined verified selected patches, including parents: **40,486,144**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 540486144]`.
Local cursor: 541,254,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 734.5833160118782, 'elapsed_seconds': 1815.619265495974, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513941, 'mean_ready_depth': 0.143643334007918, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 160547, 'prepare_wall_seconds': 1815.0554652470746, 'producer_wait_capacity_seconds': 0.09893999324413016, 'producer_wait_full_seconds': 32.61649366351776, 'ready': 0, 'ready_depth_seconds': {'0': 1627.7676937116194, '1': 149.72036192228552, '2': 3.312383857613895, '3': 34.81882498244522}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 20080, 'flush_seconds': 107.57385605201125, 'pending_bytes': 69050, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,527 patches/s**; new independent GMP audits: 1,255.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
