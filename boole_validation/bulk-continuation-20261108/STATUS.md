# Boole combined search

Updated: 2026-11-12T18:12:11.488014+00:00

State: **running**. Run **boole-range-r3-20261111-29-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,869,465,856**.
New replicated logical patches: **13,465,856** in 52,601 chunks.
Combined verified selected patches, including parents: **13,465,856**.
Fresh interval: `[8856000000, 8920000000]`; replicated: `[8856000000, 8869465856]`.
Local cursor: 8,869,695,232; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15397870389278978, 'elapsed_seconds': 1801.0241903749993, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681486, 'mean_ready_depth': 0.9992859940096794, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3330, 'prepare_wall_seconds': 1798.7437174477382, 'producer_wait_capacity_seconds': 0.004455780377611518, 'producer_wait_full_seconds': 1215.777668414521, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.285939300665632, '1': 1799.7382483143592}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 6671, 'flush_seconds': 48.67894930019975, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,568 patches/s**; new independent GMP audits: 417.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
