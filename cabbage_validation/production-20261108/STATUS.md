# Cabbage combined search

Updated: 2026-11-12T10:01:30.281694+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-44**; gpu with 16 preparation workers.
Verified replicated cursor: **9,851,944,704**.
New replicated logical patches: **35,944,704** in 140,409 chunks.
Combined verified selected patches, including parents: **35,944,704**.
Fresh interval: `[9816000000, 9880000000]`; replicated: `[9816000000, 9851944704]`.
Local cursor: 9,852,337,920; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 644.1513209843542, 'elapsed_seconds': 3623.3917302039918, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15354740, 'mean_ready_depth': 0.38554440993946615, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 8867, 'prepare_wall_seconds': 3623.037734282203, 'producer_wait_capacity_seconds': 0.007941024960018694, 'producer_wait_full_seconds': 788.231016564765, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 2226.413301047869, '1': 1396.9784266010392}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 17748, 'flush_seconds': 147.15612982749008, 'pending_bytes': 141213, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,022 patches/s**; new independent GMP audits: 1,109.
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
