# Boole combined search

Updated: 2026-11-12T11:09:05.897589+00:00

State: **running**. Run **boole-range-r3-20261111-26-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,671,155,968**.
New replicated logical patches: **7,155,968** in 27,953 chunks.
Combined verified selected patches, including parents: **7,155,968**.
Fresh interval: `[8664000000, 8728000000]`; replicated: `[8664000000, 8671155968]`.
Local cursor: 8,671,409,920; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15203163551632315, 'elapsed_seconds': 905.6304138241103, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680626, 'mean_ready_depth': 0.999069159865924, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1810, 'prepare_wall_seconds': 903.5877000557957, 'producer_wait_capacity_seconds': 0.00239515898283571, 'producer_wait_full_seconds': 586.4483447321691, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 0.842994145816192, '1': 904.787416688283}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 3623, 'flush_seconds': 27.052192639443092, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,175 patches/s**; new independent GMP audits: 227.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
