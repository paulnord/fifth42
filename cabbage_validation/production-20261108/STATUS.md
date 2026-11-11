# Cabbage combined search

Updated: 2026-11-11T00:30:10.573547+00:00

State: **running**. Run **cabbage-extended-upgrade-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **2,236,051,968**.
New replicated logical patches: **697,202,944** in 2,723,449 chunks.
Combined verified selected patches, including parents: **1,736,051,968**.
Fresh interval: `[1538849024, 2250000000]`; replicated: `[1538849024, 2236051968]`.
Local cursor: 2,239,160,832; physical tasks group up to 8 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 2; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2372.789410593512, 'elapsed_seconds': 16708.31841238495, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3841026, 'mean_ready_depth': 0.2444389383484581, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 170909, 'prepare_wall_seconds': 16707.636108739534, 'producer_wait_capacity_seconds': 0.12676073552574962, 'producer_wait_full_seconds': 548.2185894927243, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 12624.154796510586, '1': 4084.163614311372}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 342180, 'flush_seconds': 1944.6934500888456, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **41,884 patches/s**; new independent GMP audits: 21,364.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
