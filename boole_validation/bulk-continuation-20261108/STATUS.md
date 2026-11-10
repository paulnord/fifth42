# Boole combined search

Updated: 2026-11-10T10:05:25.194457+00:00

State: **running**. Run **boole-delegated-20261109-00**; gpu with 16 preparation workers.
Verified replicated cursor: **7,010,549,504**.
New replicated logical patches: **10,549,504** in 41,209 chunks.
Combined verified selected patches, including parents: **10,549,504**.
Fresh interval: `[7000000000, 7064000000]`; replicated: `[7000000000, 7010549504]`.
Local cursor: 7,011,368,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 17.71475748467492, 'elapsed_seconds': 900.6874900470139, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482003, 'mean_ready_depth': 2.0670938678042794, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 43943, 'prepare_wall_seconds': 900.5239442090387, 'producer_wait_capacity_seconds': 0.028266310051549226, 'producer_wait_full_seconds': 391.069949561439, 'ready': 2, 'ready_depth_seconds': {'0': 153.44890841451706, '1': 143.20433459011838, '2': 93.50148574309424, '3': 510.53276046930114}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 5495, 'flush_seconds': 30.734399525332265, 'pending_bytes': 73667, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,484 patches/s**; new independent GMP audits: 344.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
