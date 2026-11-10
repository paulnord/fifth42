# Boole combined search

Updated: 2026-11-10T01:16:18.644889+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,593,699,072**.
New replicated logical patches: **123,296,000** in 481,625 chunks.
Combined verified selected patches, including parents: **593,699,072**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3593699072]`.
Local cursor: 3,594,854,656; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 840.8212855604943, 'elapsed_seconds': 6864.604668118001, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9702874615120086, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 485662, 'prepare_wall_seconds': 6862.909359747486, 'producer_wait_capacity_seconds': 0.30483602435560897, 'producer_wait_full_seconds': 1281.3567574669723, 'ready': 1, 'ready_depth_seconds': {'0': 3820.001866213337, '1': 1071.119822124252, '2': 330.928921593877, '3': 1642.5540574665647}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 60811, 'flush_seconds': 352.51258280395996, 'pending_bytes': 36438, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,108 patches/s**; new independent GMP audits: 3,795.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
