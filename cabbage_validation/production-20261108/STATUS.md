# Cabbage combined search

Updated: 2026-11-11T23:30:52.254527+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-38**; gpu with 16 preparation workers.
Verified replicated cursor: **9,470,404,096**.
New replicated logical patches: **38,404,096** in 150,016 chunks.
Combined verified selected patches, including parents: **38,404,096**.
Fresh interval: `[9432000000, 9496000000]`; replicated: `[9432000000, 9470404096]`.
Local cursor: 9,471,092,224; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 752.3926990263863, 'elapsed_seconds': 3599.334912926075, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358283, 'mean_ready_depth': 0.33187286794309656, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 9522, 'prepare_wall_seconds': 3598.68329000636, 'producer_wait_capacity_seconds': 0.008502291515469551, 'producer_wait_full_seconds': 578.554675045656, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2404.8133095195517, '1': 1194.5216002404923}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 19053, 'flush_seconds': 151.29122982244007, 'pending_bytes': 35303, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,833 patches/s**; new independent GMP audits: 1,191.
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
