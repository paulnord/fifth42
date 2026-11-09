# Ada combined search

Updated: 2026-11-09T21:26:37.734117+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,452,146,560**.
New replicated logical patches: **17,872,896** in 69,816 chunks.
Combined verified selected patches, including parents: **702,146,560**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4452146560]`.
Local cursor: 4,453,389,696; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 379.8273015677114, 'elapsed_seconds': 941.7648970049922, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.49039646648279456, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 73963, 'prepare_wall_seconds': 941.5117553453892, 'producer_wait_capacity_seconds': 0.04299648222513497, 'producer_wait_full_seconds': 107.97200279380195, 'ready': 0, 'ready_depth_seconds': {'0': 726.8130804715911, '1': 85.81940897757886, '2': 11.37845161324367, '3': 117.75395518157165}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 9245, 'flush_seconds': 50.85036932077492, 'pending_bytes': 55207, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,357 patches/s**; new independent GMP audits: 578.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
