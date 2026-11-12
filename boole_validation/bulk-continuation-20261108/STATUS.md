# Boole combined search

Updated: 2026-11-12T09:57:49.304422+00:00

State: **running**. Run **boole-range-r3-20261111-25-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,636,825,344**.
New replicated logical patches: **36,825,344** in 143,849 chunks.
Combined verified selected patches, including parents: **36,825,344**.
Fresh interval: `[8600000000, 8664000000]`; replicated: `[8600000000, 8636825344]`.
Local cursor: 8,637,077,248; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.17105170141439885, 'elapsed_seconds': 4510.404030861915, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681333, 'mean_ready_depth': 0.9993055472544806, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9050, 'prepare_wall_seconds': 4508.296886226046, 'producer_wait_capacity_seconds': 0.0118700647726655, 'producer_wait_full_seconds': 2905.159659443074, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.1322604226879776, '1': 4507.271768399281}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 18133, 'flush_seconds': 140.9807370697381, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,216 patches/s**; new independent GMP audits: 1,132.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
