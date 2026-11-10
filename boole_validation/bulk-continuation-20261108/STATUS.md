# Boole combined search

Updated: 2026-11-10T08:06:02.265091+00:00

State: **running**. Run **boole-extra-20261109-b**; gpu with 16 preparation workers.
Verified replicated cursor: **383,990,784**.
New replicated logical patches: **83,990,784** in 328,089 chunks.
Combined verified selected patches, including parents: **83,990,784**.
Fresh interval: `[300000000, 500000000]`; replicated: `[300000000, 383990784]`.
Local cursor: 384,669,440; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 946.1154038560926, 'elapsed_seconds': 4517.793797150021, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 513930, 'mean_ready_depth': 0.5820819903987084, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 330317, 'prepare_wall_seconds': 4516.646798556962, 'producer_wait_capacity_seconds': 0.20280929713044316, 'producer_wait_full_seconds': 592.2909773326246, 'ready': 0, 'ready_depth_seconds': {'0': 3347.5151023289072, '1': 402.0898679860984, '2': 76.92994037503377, '3': 691.2588856399525}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 41363, 'flush_seconds': 215.32722502044635, 'pending_bytes': 17252, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,714 patches/s**; new independent GMP audits: 2,581.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
