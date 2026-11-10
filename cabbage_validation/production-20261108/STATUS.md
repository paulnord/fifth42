# Cabbage combined search

Updated: 2026-11-10T08:10:12.228501+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **782,575,360**.
New replicated logical patches: **282,575,360** in 1,103,810 chunks.
Combined verified selected patches, including parents: **282,575,360**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 782575360]`.
Local cursor: 783,587,072; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5127.0946502805455, 'elapsed_seconds': 12647.207393205957, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514228, 'mean_ready_depth': 0.14064695293014334, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1107531, 'prepare_wall_seconds': 12643.396350019146, 'producer_wait_capacity_seconds': 0.680682736390736, 'producer_wait_full_seconds': 222.6101092674071, 'ready': 1, 'ready_depth_seconds': {'0': 11373.753173660254, '1': 1007.91783770459, '2': 25.735797082073987, '3': 239.80058368708706}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 138537, 'flush_seconds': 743.4111420002882, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,403 patches/s**; new independent GMP audits: 8,653.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
