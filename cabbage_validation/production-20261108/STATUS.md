# Cabbage combined search

Updated: 2026-11-12T18:08:43.004885+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-48**; gpu with 16 preparation workers.
Verified replicated cursor: **10,121,715,456**.
New replicated logical patches: **49,715,456** in 194,201 chunks.
Combined verified selected patches, including parents: **49,715,456**.
Fresh interval: `[10072000000, 10136000000]`; replicated: `[10072000000, 10121715456]`.
Local cursor: 10,122,163,712; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 668.5769981420599, 'elapsed_seconds': 5446.6924278240185, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358751, 'mean_ready_depth': 0.444583272262664, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 12234, 'prepare_wall_seconds': 5445.586691356613, 'producer_wait_capacity_seconds': 0.011160125490278006, 'producer_wait_full_seconds': 1451.9090151770506, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3025.184082227759, '1': 2421.508342570276}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 24488, 'flush_seconds': 216.00741152337287, 'pending_bytes': 36828, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,198 patches/s**; new independent GMP audits: 1,530.
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
