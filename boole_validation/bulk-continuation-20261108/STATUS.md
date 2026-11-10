# Boole combined search

Updated: 2026-11-10T04:00:33.412656+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **115,666,688**.
New replicated logical patches: **15,666,688** in 61,198 chunks.
Combined verified selected patches, including parents: **15,666,688**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 115666688]`.
Local cursor: 116,474,624; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 206.40868929505814, 'elapsed_seconds': 894.2010214700131, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 545834, 'mean_ready_depth': 0.5381704148330356, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 63559, 'prepare_wall_seconds': 893.9763364464743, 'producer_wait_capacity_seconds': 0.038954963616561145, 'producer_wait_full_seconds': 108.83803804143099, 'ready': 0, 'ready_depth_seconds': {'0': 681.1174828067305, '1': 71.22633506526472, '2': 15.565409090660978, '3': 126.2917938073515}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 7960, 'flush_seconds': 43.21635418885853, 'pending_bytes': 85437, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,177 patches/s**; new independent GMP audits: 497.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
