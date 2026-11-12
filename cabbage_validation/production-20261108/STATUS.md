# Cabbage combined search

Updated: 2026-11-12T00:28:07.508426+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-39**; gpu with 16 preparation workers.
Verified replicated cursor: **9,505,660,672**.
New replicated logical patches: **9,660,672** in 37,737 chunks.
Combined verified selected patches, including parents: **9,660,672**.
Fresh interval: `[9496000000, 9560000000]`; replicated: `[9496000000, 9505660672]`.
Local cursor: 9,505,931,008; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 186.43889101501554, 'elapsed_seconds': 914.760048978962, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15354357, 'mean_ready_depth': 0.3411998496616406, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2410, 'prepare_wall_seconds': 914.0559481977252, 'producer_wait_capacity_seconds': 0.0021040044957771897, 'producer_wait_full_seconds': 153.95159404398873, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 602.6440544149373, '1': 312.1159911880968}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 4822, 'flush_seconds': 37.706674361019395, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,779 patches/s**; new independent GMP audits: 302.
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
