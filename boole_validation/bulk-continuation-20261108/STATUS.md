# Boole combined search

Updated: 2026-11-12T20:37:33.979018+00:00

State: **stopped**. Run **boole-range-r3-20261111-30-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,933,860,864**.
New replicated logical patches: **13,860,864** in 54,144 chunks.
Combined verified selected patches, including parents: **13,860,864**.
Fresh interval: `[8920000000, 8984000000]`; replicated: `[8920000000, 8933860864]`.
Local cursor: 8,933,860,864; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.15095874294638634, 'elapsed_seconds': 1875.2598817580147, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681660, 'mean_ready_depth': 0.9992499917219055, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3386, 'prepare_wall_seconds': 1874.0220989284571, 'producer_wait_capacity_seconds': 0.004593343241140246, 'producer_wait_full_seconds': 1279.2546561973868, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1.4064577949466184, '1': 1873.8534213231178}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 6779, 'flush_seconds': 51.64983375440352, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,390 patches/s**; new independent GMP audits: 423.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
