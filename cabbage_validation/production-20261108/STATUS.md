# Cabbage combined search

Updated: 2026-11-10T22:29:51.674602+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,940,480,512**.
New replicated logical patches: **401,631,488** in 1,568,873 chunks.
Combined verified selected patches, including parents: **1,440,480,512**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1940480512]`.
Local cursor: 1,942,471,168; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1512.7490952376393, 'elapsed_seconds': 9490.495378245949, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838862, 'mean_ready_depth': 0.1918387552351855, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 98485, 'prepare_wall_seconds': 9490.084742181527, 'producer_wait_capacity_seconds': 0.07184319122461602, 'producer_wait_full_seconds': 257.11205862718634, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7669.850556774996, '1': 1820.644819927984}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 197172, 'flush_seconds': 1143.981170819723, 'pending_bytes': 19921, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,480 patches/s**; new independent GMP audits: 12,311.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
