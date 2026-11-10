# Cabbage combined search

Updated: 2026-11-10T05:24:49.905321+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **560,567,040**.
New replicated logical patches: **60,567,040** in 236,590 chunks.
Combined verified selected patches, including parents: **60,567,040**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 560567040]`.
Local cursor: 561,659,392; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1096.621434404049, 'elapsed_seconds': 2717.843367844005, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513941, 'mean_ready_depth': 0.14179972452282488, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 240022, 'prepare_wall_seconds': 2717.0070140526514, 'producer_wait_capacity_seconds': 0.14829205517889932, 'producer_wait_full_seconds': 47.689161989372224, 'ready': 0, 'ready_depth_seconds': {'0': 2439.0299178520218, '1': 223.2192871948355, '2': 4.612332293647341, '3': 50.981829691445455}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 30020, 'flush_seconds': 159.51444686419563, 'pending_bytes': 86306, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,535 patches/s**; new independent GMP audits: 1,876.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
