# Boole combined search

Updated: 2026-11-10T23:30:40.623131+00:00

State: **running**. Run **boole-preparation-20261110-08-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,560,881,920**.
New replicated logical patches: **48,881,920** in 190,945 chunks.
Combined verified selected patches, including parents: **48,881,920**.
Fresh interval: `[7512000000, 7576000000]`; replicated: `[7512000000, 7560881920]`.
Local cursor: 7,561,342,720; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1709760403027758, 'elapsed_seconds': 4512.425488601963, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681667, 'mean_ready_depth': 0.9987275169484524, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 12042, 'prepare_wall_seconds': 4511.141244911705, 'producer_wait_capacity_seconds': 0.01521335681900382, 'producer_wait_full_seconds': 2337.542815530789, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.741982335632201, '1': 4506.683503646345}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 24128, 'flush_seconds': 165.39817654533545, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,928 patches/s**; new independent GMP audits: 1,506.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
