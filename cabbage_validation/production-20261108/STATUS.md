# Cabbage combined search

Updated: 2026-11-11T00:15:09.037303+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,200,102,656**.
New replicated logical patches: **661,253,632** in 2,583,022 chunks.
Combined verified selected patches, including parents: **1,700,102,656**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2200102656]`.
Local cursor: 2,202,552,320; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2268.725984540244, 'elapsed_seconds': 15802.64889179595, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.23950508054089473, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 161938, 'prepare_wall_seconds': 15801.936162924918, 'producer_wait_capacity_seconds': 0.11983207275625318, 'producer_wait_full_seconds': 500.6515743447235, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 12017.834193071874, '1': 3784.8146955890697}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 324216, 'flush_seconds': 1849.2845489374595, 'pending_bytes': 20016, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **41,959 patches/s**; new independent GMP audits: 20,243.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
