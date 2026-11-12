# Cabbage combined search

Updated: 2026-11-12T19:54:29.110372+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-49**; gpu with 16 preparation workers.
Verified replicated cursor: **10,176,827,136**.
New replicated logical patches: **40,827,136** in 159,481 chunks.
Combined verified selected patches, including parents: **40,827,136**.
Fresh interval: `[10136000000, 10200000000]`; replicated: `[10136000000, 10176827136]`.
Local cursor: 10,176,900,864; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 538.8442411996657, 'elapsed_seconds': 4515.45002718491, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358069, 'mean_ready_depth': 0.45567040759884037, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 9970, 'prepare_wall_seconds': 4513.651228856645, 'producer_wait_capacity_seconds': 0.008543986128643155, 'producer_wait_full_seconds': 1262.9884479382308, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2457.8930687584216, '1': 2057.5569543795427}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 19954, 'flush_seconds': 175.10262660961598, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,041 patches/s**; new independent GMP audits: 1,247.
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
