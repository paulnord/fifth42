# Cabbage combined search

Updated: 2026-11-12T19:24:16.612290+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-49**; gpu with 16 preparation workers.
Verified replicated cursor: **10,160,246,528**.
New replicated logical patches: **24,246,528** in 94,713 chunks.
Combined verified selected patches, including parents: **24,246,528**.
Fresh interval: `[10136000000, 10200000000]`; replicated: `[10136000000, 10160246528]`.
Local cursor: 10,160,557,824; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 326.2348791726399, 'elapsed_seconds': 2710.1440957359737, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358069, 'mean_ready_depth': 0.4540185517192549, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 5994, 'prepare_wall_seconds': 2708.971001678612, 'producer_wait_capacity_seconds': 0.005150206037797034, 'producer_wait_full_seconds': 754.180739643285, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1479.6883946224116, '1': 1230.4556972965365}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 11996, 'flush_seconds': 103.5669441006612, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,055 patches/s**; new independent GMP audits: 750.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
