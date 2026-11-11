# Boole combined search

Updated: 2026-11-11T17:45:10.629457+00:00

State: **running**. Run **boole-range-r3-20261111-18**; gpu with 16 preparation workers.
Verified replicated cursor: **8,212,160,512**.
New replicated logical patches: **22,542,592** in 88,057 chunks.
Combined verified selected patches, including parents: **60,160,512**.
Fresh interval: `[8189617920, 8216000000]`; replicated: `[8189617920, 8212160512]`.
Local cursor: 8,212,817,920; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.17039483692497015, 'elapsed_seconds': 2465.564209145028, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682831, 'mean_ready_depth': 0.9991745308439457, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 5657, 'prepare_wall_seconds': 2465.3948222019244, 'producer_wait_capacity_seconds': 0.0071896337904036045, 'producer_wait_full_seconds': 1464.8010904969415, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.035245156905148, '1': 2463.5289619381074}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 11333, 'flush_seconds': 80.40489246067591, 'pending_bytes': 115189, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,394 patches/s**; new independent GMP audits: 707.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
