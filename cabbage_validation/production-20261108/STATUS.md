# Cabbage combined search

Updated: 2026-11-10T20:29:24.678411+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,634,006,784**.
New replicated logical patches: **95,157,760** in 371,710 chunks.
Combined verified selected patches, including parents: **1,134,006,784**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1634006784]`.
Local cursor: 1,635,295,488; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 402.36490225675516, 'elapsed_seconds': 2262.3313450449496, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838766, 'mean_ready_depth': 0.14349307497392866, 'outstanding': 1, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 23476, 'prepare_wall_seconds': 2262.179055576271, 'producer_wait_capacity_seconds': 0.017427269252948463, 'producer_wait_full_seconds': 85.8097342250403, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1937.7024628725485, '1': 324.6288813104038}, 'ready_limit': 1, 'reserved_bytes': 12582912}; buffer: {'flush_count': 47002, 'flush_seconds': 277.75977758393856, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,400 patches/s**; new independent GMP audits: 2,935.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
