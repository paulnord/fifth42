# Boole combined search

Updated: 2026-11-10T09:06:15.501883+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **451,515,648**.
New replicated logical patches: **151,515,648** in 591,858 chunks.
Combined verified selected patches, including parents: **151,515,648**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 451515648]`.
Local cursor: 451,959,040; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1702.4974361530622, 'elapsed_seconds': 8133.593751833017, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514009, 'mean_ready_depth': 0.5800935720147903, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 593392, 'prepare_wall_seconds': 8131.54603593878, 'producer_wait_capacity_seconds': 0.3635720907477662, 'producer_wait_full_seconds': 1062.0023150293273, 'ready': 0, 'ready_depth_seconds': {'0': 6034.236787775764, '1': 720.7056212828029, '2': 138.4141944780713, '3': 1240.2371475263499}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 74293, 'flush_seconds': 391.53591276408406, 'pending_bytes': 34508, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,675 patches/s**; new independent GMP audits: 4,636.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
