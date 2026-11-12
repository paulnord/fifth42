# Boole combined search

Updated: 2026-11-12T11:54:13.356678+00:00

State: **running**. Run **boole-range-r3-20261111-26-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,693,096,192**.
New replicated logical patches: **29,096,192** in 113,657 chunks.
Combined verified selected patches, including parents: **29,096,192**.
Fresh interval: `[8664000000, 8728000000]`; replicated: `[8664000000, 8693096192]`.
Local cursor: 8,693,456,640; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1593765631550923, 'elapsed_seconds': 3607.5526536740363, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7684363, 'mean_ready_depth': 0.9993214528738918, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7178, 'prepare_wall_seconds': 3605.4160732718883, 'producer_wait_capacity_seconds': 0.009536818135529757, 'producer_wait_full_seconds': 2343.742660276126, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.4478913854109123, '1': 3605.1047591886017}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 14383, 'flush_seconds': 110.87546883674804, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,147 patches/s**; new independent GMP audits: 898.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
