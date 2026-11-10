# Cabbage combined search

Updated: 2026-11-10T11:50:44.500873+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,066,322,176**.
New replicated logical patches: **60,486,400** in 236,275 chunks.
Combined verified selected patches, including parents: **566,322,176**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1066322176]`.
Local cursor: 1,066,716,928; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1094.824129659566, 'elapsed_seconds': 2696.950002723024, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14428154063860635, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 237374, 'prepare_wall_seconds': 2696.1135510457098, 'producer_wait_capacity_seconds': 0.14696951780933887, 'producer_wait_full_seconds': 46.4919812430162, 'ready': 0, 'ready_depth_seconds': {'0': 2414.6716688033775, '1': 225.2011288770591, '2': 7.312640573596582, '3': 49.764563797973096}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 29689, 'flush_seconds': 164.66297341877362, 'pending_bytes': 89599, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,479 patches/s**; new independent GMP audits: 1,855.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
