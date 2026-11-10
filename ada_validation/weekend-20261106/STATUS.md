# Ada combined search

Updated: 2026-11-10T19:24:30.879677+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,858,195,840**.
New replicated logical patches: **1,226,895,616** in 4,792,561 chunks.
Combined verified selected patches, including parents: **2,108,195,840**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5858195840]`.
Local cursor: 5,858,562,432; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 24562.47304199438, 'elapsed_seconds': 67787.02086168004, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.7052816595512774, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4793348, 'prepare_wall_seconds': 67756.11631604389, 'producer_wait_capacity_seconds': 3.0477331184083596, 'producer_wait_full_seconds': 12376.601500439516, 'ready': 3, 'ready_depth_seconds': {'0': 47199.031710941694, '1': 6443.396171878383, '2': 1068.2325357893715, '3': 13076.360441968543}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 599278, 'flush_seconds': 4416.755063300487, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,102 patches/s**; new independent GMP audits: 37,449.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
