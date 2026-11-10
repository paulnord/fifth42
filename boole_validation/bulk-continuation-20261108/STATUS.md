# Boole combined search

Updated: 2026-11-10T01:46:20.265153+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,626,448,896**.
New replicated logical patches: **156,045,824** in 609,554 chunks.
Combined verified selected patches, including parents: **626,448,896**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3626448896]`.
Local cursor: 3,627,126,528; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1055.5330309878336, 'elapsed_seconds': 8671.73763888498, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9753226165138763, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 612162, 'prepare_wall_seconds': 8669.590347779915, 'producer_wait_capacity_seconds': 0.3846561526879668, 'producer_wait_full_seconds': 1629.338342746487, 'ready': 0, 'ready_depth_seconds': {'0': 4813.077296395379, '1': 1348.1515795605956, '2': 421.9360226285062, '3': 2088.5727396205184}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 76650, 'flush_seconds': 446.07381309958873, 'pending_bytes': 18226, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,069 patches/s**; new independent GMP audits: 4,783.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
