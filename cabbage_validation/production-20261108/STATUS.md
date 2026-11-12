# Cabbage combined search

Updated: 2026-11-12T21:12:11.713954+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-50**; gpu with 16 preparation workers.
Verified replicated cursor: **10,216,218,368**.
New replicated logical patches: **16,218,368** in 63,353 chunks.
Combined verified selected patches, including parents: **16,218,368**.
Fresh interval: `[10200000000, 10264000000]`; replicated: `[10200000000, 10216218368]`.
Local cursor: 10,216,267,520; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 201.98564555146731, 'elapsed_seconds': 1821.147822030005, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15356723, 'mean_ready_depth': 0.46748561334028127, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 3967, 'prepare_wall_seconds': 1820.9817866398953, 'producer_wait_capacity_seconds': 0.003426346811465919, 'producer_wait_full_seconds': 525.994456507382, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 969.7874116280582, '1': 851.3604065650143}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 7945, 'flush_seconds': 70.99393255799077, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,920 patches/s**; new independent GMP audits: 496.
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
