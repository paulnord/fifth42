# Cabbage combined search

Updated: 2026-11-12T03:39:31.304284+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-41**; gpu with 16 preparation workers.
Verified replicated cursor: **9,624,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[9624000000, 9688000000]`; replicated: `[9624000000, 9624002048]`.
Local cursor: 9,624,176,128; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2.2667676048586145, 'elapsed_seconds': 10.627274233964272, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15349349, 'mean_ready_depth': 0.3801434922067666, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 26, 'prepare_wall_seconds': 9.881869125762023, 'producer_wait_capacity_seconds': 2.68787844106555e-05, 'producer_wait_full_seconds': 1.8456134470179677, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 6.587380976066925, '1': 4.039889139938168}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 48, 'flush_seconds': 0.29619161190930754, 'pending_bytes': 35303, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,980 patches/s**; new independent GMP audits: 4.
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
