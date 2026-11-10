# Boole combined search

Updated: 2026-11-10T20:00:03.394201+00:00

State: **running**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,434,792,704**.
New replicated logical patches: **50,792,704** in 198,409 chunks.
Combined verified selected patches, including parents: **50,792,704**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7434792704]`.
Local cursor: 7,435,419,392; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 76.3044707768131, 'elapsed_seconds': 4547.565251394, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 487141, 'mean_ready_depth': 2.131482017397401, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 200452, 'prepare_wall_seconds': 4545.79533505271, 'producer_wait_capacity_seconds': 0.12993988051312044, 'producer_wait_full_seconds': 2124.240782347566, 'ready': 3, 'ready_depth_seconds': {'0': 708.6856709900894, '1': 674.650421987637, '2': 474.28433722886257, '3': 2689.9448199474136}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 25121, 'flush_seconds': 151.31905516062398, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,283 patches/s**; new independent GMP audits: 1,567.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
