# Cabbage combined search

Updated: 2026-11-10T06:40:02.473951+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **661,880,320**.
New replicated logical patches: **161,880,320** in 632,345 chunks.
Combined verified selected patches, including parents: **161,880,320**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 661880320]`.
Local cursor: 663,133,184; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2925.7731761650066, 'elapsed_seconds': 7235.234589539003, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514000, 'mean_ready_depth': 0.1409704037165782, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 636799, 'prepare_wall_seconds': 7233.028724006435, 'producer_wait_capacity_seconds': 0.3914168025366962, 'producer_wait_full_seconds': 126.37521477916744, 'ready': 0, 'ready_depth_seconds': {'0': 6500.172395573405, '1': 585.7855069698417, '2': 13.661623909545597, '3': 135.61506209417712}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 79654, 'flush_seconds': 425.3431657036417, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,504 patches/s**; new independent GMP audits: 4,975.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
