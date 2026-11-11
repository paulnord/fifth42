# Boole combined search

Updated: 2026-11-11T12:46:09.853738+00:00

State: **running**. Run **boole-preparation-20261110-16-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,050,120,448**.
New replicated logical patches: **26,120,448** in 102,033 chunks.
Combined verified selected patches, including parents: **26,120,448**.
Fresh interval: `[8024000000, 8088000000]`; replicated: `[8024000000, 8050120448]`.
Local cursor: 8,050,534,144; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15055839775595814, 'elapsed_seconds': 2704.5034345209715, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681603, 'mean_ready_depth': 0.9990542975171369, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6466, 'prepare_wall_seconds': 2702.963943459734, 'producer_wait_capacity_seconds': 0.008414777461439371, 'producer_wait_full_seconds': 1546.693369291257, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.557653492956888, '1': 2701.9457789080334}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 12952, 'flush_seconds': 90.87532488320721, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,789 patches/s**; new independent GMP audits: 809.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
