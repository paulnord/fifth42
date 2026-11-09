# Ada combined search

Updated: 2026-11-09T22:41:49.319805+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,543,161,728**.
New replicated logical patches: **108,888,064** in 425,344 chunks.
Combined verified selected patches, including parents: **793,161,728**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4543161728]`.
Local cursor: 4,543,487,360; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2185.4620380974375, 'elapsed_seconds': 5453.986439044995, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.5010879024069044, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 425945, 'prepare_wall_seconds': 5452.5486550597125, 'producer_wait_capacity_seconds': 0.247904357383959, 'producer_wait_full_seconds': 644.3514018569258, 'ready': 0, 'ready_depth_seconds': {'0': 4190.491575383814, '1': 495.484166141483, '2': 66.58963170775678, '3': 701.4210649799206}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 53243, 'flush_seconds': 296.77061217301525, 'pending_bytes': 18408, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,861 patches/s**; new independent GMP audits: 3,328.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
