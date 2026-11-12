# Boole combined search

Updated: 2026-11-12T18:42:24.162021+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,882,718,464**.
New replicated logical patches: **26,718,464** in 104,369 chunks.
Combined verified selected patches, including parents: **26,718,464**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8882718464]`.
Local cursor: 8,883,162,880; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15833900216966867, 'elapsed_seconds': 3614.8910442190245, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681486, 'mean_ready_depth': 0.9993720174618516, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 6618, 'prepare_wall_seconds': 3612.5165031442884, 'producer_wait_capacity_seconds': 0.008881362271495163, 'producer_wait_full_seconds': 2451.921028301702, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.2700852430425584, '1': 3612.620955765946}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 13266, 'flush_seconds': 98.43260016024578, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,496 patches/s**; new independent GMP audits: 828.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
