# Cabbage combined search

Updated: 2026-11-12T20:24:36.596106+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-49**; gpu with 16 preparation workers.
Verified replicated cursor: **10,192,807,680**.
New replicated logical patches: **56,807,680** in 221,905 chunks.
Combined verified selected patches, including parents: **56,807,680**.
Fresh interval: `[10136000000, 10200000000]`; replicated: `[10136000000, 10192807680]`.
Local cursor: 10,193,176,320; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 746.1672432799824, 'elapsed_seconds': 6325.571612918982, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358069, 'mean_ready_depth': 0.45725363692854126, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 13946, 'prepare_wall_seconds': 6324.304839554359, 'producer_wait_capacity_seconds': 0.01190350973047316, 'producer_wait_full_seconds': 1774.4117773706093, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3433.180983683793, '1': 2892.3906256591436}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 27920, 'flush_seconds': 247.4509467431344, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,029 patches/s**; new independent GMP audits: 1,744.
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
