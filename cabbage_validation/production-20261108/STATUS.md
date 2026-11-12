# Cabbage combined search

Updated: 2026-11-12T07:42:30.440070+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-43**; gpu with 16 preparation workers.
Verified replicated cursor: **9,770,282,752**.
New replicated logical patches: **18,282,752** in 71,417 chunks.
Combined verified selected patches, including parents: **18,282,752**.
Fresh interval: `[9752000000, 9816000000]`; replicated: `[9752000000, 9770282752]`.
Local cursor: 9,770,479,360; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 332.72996235406026, 'elapsed_seconds': 1808.6874487410532, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355761, 'mean_ready_depth': 0.3718023338587935, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 4511, 'prepare_wall_seconds': 1808.6474872700637, 'producer_wait_capacity_seconds': 0.004008723888546228, 'producer_wait_full_seconds': 366.71739879390225, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1136.2132325050188, '1': 672.4742146630306}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 9028, 'flush_seconds': 75.83102220087312, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,212 patches/s**; new independent GMP audits: 564.
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
