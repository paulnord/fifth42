# Ada combined search

Updated: 2026-11-10T19:09:22.559288+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,842,112,896**.
New replicated logical patches: **1,210,812,672** in 4,729,737 chunks.
Combined verified selected patches, including parents: **2,092,112,896**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5842112896]`.
Local cursor: 5,843,406,976; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 24241.330411891453, 'elapsed_seconds': 66879.09182470001, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.7035227291133624, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4734212, 'prepare_wall_seconds': 66848.58041983674, 'producer_wait_capacity_seconds': 3.0100941210985184, 'producer_wait_full_seconds': 12161.673196348827, 'ready': 3, 'ready_depth_seconds': {'0': 46590.89260160574, '1': 6377.949995777046, '2': 1057.7364737366443, '3': 12852.512752628594}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 591881, 'flush_seconds': 4371.908938940382, 'pending_bytes': 18422, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,122 patches/s**; new independent GMP audits: 36,987.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
