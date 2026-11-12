# Boole combined search

Updated: 2026-11-12T07:49:56.918380+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,573,708,032**.
New replicated logical patches: **37,708,032** in 147,297 chunks.
Combined verified selected patches, including parents: **37,708,032**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8573708032]`.
Local cursor: 8,573,974,272; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16153087525162846, 'elapsed_seconds': 4505.479738994967, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685457, 'mean_ready_depth': 0.999296324973987, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9250, 'prepare_wall_seconds': 4503.461042767856, 'producer_wait_capacity_seconds': 0.012522195000201464, 'producer_wait_full_seconds': 2865.416474366444, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.1703905725153163, '1': 4502.309345422429}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 18533, 'flush_seconds': 139.34049397101626, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,407 patches/s**; new independent GMP audits: 1,157.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
