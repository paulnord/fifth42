# Cabbage combined search

Updated: 2026-11-10T13:51:06.663542+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,226,827,520**.
New replicated logical patches: **220,991,744** in 863,249 chunks.
Combined verified selected patches, including parents: **726,827,520**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1226827520]`.
Local cursor: 1,227,523,840; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4047.001355014683, 'elapsed_seconds': 9918.778295213997, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14733010869890156, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 865552, 'prepare_wall_seconds': 9915.735360720893, 'producer_wait_capacity_seconds': 0.5367723667877726, 'producer_wait_full_seconds': 177.61000402772333, 'ready': 0, 'ready_depth_seconds': {'0': 8872.609127294389, '1': 821.5239575756132, '2': 34.12490195746068, '3': 190.52030763454968}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 108258, 'flush_seconds': 603.550801968202, 'pending_bytes': 125615, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,325 patches/s**; new independent GMP audits: 6,763.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
