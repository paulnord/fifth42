# Boole combined search

Updated: 2026-11-10T02:01:26.021121+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,641,811,200**.
New replicated logical patches: **171,408,128** in 669,563 chunks.
Combined verified selected patches, including parents: **641,811,200**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3641811200]`.
Local cursor: 3,643,285,760; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1162.3633249152335, 'elapsed_seconds': 9576.00163827499, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.976205365121, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 675192, 'prepare_wall_seconds': 9573.633328707423, 'producer_wait_capacity_seconds': 0.4242640629527159, 'producer_wait_full_seconds': 1804.475523450994, 'ready': 0, 'ready_depth_seconds': {'0': 5312.199448420608, '1': 1489.1493821673212, '2': 464.9636270470219, '3': 2309.689179810055}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 84541, 'flush_seconds': 492.86156445764937, 'pending_bytes': 91122, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,048 patches/s**; new independent GMP audits: 5,275.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
