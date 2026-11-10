# Cabbage combined search

Updated: 2026-11-10T09:55:30.194417+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **921,368,320**.
New replicated logical patches: **421,368,320** in 1,645,970 chunks.
Combined verified selected patches, including parents: **421,368,320**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 921368320]`.
Local cursor: 923,168,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7699.291337444272, 'elapsed_seconds': 18958.33421368699, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.13926320110314797, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1652245, 'prepare_wall_seconds': 18952.63785821508, 'producer_wait_capacity_seconds': 1.0185069123399444, 'producer_wait_full_seconds': 330.745085614617, 'ready': 0, 'ready_depth_seconds': {'0': 17072.792119453137, '1': 1488.027087146591, '2': 40.37379603390582, '3': 357.1412103223265}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 206666, 'flush_seconds': 1116.0293242874905, 'pending_bytes': 69823, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,300 patches/s**; new independent GMP audits: 12,909.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
