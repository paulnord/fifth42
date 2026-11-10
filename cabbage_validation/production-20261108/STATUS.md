# Cabbage combined search

Updated: 2026-11-10T04:17:26.554562+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,977,767,040**.
New replicated logical patches: **405,274,112** in 1,583,102 chunks.
Combined verified selected patches, including parents: **727,767,040**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2977767040]`.
Local cursor: 2,979,100,032; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5523.776477556326, 'elapsed_seconds': 17877.721231248986, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.34412377369846964, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1587757, 'prepare_wall_seconds': 17872.177329815808, 'producer_wait_capacity_seconds': 1.0275298703927547, 'producer_wait_full_seconds': 768.4766962782596, 'ready': 0, 'ready_depth_seconds': {'0': 14147.056656769942, '1': 2349.354912641109, '2': 341.1350000723032, '3': 1040.1746608136455}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 198576, 'flush_seconds': 1160.0854724802193, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,733 patches/s**; new independent GMP audits: 12,405.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
