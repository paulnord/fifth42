# Boole combined search

Updated: 2026-11-10T22:04:35.548035+00:00

State: **running**. Run **boole-preparation-20261110-07-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,504,948,992**.
New replicated logical patches: **56,948,992** in 222,457 chunks.
Combined verified selected patches, including parents: **56,948,992**.
Fresh interval: `[7448000000, 7512000000]`; replicated: `[7448000000, 7504948992]`.
Local cursor: 7,505,118,976; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1662862669909373, 'elapsed_seconds': 5050.530278778984, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681146, 'mean_ready_depth': 0.997767702567186, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13935, 'prepare_wall_seconds': 5050.399866450927, 'producer_wait_capacity_seconds': 0.017908981651999056, 'producer_wait_full_seconds': 2532.9576589578064, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 11.274283475650009, '1': 5039.255993003317}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 27927, 'flush_seconds': 176.93793642456876, 'pending_bytes': 38043, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,299 patches/s**; new independent GMP audits: 1,742.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
