# Boole combined search

Updated: 2026-11-10T02:46:29.069382+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,690,356,480**.
New replicated logical patches: **219,953,408** in 859,193 chunks.
Combined verified selected patches, including parents: **690,356,480**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3690356480]`.
Local cursor: 3,691,635,712; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1479.5350358228316, 'elapsed_seconds': 12276.88864020002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.977955444641317, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 863861, 'prepare_wall_seconds': 12273.861702414753, 'producer_wait_capacity_seconds': 0.5431115458486602, 'producer_wait_full_seconds': 2319.6785552551155, 'ready': 0, 'ready_depth_seconds': {'0': 6805.384623002668, '1': 1904.2195253606187, '2': 599.8229084520135, '3': 2967.4615822246997}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 108160, 'flush_seconds': 631.86930374644, 'pending_bytes': 127577, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,011 patches/s**; new independent GMP audits: 6,749.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
