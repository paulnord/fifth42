# Boole combined search

Updated: 2026-11-11T11:12:09.029679+00:00

State: **running**. Run **boole-preparation-20261110-15-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,995,621,120**.
New replicated logical patches: **35,621,120** in 139,145 chunks.
Combined verified selected patches, including parents: **35,621,120**.
Fresh interval: `[7960000000, 8024000000]`; replicated: `[7960000000, 7995621120]`.
Local cursor: 7,995,780,864; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16229498421307653, 'elapsed_seconds': 3600.0260825160076, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681938, 'mean_ready_depth': 0.9991602491770348, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8720, 'prepare_wall_seconds': 3599.8863395632943, 'producer_wait_capacity_seconds': 0.011236392427235842, 'producer_wait_full_seconds': 2040.4426878974773, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.023122484504711, '1': 3597.0029576505185}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 17472, 'flush_seconds': 124.17042547091842, 'pending_bytes': 95581, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,918 patches/s**; new independent GMP audits: 1,090.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
