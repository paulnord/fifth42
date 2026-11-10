# Boole combined search

Updated: 2026-11-10T03:31:48.070487+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,738,324,480**.
New replicated logical patches: **267,921,408** in 1,046,568 chunks.
Combined verified selected patches, including parents: **738,324,480**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3738324480]`.
Local cursor: 3,739,848,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1792.6036014074925, 'elapsed_seconds': 14990.711018360977, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482295, 'mean_ready_depth': 0.9811214506565312, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1051965, 'prepare_wall_seconds': 14987.024569135276, 'producer_wait_capacity_seconds': 0.6616273896652274, 'producer_wait_full_seconds': 2847.4272794029675, 'ready': 3, 'ready_depth_seconds': {'0': 8295.143587716157, '1': 2321.4561946426984, '2': 736.081759392051, '3': 3638.0294757601223}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 131706, 'flush_seconds': 771.8384317182354, 'pending_bytes': 36467, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **17,963 patches/s**; new independent GMP audits: 8,219.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
