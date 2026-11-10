# Cabbage combined search

Updated: 2026-11-10T16:51:47.635440+00:00

State: **running**. Run **cabbage-extended-rotation-20261110T110534Z**; gpu with 16 preparation workers.
Verified replicated cursor: **1,463,545,088**.
New replicated logical patches: **457,709,312** in 1,787,927 chunks.
Combined verified selected patches, including parents: **963,545,088**.
Fresh interval: `[1005835776, 2250000000]`; replicated: `[1005835776, 1463545088]`.
Local cursor: 1,465,248,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8477.127750700922, 'elapsed_seconds': 20758.210583776003, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514722, 'mean_ready_depth': 0.15052030062487454, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1793965, 'prepare_wall_seconds': 20751.873767834215, 'producer_wait_capacity_seconds': 1.1165226716548204, 'producer_wait_full_seconds': 379.3216879412648, 'ready': 0, 'ready_depth_seconds': {'0': 18555.577444625844, '1': 1693.5719101378345, '2': 96.22349738737103, '3': 412.8377308639465}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 224375, 'flush_seconds': 1280.555039617233, 'pending_bytes': 17937, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,117 patches/s**; new independent GMP audits: 14,016.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
