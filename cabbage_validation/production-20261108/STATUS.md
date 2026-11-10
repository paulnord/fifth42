# Cabbage combined search

Updated: 2026-11-10T12:35:55.451433+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,125,891,840**.
New replicated logical patches: **120,056,064** in 468,969 chunks.
Combined verified selected patches, including parents: **625,891,840**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1125891840]`.
Local cursor: 1,127,296,768; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2200.74888189364, 'elapsed_seconds': 5411.061057400017, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514645, 'mean_ready_depth': 0.14716935945103296, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 474293, 'prepare_wall_seconds': 5409.399766476185, 'producer_wait_capacity_seconds': 0.2940249039675109, 'producer_wait_full_seconds': 96.75950178800849, 'ready': 0, 'ready_depth_seconds': {'0': 4839.430889937154, '1': 450.7762326892116, '2': 16.99564456922235, '3': 103.8582893134444}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 59323, 'flush_seconds': 331.7904011553619, 'pending_bytes': 71779, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,413 patches/s**; new independent GMP audits: 3,706.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
