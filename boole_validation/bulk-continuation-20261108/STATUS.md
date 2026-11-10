# Boole combined search

Updated: 2026-11-10T04:15:32.303654+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **131,447,808**.
New replicated logical patches: **31,447,808** in 122,843 chunks.
Combined verified selected patches, including parents: **31,447,808**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 131447808]`.
Local cursor: 132,763,904; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 416.558152309095, 'elapsed_seconds': 1792.5852189239813, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 546271, 'mean_ready_depth': 0.5328802089949249, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 127542, 'prepare_wall_seconds': 1792.138365419989, 'producer_wait_capacity_seconds': 0.07801658764947206, 'producer_wait_full_seconds': 215.8384434534819, 'ready': 0, 'ready_depth_seconds': {'0': 1369.408841009019, '1': 141.58097267412813, '2': 31.13400004518917, '3': 250.46140444563935}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 15970, 'flush_seconds': 86.44939947209787, 'pending_bytes': 85429, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,205 patches/s**; new independent GMP audits: 997.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
