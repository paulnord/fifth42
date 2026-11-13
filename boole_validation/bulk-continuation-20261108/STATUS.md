# Boole combined search

Updated: 2026-11-13T00:11:18.332678+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,055,174,400**.
New replicated logical patches: **7,174,400** in 28,025 chunks.
Combined verified selected patches, including parents: **7,174,400**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9055174400]`.
Local cursor: 9,055,272,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15081863664090633, 'elapsed_seconds': 1024.5751775649842, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681224, 'mean_ready_depth': 0.999199720504753, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1771, 'prepare_wall_seconds': 1024.4794922695728, 'producer_wait_capacity_seconds': 0.002213931060396135, 'producer_wait_full_seconds': 713.4647107712226, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.819944045972079, '1': 1023.7552310590399}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3544, 'flush_seconds': 27.165940937702544, 'pending_bytes': 59572, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,070 patches/s**; new independent GMP audits: 222.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
