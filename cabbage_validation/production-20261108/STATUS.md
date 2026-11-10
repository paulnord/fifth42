# Cabbage combined search

Updated: 2026-11-10T17:06:54.331208+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,483,763,712**.
New replicated logical patches: **477,927,936** in 1,866,906 chunks.
Combined verified selected patches, including parents: **983,763,712**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1483763712]`.
Local cursor: 1,484,970,752; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8849.504264008836, 'elapsed_seconds': 21670.113997180015, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.15045955361360405, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1871481, 'prepare_wall_seconds': 21663.496817701962, 'producer_wait_capacity_seconds': 1.1651076228008606, 'producer_wait_full_seconds': 394.6687219941523, 'ready': 0, 'ready_depth_seconds': {'0': 19371.587419028103, '1': 1766.548007762176, '2': 102.00803802674636, '3': 429.97053165198304}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 234068, 'flush_seconds': 1336.0017139794654, 'pending_bytes': 71798, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,102 patches/s**; new independent GMP audits: 14,621.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
