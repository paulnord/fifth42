# Cabbage combined search

Updated: 2026-11-10T21:14:39.252649+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,750,585,856**.
New replicated logical patches: **211,736,832** in 827,097 chunks.
Combined verified selected patches, including parents: **1,250,585,856**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1750585856]`.
Local cursor: 1,751,544,832; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 857.4187269798131, 'elapsed_seconds': 4974.7560956479865, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3838766, 'mean_ready_depth': 0.15486788628381443, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 51842, 'prepare_wall_seconds': 4974.523874889186, 'producer_wait_capacity_seconds': 0.03793648350983858, 'producer_wait_full_seconds': 147.9467271087342, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4204.326132634422, '1': 770.429961310525}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 103792, 'flush_seconds': 607.4337043148698, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,635 patches/s**; new independent GMP audits: 6,481.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
