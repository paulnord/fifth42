# Boole combined search

Updated: 2026-11-12T13:21:55.218229+00:00

State: **running**. Run **boole-range-r3-20261111-27-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,734,945,024**.
New replicated logical patches: **6,945,024** in 27,129 chunks.
Combined verified selected patches, including parents: **6,945,024**.
Fresh interval: `[8728000000, 8792000000]`; replicated: `[8728000000, 8734945024]`.
Local cursor: 8,735,207,168; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14659052668139338, 'elapsed_seconds': 891.5249028250109, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681667, 'mean_ready_depth': 0.9990942606253768, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1738, 'prepare_wall_seconds': 889.4308413362596, 'producer_wait_capacity_seconds': 0.0023555466905236244, 'producer_wait_full_seconds': 584.9122000532225, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.8074862179346383, '1': 890.7174136170652}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3478, 'flush_seconds': 26.38829825585708, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,973 patches/s**; new independent GMP audits: 218.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
