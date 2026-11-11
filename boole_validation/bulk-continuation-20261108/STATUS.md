# Boole combined search

Updated: 2026-11-11T04:29:23.216877+00:00

State: **running**. Run **boole-preparation-20261110-11-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,750,889,216**.
New replicated logical patches: **46,889,216** in 183,161 chunks.
Combined verified selected patches, including parents: **46,889,216**.
Fresh interval: `[7704000000, 7768000000]`; replicated: `[7704000000, 7750889216]`.
Local cursor: 7,751,616,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16218629747163504, 'elapsed_seconds': 4523.480390920013, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681946, 'mean_ready_depth': 0.9990110075801707, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11625, 'prepare_wall_seconds': 4523.3883551378385, 'producer_wait_capacity_seconds': 0.01542459026677534, 'producer_wait_full_seconds': 2431.072962130711, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.473685477860272, '1': 4519.006703102146}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 23291, 'flush_seconds': 161.87025918334257, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,524 patches/s**; new independent GMP audits: 1,453.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
