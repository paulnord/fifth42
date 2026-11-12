# Boole combined search

Updated: 2026-11-12T11:24:10.425619+00:00

State: **running**. Run **boole-range-r3-20261111-26-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,678,295,296**.
New replicated logical patches: **14,295,296** in 55,841 chunks.
Combined verified selected patches, including parents: **14,295,296**.
Fresh interval: `[8664000000, 8728000000]`; replicated: `[8664000000, 8678295296]`.
Local cursor: 8,678,809,344; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15446341887582093, 'elapsed_seconds': 1803.8061626000563, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681670, 'mean_ready_depth': 0.999235637193088, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3602, 'prepare_wall_seconds': 1801.6694487357745, 'producer_wait_capacity_seconds': 0.004757569753564894, 'producer_wait_full_seconds': 1169.5578887461452, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.378759411512874, '1': 1802.4274002584862}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7214, 'flush_seconds': 55.40730125748087, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,173 patches/s**; new independent GMP audits: 451.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
