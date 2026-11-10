# Cabbage combined search

Updated: 2026-11-10T07:10:02.925237+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **702,432,768**.
New replicated logical patches: **202,432,768** in 790,753 chunks.
Combined verified selected patches, including parents: **202,432,768**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 702432768]`.
Local cursor: 703,239,680; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3655.3987507025595, 'elapsed_seconds': 9040.465973608952, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514182, 'mean_ready_depth': 0.14127773260394455, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 793896, 'prepare_wall_seconds': 9037.726908833894, 'producer_wait_capacity_seconds': 0.48770170932402834, 'producer_wait_full_seconds': 158.5654810119886, 'ready': 0, 'ready_depth_seconds': {'0': 8121.701024387206, '1': 730.6652422697516, '2': 17.74782610515831, '3': 170.3518799848389}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 99303, 'flush_seconds': 531.3878012163914, 'pending_bytes': 121807, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,459 patches/s**; new independent GMP audits: 6,203.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
