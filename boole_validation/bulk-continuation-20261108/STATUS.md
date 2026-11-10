# Boole combined search

Updated: 2026-11-10T06:46:02.754947+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **296,364,800**.
New replicated logical patches: **196,364,800** in 767,050 chunks.
Combined verified selected patches, including parents: **196,364,800**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 296364800]`.
Local cursor: 296,862,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2446.6802824691986, 'elapsed_seconds': 10831.665520632, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 547184, 'mean_ready_depth': 0.5548648076721772, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 768842, 'prepare_wall_seconds': 10829.034105054452, 'producer_wait_capacity_seconds': 0.46919143927516416, 'producer_wait_full_seconds': 1366.905426853802, 'ready': 1, 'ready_depth_seconds': {'0': 8186.264730502153, '1': 868.7695851694443, '2': 188.55319069576217, '3': 1588.0780131046195}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 96262, 'flush_seconds': 527.5229921059217, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,170 patches/s**; new independent GMP audits: 6,007.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
