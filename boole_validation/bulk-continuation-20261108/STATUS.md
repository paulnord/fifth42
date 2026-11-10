# Boole combined search

Updated: 2026-11-10T07:51:04.274394+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **367,294,976**.
New replicated logical patches: **67,294,976** in 262,871 chunks.
Combined verified selected patches, including parents: **67,294,976**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 367294976]`.
Local cursor: 367,959,552; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 759.6911681152997, 'elapsed_seconds': 3622.957660468004, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513863, 'mean_ready_depth': 0.5803960797773975, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 265312, 'prepare_wall_seconds': 3622.0378799777245, 'producer_wait_capacity_seconds': 0.16312407521763816, 'producer_wait_full_seconds': 472.65203565818956, 'ready': 0, 'ready_depth_seconds': {'0': 2687.138470346341, '1': 321.2309099881095, '2': 62.24532498366898, '3': 552.3429544598912}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 33226, 'flush_seconds': 172.04497500037542, 'pending_bytes': 86269, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,742 patches/s**; new independent GMP audits: 2,073.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
