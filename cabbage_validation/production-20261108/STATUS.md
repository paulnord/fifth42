# Cabbage combined search

Updated: 2026-11-10T15:21:22.595898+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,346,515,712**.
New replicated logical patches: **340,679,936** in 1,330,781 chunks.
Combined verified selected patches, including parents: **846,515,712**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1346515712]`.
Local cursor: 1,346,842,368; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6266.441270120908, 'elapsed_seconds': 15338.681706144009, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.14758118746858834, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1331947, 'prepare_wall_seconds': 15333.984234058822, 'producer_wait_capacity_seconds': 0.8273891448625363, 'producer_wait_full_seconds': 273.21029918367276, 'ready': 0, 'ready_depth_seconds': {'0': 13723.429094594147, '1': 1261.4346479487722, '2': 59.1876764636836, '3': 294.63028650643537}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 166593, 'flush_seconds': 936.3609021053417, 'pending_bytes': 35875, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,221 patches/s**; new independent GMP audits: 10,406.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
