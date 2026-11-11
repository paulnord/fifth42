# Boole combined search

Updated: 2026-11-11T09:40:35.980242+00:00

State: **running**. Run **boole-preparation-20261110-14-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,941,185,280**.
New replicated logical patches: **45,185,280** in 176,505 chunks.
Combined verified selected patches, including parents: **45,185,280**.
Fresh interval: `[7896000000, 7960000000]`; replicated: `[7896000000, 7941185280]`.
Local cursor: 7,941,447,424; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.16122213657945395, 'elapsed_seconds': 4523.567047102028, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681255, 'mean_ready_depth': 0.9991339893572335, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11086, 'prepare_wall_seconds': 4523.236354427296, 'producer_wait_capacity_seconds': 0.014219946751836687, 'producer_wait_full_seconds': 2531.9180617271923, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.9174556860816665, '1': 4519.649589895969}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 22210, 'flush_seconds': 160.47671911900397, 'pending_bytes': 133503, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,036 patches/s**; new independent GMP audits: 1,386.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
