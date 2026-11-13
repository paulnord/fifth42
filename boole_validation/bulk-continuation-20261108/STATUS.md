# Boole combined search

Updated: 2026-11-13T02:26:40.042294+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,111,764,736**.
New replicated logical patches: **63,764,736** in 249,081 chunks.
Combined verified selected patches, including parents: **63,764,736**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9111764736]`.
Local cursor: 9,111,951,104; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.17026096838526428, 'elapsed_seconds': 9145.054141169065, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7687191, 'mean_ready_depth': 0.9994501301952496, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15606, 'prepare_wall_seconds': 9144.783022391144, 'producer_wait_capacity_seconds': 0.01954999892041087, 'producer_wait_full_seconds': 6375.286739314091, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.0285865450277925, '1': 9140.025552034029}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 31253, 'flush_seconds': 242.88995219522621, 'pending_bytes': 19860, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **6,989 patches/s**; new independent GMP audits: 1,951.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
