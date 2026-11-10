# Cabbage combined search

Updated: 2026-11-10T14:06:12.687220+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,246,572,288**.
New replicated logical patches: **240,736,512** in 940,377 chunks.
Combined verified selected patches, including parents: **746,572,288**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1246572288]`.
Local cursor: 1,247,592,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4416.799436675559, 'elapsed_seconds': 10820.708194028994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.14772893804010276, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 943519, 'prepare_wall_seconds': 10817.389355353604, 'producer_wait_capacity_seconds': 0.5850997404777445, 'producer_wait_full_seconds': 194.61137686058646, 'ready': 0, 'ready_depth_seconds': {'0': 9678.681309821666, '1': 894.50240590272, '2': 38.544107587775216, '3': 208.98036975582363}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 118012, 'flush_seconds': 659.3570690058405, 'pending_bytes': 107661, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,309 patches/s**; new independent GMP audits: 7,372.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
