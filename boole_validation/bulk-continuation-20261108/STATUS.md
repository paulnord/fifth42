# Boole combined search

Updated: 2026-11-11T06:26:25.306494+00:00

State: **running**. Run **boole-preparation-20261110-12-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,823,396,608**.
New replicated logical patches: **55,396,608** in 216,393 chunks.
Combined verified selected patches, including parents: **55,396,608**.
Fresh interval: `[7768000000, 7832000000]`; replicated: `[7768000000, 7823396608]`.
Local cursor: 7,823,998,720; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16878776892554015, 'elapsed_seconds': 5408.308301941026, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681653, 'mean_ready_depth': 0.9990592426588362, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 13663, 'prepare_wall_seconds': 5408.0382390999, 'producer_wait_capacity_seconds': 0.017709238338284194, 'producer_wait_full_seconds': 2950.486190663243, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.087903428298887, '1': 5403.220396202698}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 27378, 'flush_seconds': 190.01434190029977, 'pending_bytes': 114214, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,346 patches/s**; new independent GMP audits: 1,708.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
