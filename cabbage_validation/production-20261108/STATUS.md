# Cabbage combined search

Updated: 2026-11-12T01:13:12.843944+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-39**; gpu with 16 preparation workers.
Verified replicated cursor: **9,534,756,608**.
New replicated logical patches: **38,756,608** in 151,393 chunks.
Combined verified selected patches, including parents: **38,756,608**.
Fresh interval: `[9496000000, 9560000000]`; replicated: `[9496000000, 9534756608]`.
Local cursor: 9,535,004,416; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 732.534141956945, 'elapsed_seconds': 3625.648252538056, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355833, 'mean_ready_depth': 0.34328050174624747, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 9522, 'prepare_wall_seconds': 3624.893573155161, 'producer_wait_capacity_seconds': 0.00829520239494741, 'producer_wait_full_seconds': 616.5317242731107, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2381.0338983352995, '1': 1244.6143512866693}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 19057, 'flush_seconds': 154.38817813631613, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,754 patches/s**; new independent GMP audits: 1,191.
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
