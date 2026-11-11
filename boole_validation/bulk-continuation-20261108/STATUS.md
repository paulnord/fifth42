# Boole combined search

Updated: 2026-11-11T22:15:13.725558+00:00

State: **running**. Run **boole-range-r3-20261111-19-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,274,261,504**.
New replicated logical patches: **58,261,504** in 227,584 chunks.
Combined verified selected patches, including parents: **58,261,504**.
Fresh interval: `[8216000000, 8280000000]`; replicated: `[8216000000, 8274261504]`.
Local cursor: 8,274,294,272; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1587450283113867, 'elapsed_seconds': 6322.924719842034, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683265, 'mean_ready_depth': 0.9992749828176147, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14226, 'prepare_wall_seconds': 6317.292708727589, 'producer_wait_capacity_seconds': 0.01878403004957363, 'producer_wait_full_seconds': 3785.154507716885, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.58422611473361, '1': 6318.34049077722}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 28500, 'flush_seconds': 212.05778294161428, 'pending_bytes': 19213, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,214 patches/s**; new independent GMP audits: 1,779.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
