# Cabbage combined search

Updated: 2026-11-10T22:44:58.199893+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **1,977,616,896**.
New replicated logical patches: **438,767,872** in 1,713,937 chunks.
Combined verified selected patches, including parents: **1,477,616,896**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 1977616896]`.
Local cursor: 1,980,282,112; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1628.5244236476137, 'elapsed_seconds': 10395.371021733969, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.2006199545588995, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 107698, 'prepare_wall_seconds': 10394.9053997132, 'producer_wait_capacity_seconds': 0.07874427642673254, 'producer_wait_full_seconds': 284.2134197150008, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 8309.852158027817, '1': 2085.5188620031695}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 215614, 'flush_seconds': 1248.0253591215587, 'pending_bytes': 49992, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,412 patches/s**; new independent GMP audits: 13,463.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
