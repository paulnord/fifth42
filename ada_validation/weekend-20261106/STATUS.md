# Ada combined search

Updated: 2026-11-10T00:27:30.272278+00:00

State: **running**. Run **ada-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,623,489,664**.
New replicated logical patches: **58,533,888** in 228,648 chunks.
Combined verified selected patches, including parents: **873,489,664**.
Fresh interval: `[4564955776, 11250000001]`; replicated: `[4564955776, 4623489664]`.
Local cursor: 4,624,480,896; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1237.8952302889666, 'elapsed_seconds': 3036.7011445569806, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482129, 'mean_ready_depth': 0.5199459515864243, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 231886, 'prepare_wall_seconds': 3035.202063150704, 'producer_wait_capacity_seconds': 0.15218822797760367, 'producer_wait_full_seconds': 380.1194426700822, 'ready': 0, 'ready_depth_seconds': {'0': 2317.355741639447, '1': 271.3507528344635, '2': 36.41423405741807, '3': 411.58041511365445}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 28985, 'flush_seconds': 158.42204973346088, 'pending_bytes': 110467, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **120 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,548 patches/s**; new independent GMP audits: 1,812.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
