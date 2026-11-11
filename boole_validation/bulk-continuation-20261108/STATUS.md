# Boole combined search

Updated: 2026-11-11T13:46:26.208738+00:00

State: **running**. Run **boole-preparation-20261110-16-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,085,044,992**.
New replicated logical patches: **61,044,992** in 238,457 chunks.
Combined verified selected patches, including parents: **61,044,992**.
Fresh interval: `[8024000000, 8088000000]`; replicated: `[8024000000, 8085044992]`.
Local cursor: 8,085,667,584; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1618488814565353, 'elapsed_seconds': 6317.410872698005, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682388, 'mean_ready_depth': 0.9991661562055494, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 15037, 'prepare_wall_seconds': 6317.2545489405165, 'producer_wait_capacity_seconds': 0.019608081493061036, 'producer_wait_full_seconds': 3627.811439681158, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.267731403175276, '1': 6312.143138844811}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 30119, 'flush_seconds': 217.68909864430316, 'pending_bytes': 76711, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,748 patches/s**; new independent GMP audits: 1,880.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
