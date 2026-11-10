# Boole combined search

Updated: 2026-11-10T14:12:56.696421+00:00

State: **stopped**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,192,000,000**.
New replicated logical patches: **64,000,000** in 250,000 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7192000000]`.
Local cursor: 7,192,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 76.85300472495146, 'elapsed_seconds': 5268.798512601003, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482367, 'mean_ready_depth': 2.173559150907753, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 250000, 'prepare_wall_seconds': 5267.8084646483185, 'producer_wait_capacity_seconds': 0.16420977929374203, 'producer_wait_full_seconds': 2366.5102639156976, 'ready': 0, 'ready_depth_seconds': {'0': 726.8781153432792, '1': 783.8883838447509, '2': 605.939195920655, '3': 3152.092815222335}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 31296, 'flush_seconds': 175.48149128333898, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,146 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
