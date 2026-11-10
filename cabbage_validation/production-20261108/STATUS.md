# Cabbage combined search

Updated: 2026-11-10T02:16:43.449454+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,815,938,944**.
New replicated logical patches: **243,446,016** in 950,961 chunks.
Combined verified selected patches, including parents: **565,938,944**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2815938944]`.
Local cursor: 2,816,432,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3300.3199381409213, 'elapsed_seconds': 10640.322134155955, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.3372997470814296, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 952852, 'prepare_wall_seconds': 10636.999446062662, 'producer_wait_capacity_seconds': 0.615629973995965, 'producer_wait_full_seconds': 425.4925548808533, 'ready': 0, 'ready_depth_seconds': {'0': 8430.042501723685, '1': 1419.8287999244058, '2': 202.2033303893404, '3': 588.2475013375515}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 119172, 'flush_seconds': 693.2952088651364, 'pending_bytes': 72879, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,920 patches/s**; new independent GMP audits: 7,445.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
