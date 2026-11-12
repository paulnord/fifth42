# Cabbage combined search

Updated: 2026-11-12T16:11:03.528064+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-47**; gpu with 16 preparation workers.
Verified replicated cursor: **10,058,471,168**.
New replicated logical patches: **50,471,168** in 197,153 chunks.
Combined verified selected patches, including parents: **50,471,168**.
Fresh interval: `[10008000000, 10072000000]`; replicated: `[10008000000, 10058471168]`.
Local cursor: 10,059,017,984; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 695.4903861868661, 'elapsed_seconds': 5430.891673703096, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357656, 'mean_ready_depth': 0.43638705952810036, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 12450, 'prepare_wall_seconds': 5429.714295957005, 'producer_wait_capacity_seconds': 0.010872152517549694, 'producer_wait_full_seconds': 1376.7712808646029, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3060.9208223341266, '1': 2369.9708481029375}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 24936, 'flush_seconds': 217.46426699927542, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,388 patches/s**; new independent GMP audits: 1,557.
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
