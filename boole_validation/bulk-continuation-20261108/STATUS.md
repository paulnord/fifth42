# Boole combined search

Updated: 2026-11-10T21:34:31.261748+00:00

State: **running**. Run **boole-preparation-20261110-07-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,484,600,064**.
New replicated logical patches: **36,600,064** in 142,969 chunks.
Combined verified selected patches, including parents: **36,600,064**.
Fresh interval: `[7448000000, 7512000000]`; replicated: `[7448000000, 7484600064]`.
Local cursor: 7,484,960,512; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1596831812057644, 'elapsed_seconds': 3248.3642481299466, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681146, 'mean_ready_depth': 0.9976092059026035, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9018, 'prepare_wall_seconds': 3247.13810582686, 'producer_wait_capacity_seconds': 0.011542739754077047, 'producer_wait_full_seconds': 1618.5023143582512, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 7.766167930676602, '1': 3240.5980780593236}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 18071, 'flush_seconds': 114.47282178263413, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,368 patches/s**; new independent GMP audits: 1,128.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
