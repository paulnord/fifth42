# Boole combined search

Updated: 2026-11-11T03:29:05.243563+00:00

State: **running**. Run **boole-preparation-20261110-11-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,712,823,040**.
New replicated logical patches: **8,823,040** in 34,465 chunks.
Combined verified selected patches, including parents: **8,823,040**.
Fresh interval: `[7704000000, 7768000000]`; replicated: `[7704000000, 7712823040]`.
Local cursor: 7,713,588,992; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1496162589173764, 'elapsed_seconds': 904.0202151169651, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7679978, 'mean_ready_depth': 0.998803987107764, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2336, 'prepare_wall_seconds': 899.2784096598043, 'producer_wait_capacity_seconds': 0.00310672604246065, 'producer_wait_full_seconds': 480.26363500824664, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.0812166921678, '1': 902.9389952848433}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4679, 'flush_seconds': 32.16649959323695, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,573 patches/s**; new independent GMP audits: 292.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
