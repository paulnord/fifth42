# Boole combined search

Updated: 2026-11-13T02:11:31.675430+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,105,374,976**.
New replicated logical patches: **57,374,976** in 224,121 chunks.
Combined verified selected patches, including parents: **57,374,976**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9105374976]`.
Local cursor: 9,105,671,680; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16810457885731012, 'elapsed_seconds': 8238.440285763005, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7687191, 'mean_ready_depth': 0.9994461764158565, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14074, 'prepare_wall_seconds': 8235.775566756842, 'producer_wait_capacity_seconds': 0.017621533013880253, 'producer_wait_full_seconds': 5739.667838116526, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.562639626790769, '1': 8233.877643236192}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 28187, 'flush_seconds': 220.666148608434, 'pending_bytes': 19860, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **6,996 patches/s**; new independent GMP audits: 1,760.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
