# Boole combined search

Updated: 2026-11-11T02:18:22.003881+00:00

State: **running**. Run **boole-preparation-20261110-10-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **7,668,979,456**.
New replicated logical patches: **28,979,456** in 113,201 chunks.
Combined verified selected patches, including parents: **28,979,456**.
Fresh interval: `[7640000000, 7704000000]`; replicated: `[7640000000, 7668979456]`.
Local cursor: 7,669,061,376; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15410727699054405, 'elapsed_seconds': 2719.8187088309787, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680489, 'mean_ready_depth': 0.9989524703609082, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7077, 'prepare_wall_seconds': 2714.300272016728, 'producer_wait_capacity_seconds': 0.009184799797367305, 'producer_wait_full_seconds': 1436.3810417290078, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.8490877604926936, '1': 2716.969618120522}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 14174, 'flush_seconds': 91.9790312301484, 'pending_bytes': 19025, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,654 patches/s**; new independent GMP audits: 885.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
