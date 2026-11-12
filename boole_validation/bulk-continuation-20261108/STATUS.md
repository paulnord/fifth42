# Boole combined search

Updated: 2026-11-12T17:38:39.057174+00:00

State: **running**. Run **boole-range-r3-20261111-28-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,854,556,416**.
New replicated logical patches: **62,556,416** in 244,361 chunks.
Combined verified selected patches, including parents: **62,556,416**.
Fresh interval: `[8792000000, 8856000000]`; replicated: `[8792000000, 8854556416]`.
Local cursor: 8,854,832,896; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1637270355131477, 'elapsed_seconds': 8134.014324372052, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7686814, 'mean_ready_depth': 0.9994012666587152, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15338, 'prepare_wall_seconds': 8131.680442224955, 'producer_wait_capacity_seconds': 0.020230166846886277, 'producer_wait_full_seconds': 5433.9400304270675, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.870102114509791, '1': 8129.144218797563}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 30742, 'flush_seconds': 230.69444550969638, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,722 patches/s**; new independent GMP audits: 1,918.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
