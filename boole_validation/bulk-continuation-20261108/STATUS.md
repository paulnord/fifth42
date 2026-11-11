# Boole combined search

Updated: 2026-11-11T01:23:57.329258+00:00

State: **running**. Run **boole-preparation-20261110-09-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,633,722,880**.
New replicated logical patches: **57,722,880** in 225,480 chunks.
Combined verified selected patches, including parents: **57,722,880**.
Fresh interval: `[7576000000, 7640000000]`; replicated: `[7576000000, 7633722880]`.
Local cursor: 7,634,470,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.171631223463919, 'elapsed_seconds': 5413.221767300973, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7696880, 'mean_ready_depth': 0.9987917199610614, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 14274, 'prepare_wall_seconds': 5411.857194755343, 'producer_wait_capacity_seconds': 0.019063218438532203, 'producer_wait_full_seconds': 2828.4136376123643, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 6.540685207757633, '1': 5406.681079493195}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 28591, 'flush_seconds': 196.21765847248025, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,799 patches/s**; new independent GMP audits: 1,785.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
