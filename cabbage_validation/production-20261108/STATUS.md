# Cabbage combined search

Updated: 2026-11-10T05:39:50.574083+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **580,548,096**.
New replicated logical patches: **80,548,096** in 314,641 chunks.
Combined verified selected patches, including parents: **80,548,096**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 580548096]`.
Local cursor: 581,935,616; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1458.4293538347702, 'elapsed_seconds': 3619.0512257109513, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513941, 'mean_ready_depth': 0.14194530641699366, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 319302, 'prepare_wall_seconds': 3617.946708557196, 'producer_wait_capacity_seconds': 0.1968427278334275, 'producer_wait_full_seconds': 63.46990342257777, 'ready': 1, 'ready_depth_seconds': {'0': 3247.2659891246585, '1': 297.6905662389472, '2': 6.267239495762624, '3': 67.82742998062167}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 39940, 'flush_seconds': 213.73803533473983, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,531 patches/s**; new independent GMP audits: 2,495.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
