# Boole combined search

Updated: 2026-11-10T17:57:56.002338+00:00

State: **running**. Run **boole-delegated-20261109-05**; gpu with 16 preparation workers.
Verified replicated cursor: **7,351,666,432**.
New replicated logical patches: **31,666,432** in 123,697 chunks.
Combined verified selected patches, including parents: **31,666,432**.
Fresh interval: `[7320000000, 7384000000]`; replicated: `[7320000000, 7351666432]`.
Local cursor: 7,351,850,496; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 31.090156684978865, 'elapsed_seconds': 2721.3997045870055, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482507, 'mean_ready_depth': 2.266094866025757, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 124164, 'prepare_wall_seconds': 2719.9293610794703, 'producer_wait_capacity_seconds': 0.08150940819177777, 'producer_wait_full_seconds': 1279.5825764312176, 'ready': 3, 'ready_depth_seconds': {'0': 311.40737851237645, '1': 371.14079689170467, '2': 320.7454828018672, '3': 1718.106045491062}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 15551, 'flush_seconds': 87.14336631633341, 'pending_bytes': 18401, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,678 patches/s**; new independent GMP audits: 971.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
