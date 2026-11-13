# Cabbage combined search

Updated: 2026-11-13T01:26:08.557012+00:00

State: **running**. Run **cabbage-extended-overnight-sharing-claim33-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,173,794,304**.
New replicated logical patches: **61,794,304** in 241,384 chunks.
Combined verified selected patches, including parents: **61,794,304**.
Fresh interval: `[9112000000, 9176000000]`; replicated: `[9112000000, 9173794304]`.
Local cursor: 9,173,888,512; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1276.5579476903658, 'elapsed_seconds': 5452.920404318022, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15360737, 'mean_ready_depth': 0.29244380117461743, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 15108, 'prepare_wall_seconds': 5452.734630541992, 'producer_wait_capacity_seconds': 0.014299712143838406, 'producer_wait_full_seconds': 638.1417688181391, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3858.2476311816135, '1': 1594.6727705413941}, 'ready_limit': 1, 'reserved_bytes': 268435456}; buffer: {'flush_count': 30237, 'flush_seconds': 247.0493713344913, 'pending_bytes': 105910, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,347 patches/s**; new independent GMP audits: 1,889.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
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
