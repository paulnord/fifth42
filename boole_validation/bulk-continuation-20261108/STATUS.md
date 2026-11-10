# Boole combined search

Updated: 2026-11-10T06:50:52.759610+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **300,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 300002048]`.
Local cursor: 300,284,672; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2.069495103089139, 'elapsed_seconds': 9.111840942001436, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513015, 'mean_ready_depth': 0.3023860622051839, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 761, 'prepare_wall_seconds': 9.101926181814633, 'producer_wait_capacity_seconds': 0.00046728801680728793, 'producer_wait_full_seconds': 0.19343680184101686, 'ready': 0, 'ready_depth_seconds': {'0': 7.519941884034779, '1': 0.904381757020019, '2': 0.21163674804847687, '3': 0.4758794829249382}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 95, 'flush_seconds': 0.469452764140442, 'pending_bytes': 17254, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,451 patches/s**; new independent GMP audits: 6.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
