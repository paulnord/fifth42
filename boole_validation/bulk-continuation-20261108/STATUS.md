# Boole combined search

Updated: 2026-11-12T08:42:28.425268+00:00

State: **stopped**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,600,000,000**.
New replicated logical patches: **64,000,000** in 250,000 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8600000000]`.
Local cursor: 8,600,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 0.1701184429693967, 'elapsed_seconds': 7629.201131674927, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685457, 'mean_ready_depth': 0.9990459332606011, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15625, 'prepare_wall_seconds': 7626.847326618736, 'producer_wait_capacity_seconds': 0.021172644919715822, 'producer_wait_full_seconds': 4858.450301469187, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7.278764407965355, '1': 7621.922364627011}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 31304, 'flush_seconds': 239.085194589803, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,388 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
