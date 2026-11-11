# Boole combined search

Updated: 2026-11-11T02:03:16.404855+00:00

State: **running**. Run **boole-preparation-20261110-10-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,659,269,888**.
New replicated logical patches: **19,269,888** in 75,273 chunks.
Combined verified selected patches, including parents: **19,269,888**.
Fresh interval: `[7640000000, 7704000000]`; replicated: `[7640000000, 7659269888]`.
Local cursor: 7,659,435,520; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15095593692967668, 'elapsed_seconds': 1819.8411368100205, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680366, 'mean_ready_depth': 0.9989256887454986, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4742, 'prepare_wall_seconds': 1819.65445880685, 'producer_wait_capacity_seconds': 0.006212071166373789, 'producer_wait_full_seconds': 964.1276177529944, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.9550736046512611, '1': 1817.8860609953408}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 9494, 'flush_seconds': 62.25637443776941, 'pending_bytes': 95107, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,668 patches/s**; new independent GMP audits: 593.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
