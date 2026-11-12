# Cabbage combined search

Updated: 2026-11-12T00:00:55.099738+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-38**; gpu with 16 preparation workers.
Verified replicated cursor: **9,489,833,728**.
New replicated logical patches: **57,833,728** in 225,913 chunks.
Combined verified selected patches, including parents: **57,833,728**.
Fresh interval: `[9432000000, 9496000000]`; replicated: `[9432000000, 9489833728]`.
Local cursor: 9,490,484,992; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1121.5822250079364, 'elapsed_seconds': 5406.092654677108, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358283, 'mean_ready_depth': 0.334211981155225, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 14266, 'prepare_wall_seconds': 5405.340769544244, 'producer_wait_capacity_seconds': 0.01273393223527819, 'producer_wait_full_seconds': 878.923455642187, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3599.311715503689, '1': 1806.7809364283457}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 28554, 'flush_seconds': 229.64047954184934, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,807 patches/s**; new independent GMP audits: 1,784.
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
