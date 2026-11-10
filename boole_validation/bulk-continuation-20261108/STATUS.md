# Boole combined search

Updated: 2026-11-10T18:28:06.880432+00:00

State: **running**. Run **boole-delegated-20261109-05**; gpu with 16 preparation workers.
Verified replicated cursor: **7,372,533,504**.
New replicated logical patches: **52,533,504** in 205,209 chunks.
Combined verified selected patches, including parents: **52,533,504**.
Fresh interval: `[7320000000, 7384000000]`; replicated: `[7320000000, 7372533504]`.
Local cursor: 7,373,039,360; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 51.84629937435966, 'elapsed_seconds': 4528.476015285996, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482507, 'mean_ready_depth': 2.2643092959982853, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 206724, 'prepare_wall_seconds': 4526.6825853465125, 'producer_wait_capacity_seconds': 0.13539037597365677, 'producer_wait_full_seconds': 2126.4458683214034, 'ready': 3, 'ready_depth_seconds': {'0': 520.1194693663856, '1': 617.3459963700734, '2': 536.5073038113769, '3': 2854.5032447081758}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 25884, 'flush_seconds': 144.44120280462084, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,685 patches/s**; new independent GMP audits: 1,616.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
