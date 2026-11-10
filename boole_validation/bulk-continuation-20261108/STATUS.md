# Boole combined search

Updated: 2026-11-10T11:47:41.596760+00:00

State: **running**. Run **boole-delegated-20261109-01**; gpu with 16 preparation workers.
Verified replicated cursor: **7,086,110,208**.
New replicated logical patches: **22,110,208** in 86,368 chunks.
Combined verified selected patches, including parents: **22,110,208**.
Fresh interval: `[7064000000, 7128000000]`; replicated: `[7064000000, 7086110208]`.
Local cursor: 7,086,366,464; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 30.156372228462715, 'elapsed_seconds': 1802.3124046919984, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482111, 'mean_ready_depth': 2.112986422482165, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 86916, 'prepare_wall_seconds': 1801.111718665692, 'producer_wait_capacity_seconds': 0.05500801996095106, 'producer_wait_full_seconds': 794.6218208976206, 'ready': 3, 'ready_depth_seconds': {'0': 276.65764040109934, '1': 284.4791541908053, '2': 199.7443412457942, '3': 1041.4312678343267}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 10882, 'flush_seconds': 61.230899332556874, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,343 patches/s**; new independent GMP audits: 680.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
