# Cabbage combined search

Updated: 2026-11-10T15:36:28.634158+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,365,367,552**.
New replicated logical patches: **359,531,776** in 1,404,421 chunks.
Combined verified selected patches, including parents: **865,367,552**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1365367552]`.
Local cursor: 1,366,446,848; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6628.841165299644, 'elapsed_seconds': 16239.40811137599, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.1498483006648479, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1408033, 'prepare_wall_seconds': 16234.440930338693, 'producer_wait_capacity_seconds': 0.875136861752253, 'producer_wait_full_seconds': 300.0495146653848, 'ready': 0, 'ready_depth_seconds': {'0': 14517.561813380744, '1': 1333.6166999660782, '2': 64.85778178501641, '3': 323.371815252176}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 176108, 'flush_seconds': 1001.3832685687812, 'pending_bytes': 71772, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,188 patches/s**; new independent GMP audits: 11,001.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
