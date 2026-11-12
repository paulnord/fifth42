# Boole combined search

Updated: 2026-11-12T07:19:54.410280+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,558,247,680**.
New replicated logical patches: **22,247,680** in 86,905 chunks.
Combined verified selected patches, including parents: **22,247,680**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8558247680]`.
Local cursor: 8,558,825,216; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15660227905027568, 'elapsed_seconds': 2708.5004159179516, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685457, 'mean_ready_depth': 0.9992524853343286, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 5570, 'prepare_wall_seconds': 2706.5179627295583, 'producer_wait_capacity_seconds': 0.0075286360224708915, 'producer_wait_full_seconds': 1721.3221375981811, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.0246405828511342, '1': 2706.475772135076}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 11162, 'flush_seconds': 83.85495677997824, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,419 patches/s**; new independent GMP audits: 697.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
