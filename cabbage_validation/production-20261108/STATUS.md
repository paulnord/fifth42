# Cabbage combined search

Updated: 2026-11-12T03:25:56.508830+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-40**; gpu with 16 preparation workers.
Verified replicated cursor: **9,616,965,376**.
New replicated logical patches: **56,965,376** in 222,521 chunks.
Combined verified selected patches, including parents: **56,965,376**.
Fresh interval: `[9560000000, 9624000000]`; replicated: `[9560000000, 9616965376]`.
Local cursor: 9,617,624,832; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1072.9664818568854, 'elapsed_seconds': 5426.050340802991, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357014, 'mean_ready_depth': 0.3478590168325472, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 14056, 'prepare_wall_seconds': 5425.960808122298, 'producer_wait_capacity_seconds': 0.012595197418704629, 'producer_wait_full_seconds': 959.0041049628053, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3538.5498023843393, '1': 1887.500536835636}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 28138, 'flush_seconds': 234.01146160950884, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,609 patches/s**; new independent GMP audits: 1,757.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
