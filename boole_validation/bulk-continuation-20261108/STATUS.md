# Boole combined search

Updated: 2026-11-11T06:11:24.623754+00:00

State: **running**. Run **boole-preparation-20261110-12-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,814,018,816**.
New replicated logical patches: **46,018,816** in 179,761 chunks.
Combined verified selected patches, including parents: **46,018,816**.
Fresh interval: `[7768000000, 7832000000]`; replicated: `[7768000000, 7814018816]`.
Local cursor: 7,814,742,272; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1657695884932764, 'elapsed_seconds': 4507.714679956029, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681653, 'mean_ready_depth': 0.9990506166155725, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11410, 'prepare_wall_seconds': 4506.29738976853, 'producer_wait_capacity_seconds': 0.01478954980848357, 'producer_wait_full_seconds': 2454.5941481916816, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.279546908859629, '1': 4503.435130537138}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 22855, 'flush_seconds': 158.85702981357463, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,365 patches/s**; new independent GMP audits: 1,427.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
