# Cabbage combined search

Updated: 2026-11-12T18:23:48.051828+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-48**; gpu with 16 preparation workers.
Verified replicated cursor: **10,130,194,176**.
New replicated logical patches: **58,194,176** in 227,321 chunks.
Combined verified selected patches, including parents: **58,194,176**.
Fresh interval: `[10072000000, 10136000000]`; replicated: `[10072000000, 10130194176]`.
Local cursor: 10,130,390,784; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 777.022840786376, 'elapsed_seconds': 6354.554329678067, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358751, 'mean_ready_depth': 0.445544776383824, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 14251, 'prepare_wall_seconds': 6354.236284079612, 'producer_wait_capacity_seconds': 0.013027929468080401, 'producer_wait_full_seconds': 1698.9075344650773, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3523.3158398687374, '1': 2831.238487835275}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 28530, 'flush_seconds': 251.0827471729135, 'pending_bytes': 147301, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,184 patches/s**; new independent GMP audits: 1,782.
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
