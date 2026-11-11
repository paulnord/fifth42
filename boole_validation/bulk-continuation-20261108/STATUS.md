# Boole combined search

Updated: 2026-11-11T07:10:07.780441+00:00

State: **running**. Run **boole-preparation-20261110-13-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,849,881,344**.
New replicated logical patches: **17,881,344** in 69,849 chunks.
Combined verified selected patches, including parents: **17,881,344**.
Fresh interval: `[7832000000, 7896000000]`; replicated: `[7832000000, 7849881344]`.
Local cursor: 7,850,538,752; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1549290248658508, 'elapsed_seconds': 1798.1745003329706, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681125, 'mean_ready_depth': 0.9990370650003295, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4503, 'prepare_wall_seconds': 1797.9721813958604, 'producer_wait_capacity_seconds': 0.005849227251019329, 'producer_wait_full_seconds': 993.7698872419423, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.7315228818915784, '1': 1796.442975171085}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 9018, 'flush_seconds': 63.06134771055076, 'pending_bytes': 95183, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,252 patches/s**; new independent GMP audits: 563.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
