# Cabbage combined search

Updated: 2026-11-11T22:45:43.825045+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-38**; gpu with 16 preparation workers.
Verified replicated cursor: **9,441,699,328**.
New replicated logical patches: **9,699,328** in 37,888 chunks.
Combined verified selected patches, including parents: **9,699,328**.
Fresh interval: `[9432000000, 9496000000]`; replicated: `[9432000000, 9441699328]`.
Local cursor: 9,441,748,480; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 187.69251649058424, 'elapsed_seconds': 889.9573704900686, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15356922, 'mean_ready_depth': 0.3307722508237731, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2358, 'prepare_wall_seconds': 889.8215743685141, 'producer_wait_capacity_seconds': 0.0021275316830724478, 'producer_wait_full_seconds': 142.77205265068915, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 595.5841584478039, '1': 294.3732025742065}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 4717, 'flush_seconds': 37.63587556348648, 'pending_bytes': 70602, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,846 patches/s**; new independent GMP audits: 295.
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
