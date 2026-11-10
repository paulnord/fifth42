# Cabbage combined search

Updated: 2026-11-10T06:24:56.518227+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **641,257,728**.
New replicated logical patches: **141,257,728** in 551,788 chunks.
Combined verified selected patches, including parents: **141,257,728**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 641257728]`.
Local cursor: 642,760,192; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2557.1194102765294, 'elapsed_seconds': 6334.027306962002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514000, 'mean_ready_depth': 0.14223038736095583, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 557647, 'prepare_wall_seconds': 6332.098367127706, 'producer_wait_capacity_seconds': 0.3431368217570707, 'producer_wait_full_seconds': 112.26295797718922, 'ready': 0, 'ready_depth_seconds': {'0': 5685.532141233212, '1': 516.3627967190114, '2': 11.868743918137625, '3': 120.26362428959692}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 69755, 'flush_seconds': 372.6996051592869, 'pending_bytes': 103700, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,507 patches/s**; new independent GMP audits: 4,357.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
