# Boole combined search

Updated: 2026-11-10T07:05:58.314129+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **316,249,344**.
New replicated logical patches: **16,249,344** in 63,474 chunks.
Combined verified selected patches, including parents: **16,249,344**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 316249344]`.
Local cursor: 317,443,840; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 193.9767121548648, 'elapsed_seconds': 912.4334480250254, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513842, 'mean_ready_depth': 0.551212139143775, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 67606, 'prepare_wall_seconds': 912.1941627755295, 'producer_wait_capacity_seconds': 0.04151945770718157, 'producer_wait_full_seconds': 112.14456623111619, 'ready': 0, 'ready_depth_seconds': {'0': 685.8184551301529, '1': 81.49768740643049, '2': 13.905209209537134, '3': 131.2120956289}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 8464, 'flush_seconds': 43.926555240526795, 'pending_bytes': 34506, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,949 patches/s**; new independent GMP audits: 529.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
