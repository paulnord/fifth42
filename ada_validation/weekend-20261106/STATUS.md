# Ada combined search

Updated: 2026-11-09T22:26:46.019940+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,525,206,912**.
New replicated logical patches: **90,933,248** in 355,208 chunks.
Combined verified selected patches, including parents: **775,206,912**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4525206912]`.
Local cursor: 4,525,550,976; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1825.6859549374785, 'elapsed_seconds': 4551.733860057022, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.4990845833337337, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 355972, 'prepare_wall_seconds': 4550.329789553303, 'producer_wait_capacity_seconds': 0.20723481656750664, 'producer_wait_full_seconds': 534.7776857204735, 'ready': 3, 'ready_depth_seconds': {'0': 3501.034803579678, '1': 412.3488347886596, '2': 55.699300155974925, '3': 582.6509206306655}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 44496, 'flush_seconds': 245.89208410063293, 'pending_bytes': 18404, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,862 patches/s**; new independent GMP audits: 2,782.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
