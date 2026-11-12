# Boole combined search

Updated: 2026-11-12T13:37:02.584575+00:00

State: **running**. Run **boole-range-r3-20261111-27-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,741,906,176**.
New replicated logical patches: **13,906,176** in 54,321 chunks.
Combined verified selected patches, including parents: **13,906,176**.
Fresh interval: `[8728000000, 8792000000]`; replicated: `[8728000000, 8741906176]`.
Local cursor: 8,742,448,896; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1489177520852536, 'elapsed_seconds': 1801.2168973030057, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681667, 'mean_ready_depth': 0.9992566569300081, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3514, 'prepare_wall_seconds': 1799.1018528583227, 'producer_wait_capacity_seconds': 0.0047454602317884564, 'producer_wait_full_seconds': 1182.1128476453014, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.3389196981443092, '1': 1799.877975204843}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7036, 'flush_seconds': 53.29276232642587, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,985 patches/s**; new independent GMP audits: 440.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
