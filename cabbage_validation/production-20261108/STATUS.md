# Cabbage combined search

Updated: 2026-11-10T23:14:59.357087+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,052,454,144**.
New replicated logical patches: **513,605,120** in 2,006,270 chunks.
Combined verified selected patches, including parents: **1,552,454,144**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2052454144]`.
Local cursor: 2,054,781,184; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1849.6151244572247, 'elapsed_seconds': 12193.59668288898, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.2154650026030384, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 125862, 'prepare_wall_seconds': 12193.09674598393, 'producer_wait_capacity_seconds': 0.09237573336577043, 'producer_wait_full_seconds': 344.9324287531199, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 9566.303338283906, '1': 2627.2933410190744}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 251982, 'flush_seconds': 1448.6736586958868, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,259 patches/s**; new independent GMP audits: 15,733.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
