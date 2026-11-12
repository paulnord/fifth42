# Cabbage combined search

Updated: 2026-11-12T16:53:13.463320+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-48**; gpu with 16 preparation workers.
Verified replicated cursor: **10,079,895,296**.
New replicated logical patches: **7,895,296** in 30,841 chunks.
Combined verified selected patches, including parents: **7,895,296**.
Fresh interval: `[10072000000, 10136000000]`; replicated: `[10072000000, 10079895296]`.
Local cursor: 10,080,550,656; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 116.87547161837574, 'elapsed_seconds': 919.3440368390875, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355893, 'mean_ready_depth': 0.43802836627688013, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2082, 'prepare_wall_seconds': 917.2151693355991, 'producer_wait_capacity_seconds': 0.0018879177514463663, 'producer_wait_full_seconds': 238.99137024302036, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 516.6452667390695, '1': 402.6987665030174}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 4167, 'flush_seconds': 36.141278543742374, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,264 patches/s**; new independent GMP audits: 261.
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
