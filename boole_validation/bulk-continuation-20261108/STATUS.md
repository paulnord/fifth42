# Boole combined search

Updated: 2026-11-11T10:42:12.220709+00:00

State: **running**. Run **boole-preparation-20261110-15-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,977,791,232**.
New replicated logical patches: **17,791,232** in 69,497 chunks.
Combined verified selected patches, including parents: **17,791,232**.
Fresh interval: `[7960000000, 8024000000]`; replicated: `[7960000000, 7977791232]`.
Local cursor: 7,978,053,376; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.1566982125514187, 'elapsed_seconds': 1809.7790679470054, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681938, 'mean_ready_depth': 0.9990774574318583, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4408, 'prepare_wall_seconds': 1809.5511446278542, 'producer_wait_capacity_seconds': 0.0057034207857213914, 'producer_wait_full_seconds': 1022.2090298153926, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.6695961491204798, '1': 1808.1094697178924}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 8820, 'flush_seconds': 63.19282208190998, 'pending_bytes': 133640, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,971 patches/s**; new independent GMP audits: 551.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
