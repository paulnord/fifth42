# Boole combined search

Updated: 2026-11-11T05:11:17.132006+00:00

State: **running**. Run **boole-preparation-20261110-12-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,777,337,088**.
New replicated logical patches: **9,337,088** in 36,473 chunks.
Combined verified selected patches, including parents: **9,337,088**.
Fresh interval: `[7768000000, 7832000000]`; replicated: `[7768000000, 7777337088]`.
Local cursor: 7,777,435,392; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15364431345369667, 'elapsed_seconds': 898.3867113920278, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680765, 'mean_ready_depth': 0.9988074267336963, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 2290, 'prepare_wall_seconds': 897.013232830679, 'producer_wait_capacity_seconds': 0.002959514851681888, 'producer_wait_full_seconds': 486.587161819567, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.0713889048201963, '1': 897.3153194172191}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 4578, 'flush_seconds': 31.932248454599176, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,428 patches/s**; new independent GMP audits: 287.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
