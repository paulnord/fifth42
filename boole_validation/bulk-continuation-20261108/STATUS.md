# Boole combined search

Updated: 2026-11-11T05:56:25.131140+00:00

State: **running**. Run **boole-preparation-20261110-12-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,805,370,112**.
New replicated logical patches: **37,370,112** in 145,977 chunks.
Combined verified selected patches, including parents: **37,370,112**.
Fresh interval: `[7768000000, 7832000000]`; replicated: `[7768000000, 7805370112]`.
Local cursor: 7,805,484,800; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.16276394244050607, 'elapsed_seconds': 3610.426998860028, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681013, 'mean_ready_depth': 0.9990431799513466, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9147, 'prepare_wall_seconds': 3610.172150981787, 'producer_wait_capacity_seconds': 0.01184321491746232, 'producer_wait_full_seconds': 1965.9068013635115, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.454527906724252, '1': 3606.9724699233193}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 18316, 'flush_seconds': 126.48779218812706, 'pending_bytes': 133244, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,375 patches/s**; new independent GMP audits: 1,144.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
