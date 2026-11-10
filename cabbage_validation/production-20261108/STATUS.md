# Cabbage combined search

Updated: 2026-11-10T22:59:58.467644+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,014,653,952**.
New replicated logical patches: **475,804,928** in 1,858,613 chunks.
Combined verified selected patches, including parents: **1,514,653,952**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2014653952]`.
Local cursor: 2,017,576,960; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1740.7692978773848, 'elapsed_seconds': 11299.773921522952, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.20836188875380307, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 116851, 'prepare_wall_seconds': 11299.31376680464, 'producer_wait_capacity_seconds': 0.08554019540315494, 'producer_wait_full_seconds': 313.122147625254, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 8945.33168245951, '1': 2354.4422367794905}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 233939, 'flush_seconds': 1350.7498310977244, 'pending_bytes': 20016, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **42,335 patches/s**; new independent GMP audits: 14,607.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
