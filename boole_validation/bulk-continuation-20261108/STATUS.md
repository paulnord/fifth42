# Boole combined search

Updated: 2026-11-10T03:01:32.346782+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,706,300,416**.
New replicated logical patches: **235,897,344** in 921,474 chunks.
Combined verified selected patches, including parents: **706,300,416**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3706300416]`.
Local cursor: 3,707,703,040; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1584.4528862087755, 'elapsed_seconds': 13184.208359874028, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9791916511914504, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 926947, 'prepare_wall_seconds': 13180.970166824758, 'producer_wait_capacity_seconds': 0.5828047991963103, 'producer_wait_full_seconds': 2495.954530313087, 'ready': 1, 'ready_depth_seconds': {'0': 7302.583358955686, '1': 2044.6183124490199, '2': 645.7716221697628, '3': 3191.2350655895425}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 116058, 'flush_seconds': 678.790527596313, 'pending_bytes': 18228, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **17,997 patches/s**; new independent GMP audits: 7,242.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
