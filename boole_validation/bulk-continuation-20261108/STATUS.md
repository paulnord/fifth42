# Boole combined search

Updated: 2026-11-11T07:55:16.452612+00:00

State: **running**. Run **boole-preparation-20261110-13-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,877,481,984**.
New replicated logical patches: **45,481,984** in 177,664 chunks.
Combined verified selected patches, including parents: **45,481,984**.
Fresh interval: `[7832000000, 7896000000]`; replicated: `[7832000000, 7877481984]`.
Local cursor: 7,878,029,056; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1638231096439995, 'elapsed_seconds': 4507.028634654998, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681636, 'mean_ready_depth': 0.9991070302729865, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11216, 'prepare_wall_seconds': 4506.942730103212, 'producer_wait_capacity_seconds': 0.01454255887074396, 'producer_wait_full_seconds': 2500.530945313978, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.024638609495014, '1': 4503.003994525468}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 22477, 'flush_seconds': 157.6093945466564, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,191 patches/s**; new independent GMP audits: 1,402.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
