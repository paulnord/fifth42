# Boole combined search

Updated: 2026-11-11T20:45:03.588612+00:00

State: **running**. Run **boole-range-r3-20261111-19-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,224,280,320**.
New replicated logical patches: **8,280,320** in 32,345 chunks.
Combined verified selected patches, including parents: **8,280,320**.
Fresh interval: `[8216000000, 8280000000]`; replicated: `[8216000000, 8224280320]`.
Local cursor: 8,224,550,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.14233235421124846, 'elapsed_seconds': 914.2204819939798, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681764, 'mean_ready_depth': 0.9990062045299098, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2084, 'prepare_wall_seconds': 914.1834542739089, 'producer_wait_capacity_seconds': 0.0027301095542497933, 'producer_wait_full_seconds': 545.0393783946056, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.9085461936774664, '1': 913.3119338203105}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4173, 'flush_seconds': 29.763648585649207, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,325 patches/s**; new independent GMP audits: 261.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
