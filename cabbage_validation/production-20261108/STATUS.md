# Cabbage combined search

Updated: 2026-11-10T05:54:51.409063+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **600,507,904**.
New replicated logical patches: **100,507,904** in 392,609 chunks.
Combined verified selected patches, including parents: **100,507,904**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 600507904]`.
Local cursor: 602,198,272; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1823.4496590244235, 'elapsed_seconds': 4520.108832980972, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513941, 'mean_ready_depth': 0.1414840689167938, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 398550, 'prepare_wall_seconds': 4518.728519584867, 'producer_wait_capacity_seconds': 0.24572041898500174, 'producer_wait_full_seconds': 79.5299082690035, 'ready': 0, 'ready_depth_seconds': {'0': 4058.178398233431, '1': 369.2904803180718, '2': 7.686950033588801, '3': 84.9530030838796}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 49852, 'flush_seconds': 265.87908091570716, 'pending_bytes': 103590, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,528 patches/s**; new independent GMP audits: 3,114.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
