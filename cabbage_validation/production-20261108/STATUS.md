# Cabbage combined search

Updated: 2026-11-10T17:16:03.246192+00:00

State: **stopped**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,494,849,536**.
New replicated logical patches: **489,013,760** in 1,910,210 chunks.
Combined verified selected patches, including parents: **994,849,536**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1494849536]`.
Local cursor: 1,496,172,288; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 9060.330695974582, 'elapsed_seconds': 22187.029908547003, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514773, 'mean_ready_depth': 0.15032801703018034, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1915378, 'prepare_wall_seconds': 22180.129274120263, 'producer_wait_capacity_seconds': 1.1926031439215876, 'producer_wait_full_seconds': 402.9259946604725, 'ready': 0, 'ready_depth_seconds': {'0': 19834.846487312403, '1': 1808.0261844790657, '2': 105.1656780396006, '3': 438.99155646096915}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 239557, 'flush_seconds': 1367.8065752148395, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,094 patches/s**; new independent GMP audits: 14,964.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
