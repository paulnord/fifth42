# Cabbage combined search

Updated: 2026-11-10T09:25:26.636587+00:00

State: **running**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **881,780,992**.
New replicated logical patches: **381,780,992** in 1,491,332 chunks.
Combined verified selected patches, including parents: **381,780,992**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 881780992]`.
Local cursor: 883,499,776; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6969.1847213222645, 'elapsed_seconds': 17163.857232893002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.13959044828694514, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1498005, 'prepare_wall_seconds': 17158.696918440924, 'producer_wait_capacity_seconds': 0.9205822080839425, 'producer_wait_full_seconds': 300.4128606262384, 'ready': 0, 'ready_depth_seconds': {'0': 15452.326519382652, '1': 1351.4903637954849, '2': 35.70088521129219, '3': 324.3394637515303}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 187374, 'flush_seconds': 1009.9495419119485, 'pending_bytes': 122179, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,331 patches/s**; new independent GMP audits: 11,704.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
