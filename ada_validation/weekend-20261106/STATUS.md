# Ada combined search

Updated: 2026-11-10T14:52:54.250570+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,581,115,776**.
New replicated logical patches: **949,815,552** in 3,710,217 chunks.
Combined verified selected patches, including parents: **1,831,115,776**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5581115776]`.
Local cursor: 5,581,457,536; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 18733.078287593496, 'elapsed_seconds': 51496.50337511202, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6754257531175162, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3711311, 'prepare_wall_seconds': 51472.96380149748, 'producer_wait_capacity_seconds': 2.358305369503796, 'producer_wait_full_seconds': 8729.003688484489, 'ready': 1, 'ready_depth_seconds': {'0': 36128.653106555634, '1': 5220.899990970618, '2': 879.6862464182195, '3': 9267.264030415565}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 463927, 'flush_seconds': 3610.3711164991255, 'pending_bytes': 110511, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,450 patches/s**; new independent GMP audits: 28,995.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
