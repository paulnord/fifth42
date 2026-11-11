# Boole combined search

Updated: 2026-11-11T15:21:18.523957+00:00

State: **running**. Run **boole-preparation-20261110-17-r1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,139,994,880**.
New replicated logical patches: **51,994,880** in 203,105 chunks.
Combined verified selected patches, including parents: **51,994,880**.
Fresh interval: `[8088000000, 8152000000]`; replicated: `[8088000000, 8139994880]`.
Local cursor: 8,140,080,896; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16652837430592626, 'elapsed_seconds': 5414.301291044045, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683578, 'mean_ready_depth': 0.9992258301841361, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 12698, 'prepare_wall_seconds': 5412.631866022886, 'producer_wait_capacity_seconds': 0.01666636817390099, 'producer_wait_full_seconds': 3147.9627936512697, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4.191586183500476, '1': 5410.109702410526}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 25429, 'flush_seconds': 184.83509214228252, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,604 patches/s**; new independent GMP audits: 1,588.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
