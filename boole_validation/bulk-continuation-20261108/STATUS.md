# Boole combined search

Updated: 2026-11-11T23:26:29.407514+00:00

State: **running**. Run **boole-range-r3-20261111-20-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,312,755,968**.
New replicated logical patches: **32,755,968** in 127,953 chunks.
Combined verified selected patches, including parents: **32,755,968**.
Fresh interval: `[8280000000, 8344000000]`; replicated: `[8280000000, 8312755968]`.
Local cursor: 8,312,837,888; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15142540307715535, 'elapsed_seconds': 3613.572563697002, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682926, 'mean_ready_depth': 0.9992499720460065, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8019, 'prepare_wall_seconds': 3613.4933040894102, 'producer_wait_capacity_seconds': 0.011466094641946256, 'producer_wait_full_seconds': 2190.8936664200155, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.710277886595577, '1': 3610.862283260445}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 16060, 'flush_seconds': 121.66690240101889, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,087 patches/s**; new independent GMP audits: 1,003.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
