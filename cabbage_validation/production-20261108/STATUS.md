# Cabbage combined search

Updated: 2026-11-11T23:15:51.203925+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-38**; gpu with 16 preparation workers.
Verified replicated cursor: **9,460,598,528**.
New replicated logical patches: **28,598,528** in 111,713 chunks.
Combined verified selected patches, including parents: **28,598,528**.
Fresh interval: `[9432000000, 9496000000]`; replicated: `[9432000000, 9460598528]`.
Local cursor: 9,461,323,264; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 566.1048429446528, 'elapsed_seconds': 2701.943132315064, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358283, 'mean_ready_depth': 0.33184494627695066, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 7146, 'prepare_wall_seconds': 2701.2345063261455, 'producer_wait_capacity_seconds': 0.0063857127679511905, 'producer_wait_full_seconds': 436.1057511410909, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1805.316955522634, '1': 896.6261735864682}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 14296, 'flush_seconds': 113.29429532284848, 'pending_bytes': 35299, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,829 patches/s**; new independent GMP audits: 894.
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
