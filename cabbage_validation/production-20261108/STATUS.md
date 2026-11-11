# Cabbage combined search

Updated: 2026-11-11T17:45:24.917536+00:00

State: **running**. Run **cabbage-extended-r3-cap100-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,265,084,160**.
New replicated logical patches: **25,084,160** in 97,985 chunks.
Combined verified selected patches, including parents: **25,084,160**.
Fresh interval: `[9240000000, 9304000000]`; replicated: `[9240000000, 9265084160]`.
Local cursor: 9,265,262,336; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 819.5163788052741, 'elapsed_seconds': 2436.915317655017, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3843959, 'mean_ready_depth': 0.2595593695036624, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 24607, 'prepare_wall_seconds': 2436.7975152532454, 'producer_wait_capacity_seconds': 0.01758388290181756, 'producer_wait_full_seconds': 514.394111142843, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1804.391112056619, '1': 632.5242033843533}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 12326, 'flush_seconds': 124.57597977353726, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,338 patches/s**; new independent GMP audits: 769.
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
