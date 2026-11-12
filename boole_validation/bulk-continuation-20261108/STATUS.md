# Boole combined search

Updated: 2026-11-12T08:20:04.406515+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,588,558,080**.
New replicated logical patches: **52,558,080** in 205,305 chunks.
Combined verified selected patches, including parents: **52,558,080**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8588558080]`.
Local cursor: 8,589,082,368; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1665507226716727, 'elapsed_seconds': 6315.089654310956, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685457, 'mean_ready_depth': 0.9993157537633931, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 12946, 'prepare_wall_seconds': 6313.072020970751, 'producer_wait_capacity_seconds': 0.01754158374387771, 'producer_wait_full_seconds': 4019.9246409742627, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.3210739297792315, '1': 6310.768577981158}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 25935, 'flush_seconds': 197.49987094232347, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,395 patches/s**; new independent GMP audits: 1,619.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
