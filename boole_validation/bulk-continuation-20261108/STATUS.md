# Boole combined search

Updated: 2026-11-12T03:26:07.167534+00:00

State: **running**. Run **boole-range-r3-20261111-22-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,439,125,760**.
New replicated logical patches: **31,125,760** in 121,585 chunks.
Combined verified selected patches, including parents: **31,125,760**.
Fresh interval: `[8408000000, 8472000000]`; replicated: `[8408000000, 8439125760]`.
Local cursor: 8,439,717,632; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16410695610102266, 'elapsed_seconds': 3607.874395666062, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7688034, 'mean_ready_depth': 0.9992543174445582, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7738, 'prepare_wall_seconds': 3606.009234610945, 'producer_wait_capacity_seconds': 0.010287493816576898, 'producer_wait_full_seconds': 2235.6170336948708, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.690326589043252, '1': 3605.1840666669887}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 15498, 'flush_seconds': 116.19560820632614, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,782 patches/s**; new independent GMP audits: 968.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
