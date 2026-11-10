# Boole combined search

Updated: 2026-11-10T09:21:20.442872+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **467,330,048**.
New replicated logical patches: **167,330,048** in 653,633 chunks.
Combined verified selected patches, including parents: **167,330,048**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 467330048]`.
Local cursor: 468,847,104; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1891.9948256794014, 'elapsed_seconds': 9037.758997884986, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514009, 'mean_ready_depth': 0.5783945130571567, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 659293, 'prepare_wall_seconds': 9035.480974277074, 'producer_wait_capacity_seconds': 0.40389562904601917, 'producer_wait_full_seconds': 1174.7322488026111, 'ready': 0, 'ready_depth_seconds': {'0': 6709.465666318894, '1': 801.4174102884717, '2': 154.65495662175817, '3': 1372.2209637258784}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 82544, 'flush_seconds': 436.13939647754887, 'pending_bytes': 103510, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,673 patches/s**; new independent GMP audits: 5,151.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
