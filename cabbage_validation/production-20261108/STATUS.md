# Cabbage combined search

Updated: 2026-11-10T23:45:06.498436+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,125,219,584**.
New replicated logical patches: **586,370,560** in 2,290,510 chunks.
Combined verified selected patches, including parents: **1,625,219,584**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2125219584]`.
Local cursor: 2,129,033,728; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2062.2603274320136, 'elapsed_seconds': 14002.580874973966, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.2288804255793028, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 144008, 'prepare_wall_seconds': 14002.002614502446, 'producer_wait_capacity_seconds': 0.10615629790117964, 'producer_wait_full_seconds': 418.53596286295215, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 10797.664203829307, '1': 3204.9166698726476}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 288316, 'flush_seconds': 1649.2385236066184, 'pending_bytes': 10012, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,108 patches/s**; new independent GMP audits: 18,001.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
