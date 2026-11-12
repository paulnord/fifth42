# Cabbage combined search

Updated: 2026-11-12T14:40:44.053072+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-47**; gpu with 16 preparation workers.
Verified replicated cursor: **10,008,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[10008000000, 10072000000]`; replicated: `[10008000000, 10008002048]`.
Local cursor: 10,008,131,072; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1.5066707228543237, 'elapsed_seconds': 9.738680195994675, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15352740, 'mean_ready_depth': 0.42026376705942636, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 23, 'prepare_wall_seconds': 9.728466614964418, 'producer_wait_capacity_seconds': 2.5349087081849575e-05, 'producer_wait_full_seconds': 2.477930470602587, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 5.64586376666557, '1': 4.092814425355755}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 44, 'flush_seconds': 0.392137557384558, 'pending_bytes': 36823, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,945 patches/s**; new independent GMP audits: 3.
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
