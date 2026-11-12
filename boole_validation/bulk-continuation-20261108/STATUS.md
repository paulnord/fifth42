# Boole combined search

Updated: 2026-11-12T23:00:19.147662+00:00

State: **stopped**. Run **boole-range-r3-20261111-30-recovery2**; gpu with 16 preparation workers.
Verified replicated cursor: **8,968,873,728**.
New replicated logical patches: **35,012,864** in 136,769 chunks.
Combined verified selected patches, including parents: **48,873,728**.
Fresh interval: `[8933860864, 8984000000]`; replicated: `[8933860864, 8968873728]`.
Local cursor: 8,968,873,728; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.2060732615645975, 'elapsed_seconds': 4818.850028896006, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681479, 'mean_ready_depth': 0.9993754707767133, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 8550, 'prepare_wall_seconds': 4818.579250197858, 'producer_wait_capacity_seconds': 0.01139896281529218, 'producer_wait_full_seconds': 3315.3592656844994, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3.0095101956976578, '1': 4815.840516230324}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 17149, 'flush_seconds': 133.17294895090163, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,265 patches/s**; new independent GMP audits: 1,069.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
