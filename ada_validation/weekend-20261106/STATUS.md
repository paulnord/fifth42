# Ada combined search

Updated: 2026-11-10T02:50:40.251894+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,788,988,032**.
New replicated logical patches: **157,687,808** in 615,968 chunks.
Combined verified selected patches, including parents: **1,038,988,032**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4788988032]`.
Local cursor: 4,790,306,944; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3248.3989404534805, 'elapsed_seconds': 8159.29781151202, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5496871956880283, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 620623, 'prepare_wall_seconds': 8155.36117515876, 'producer_wait_capacity_seconds': 0.39322220388567075, 'producer_wait_full_seconds': 1101.5180171117536, 'ready': 1, 'ready_depth_seconds': {'0': 6143.565621492278, '1': 732.0407314939657, '2': 98.05357217480196, '3': 1185.6378856499796}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 77577, 'flush_seconds': 427.05890100623947, 'pending_bytes': 110489, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,472 patches/s**; new independent GMP audits: 4,849.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
