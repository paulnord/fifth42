# Cabbage combined search

Updated: 2026-11-09T20:50:10.562044+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,393,391,744**.
New replicated logical patches: **26,050,048** in 101,758 chunks.
Combined verified selected patches, including parents: **143,391,744**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2393391744]`.
Local cursor: 2,393,866,880; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 365.9311226555146, 'elapsed_seconds': 1138.6038874899969, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482045, 'mean_ready_depth': 0.3018978100242621, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 103066, 'prepare_wall_seconds': 1138.2392714977032, 'producer_wait_capacity_seconds': 0.06494135985849425, 'producer_wait_full_seconds': 34.30433323129546, 'ready': 1, 'ready_depth_seconds': {'0': 915.0797303554718, '1': 153.35960405191872, '2': 20.111239725432824, '3': 50.05331220518565}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 12889, 'flush_seconds': 71.9888337320881, 'pending_bytes': 54664, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,108 patches/s**; new independent GMP audits: 806.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
