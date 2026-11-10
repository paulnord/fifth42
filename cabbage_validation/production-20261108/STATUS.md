# Cabbage combined search

Updated: 2026-11-10T03:32:09.344278+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,917,892,480**.
New replicated logical patches: **345,399,552** in 1,349,217 chunks.
Combined verified selected patches, including parents: **667,892,480**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2917892480]`.
Local cursor: 2,918,363,520; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4688.916946681333, 'elapsed_seconds': 15161.485219206952, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.34136744118872386, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1350580, 'prepare_wall_seconds': 15156.775138609926, 'producer_wait_capacity_seconds': 0.8735060354811139, 'producer_wait_full_seconds': 632.3967459796695, 'ready': 0, 'ready_depth_seconds': {'0': 12001.894538459659, '1': 2006.8368169397581, '2': 289.46099217800656, '3': 863.2928708685213}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 168912, 'flush_seconds': 986.1061736984993, 'pending_bytes': 54674, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,801 patches/s**; new independent GMP audits: 10,552.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
