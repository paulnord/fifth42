# Boole combined search

Updated: 2026-11-10T00:46:14.621516+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,561,177,344**.
New replicated logical patches: **90,774,272** in 354,587 chunks.
Combined verified selected patches, including parents: **561,177,344**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3561177344]`.
Local cursor: 3,562,283,264; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 625.2519961806829, 'elapsed_seconds': 5064.082573371998, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9679059570939641, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 358696, 'prepare_wall_seconds': 5062.821151412674, 'producer_wait_capacity_seconds': 0.2253151792101562, 'producer_wait_full_seconds': 940.7789226616733, 'ready': 0, 'ready_depth_seconds': {'0': 2822.4244212800986, '1': 789.9554739150335, '2': 243.50781612319406, '3': 1208.1948612736887}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 44910, 'flush_seconds': 259.7876758907805, 'pending_bytes': 91092, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,128 patches/s**; new independent GMP audits: 2,803.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
