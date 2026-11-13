# Cabbage combined search

Updated: 2026-11-13T00:41:05.774947+00:00

State: **running**. Run **cabbage-extended-overnight-sharing-claim33-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,142,941,440**.
New replicated logical patches: **30,941,440** in 120,865 chunks.
Combined verified selected patches, including parents: **30,941,440**.
Fresh interval: `[9112000000, 9176000000]`; replicated: `[9112000000, 9142941440]`.
Local cursor: 9,143,354,880; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 642.5948313531699, 'elapsed_seconds': 2741.9513098380994, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15359868, 'mean_ready_depth': 0.2901924455026949, 'outstanding': 1, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 7631, 'prepare_wall_seconds': 2741.7545014215866, 'producer_wait_capacity_seconds': 0.007234090473502874, 'producer_wait_full_seconds': 315.0667943897424, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1946.257752844831, '1': 795.6935560512356}, 'ready_limit': 1, 'reserved_bytes': 134217728}; buffer: {'flush_count': 15273, 'flush_seconds': 123.87571652315091, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,398 patches/s**; new independent GMP audits: 954.
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
