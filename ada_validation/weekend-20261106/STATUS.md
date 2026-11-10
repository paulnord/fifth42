# Ada combined search

Updated: 2026-11-10T18:08:58.761332+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,781,649,792**.
New replicated logical patches: **1,150,349,568** in 4,493,553 chunks.
Combined verified selected patches, including parents: **2,031,649,792**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5781649792]`.
Local cursor: 5,782,544,768; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 22956.32214860618, 'elapsed_seconds': 63261.606265623006, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6965744845999168, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4496871, 'prepare_wall_seconds': 63233.057431605004, 'producer_wait_capacity_seconds': 2.8592074937187135, 'producer_wait_full_seconds': 11319.003556737967, 'ready': 0, 'ready_depth_seconds': {'0': 44158.302803025814, '1': 6113.619858868711, '2': 1016.2498879989143, '3': 11973.433714857558}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 562189, 'flush_seconds': 4194.44628344482, 'pending_bytes': 110497, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,197 patches/s**; new independent GMP audits: 35,132.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
