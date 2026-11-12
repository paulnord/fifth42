# Boole combined search

Updated: 2026-11-12T03:41:11.974032+00:00

State: **running**. Run **boole-range-r3-20261111-22-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,447,385,344**.
New replicated logical patches: **39,385,344** in 153,849 chunks.
Combined verified selected patches, including parents: **39,385,344**.
Fresh interval: `[8408000000, 8472000000]`; replicated: `[8408000000, 8447385344]`.
Local cursor: 8,447,483,648; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1666037040995434, 'elapsed_seconds': 4506.271663735039, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7688034, 'mean_ready_depth': 0.9992735241751083, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 9618, 'prepare_wall_seconds': 4501.30300893134, 'producer_wait_capacity_seconds': 0.012812799541279674, 'producer_wait_full_seconds': 2798.258854866377, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.273694894160144, '1': 4502.997966310941}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 19265, 'flush_seconds': 144.3845601323992, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,740 patches/s**; new independent GMP audits: 1,203.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
