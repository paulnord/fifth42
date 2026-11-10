# Ada combined search

Updated: 2026-11-10T10:37:09.246661+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,311,125,632**.
New replicated logical patches: **679,825,408** in 2,655,568 chunks.
Combined verified selected patches, including parents: **1,561,125,632**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5311125632]`.
Local cursor: 5,311,813,760; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 13548.29705976398, 'elapsed_seconds': 36149.582822935015, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6307156507282725, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2657878, 'prepare_wall_seconds': 36132.73332006612, 'producer_wait_capacity_seconds': 1.6874887729645707, 'producer_wait_full_seconds': 5672.696966706833, 'ready': 0, 'ready_depth_seconds': {'0': 26004.888677227776, '1': 3536.99682580214, '2': 559.9811298414133, '3': 6047.716189412691}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 332234, 'flush_seconds': 2323.479293858283, 'pending_bytes': 110510, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,822 patches/s**; new independent GMP audits: 20,765.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
