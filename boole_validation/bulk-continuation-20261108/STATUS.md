# Boole combined search

Updated: 2026-11-12T08:05:02.687355+00:00

State: **running**. Run **boole-range-r3-20261111-24-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,581,119,744**.
New replicated logical patches: **45,119,744** in 176,249 chunks.
Combined verified selected patches, including parents: **45,119,744**.
Fresh interval: `[8536000000, 8600000000]`; replicated: `[8536000000, 8581119744]`.
Local cursor: 8,581,562,112; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16409145831130445, 'elapsed_seconds': 5415.661543192924, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7685457, 'mean_ready_depth': 0.9993075786796787, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 11114, 'prepare_wall_seconds': 5413.632483934052, 'producer_wait_capacity_seconds': 0.015067929634824395, 'producer_wait_full_seconds': 3445.378502590349, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.749917366192676, '1': 5411.911623676773}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 22265, 'flush_seconds': 168.8106825397117, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,404 patches/s**; new independent GMP audits: 1,390.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
