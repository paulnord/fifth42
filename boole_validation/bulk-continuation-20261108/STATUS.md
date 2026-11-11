# Boole combined search

Updated: 2026-11-11T10:57:10.254171+00:00

State: **running**. Run **boole-preparation-20261110-15-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,986,726,656**.
New replicated logical patches: **26,726,656** in 104,401 chunks.
Combined verified selected patches, including parents: **26,726,656**.
Fresh interval: `[7960000000, 8024000000]`; replicated: `[7960000000, 7986726656]`.
Local cursor: 7,986,925,312; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15948012616718188, 'elapsed_seconds': 2698.4502295220154, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681938, 'mean_ready_depth': 0.999138060430473, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6549, 'prepare_wall_seconds': 2698.25151824404, 'producer_wait_capacity_seconds': 0.008445498708169907, 'producer_wait_full_seconds': 1527.8396068998263, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.3258986191940494, '1': 2696.1243284927914}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 13116, 'flush_seconds': 92.48093766038073, 'pending_bytes': 38190, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,937 patches/s**; new independent GMP audits: 819.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
