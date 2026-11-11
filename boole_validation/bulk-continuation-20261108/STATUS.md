# Boole combined search

Updated: 2026-11-11T03:43:59.680001+00:00

State: **running**. Run **boole-preparation-20261110-11-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,722,315,520**.
New replicated logical patches: **18,315,520** in 71,545 chunks.
Combined verified selected patches, including parents: **18,315,520**.
Fresh interval: `[7704000000, 7768000000]`; replicated: `[7704000000, 7722315520]`.
Local cursor: 7,723,045,632; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.152769087231718, 'elapsed_seconds': 1798.055960928963, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681946, 'mean_ready_depth': 0.9989443529734832, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 4642, 'prepare_wall_seconds': 1796.6323834369541, 'producer_wait_capacity_seconds': 0.006144956219941378, 'producer_wait_full_seconds': 962.3505997825414, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.8981109386659227, '1': 1796.1578485002974}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 9300, 'flush_seconds': 64.64036432822468, 'pending_bytes': 133177, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,569 patches/s**; new independent GMP audits: 581.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
