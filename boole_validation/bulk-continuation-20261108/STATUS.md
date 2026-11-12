# Boole combined search

Updated: 2026-11-12T04:44:00.480370+00:00

State: **running**. Run **boole-range-r3-20261111-23-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,479,587,840**.
New replicated logical patches: **7,587,840** in 29,640 chunks.
Combined verified selected patches, including parents: **7,587,840**.
Fresh interval: `[8472000000, 8536000000]`; replicated: `[8472000000, 8479587840]`.
Local cursor: 8,479,823,616; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14840713411103934, 'elapsed_seconds': 904.1727049209876, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681233, 'mean_ready_depth': 0.999015250646486, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1906, 'prepare_wall_seconds': 902.2922100464348, 'producer_wait_capacity_seconds': 0.0026142278220504522, 'producer_wait_full_seconds': 565.3618741796818, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.8903811266645789, '1': 903.2823214343516}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3815, 'flush_seconds': 29.03822549979668, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,623 patches/s**; new independent GMP audits: 239.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
