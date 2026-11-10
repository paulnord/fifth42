# Ada combined search

Updated: 2026-11-10T13:07:35.978987+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,469,690,240**.
New replicated logical patches: **838,390,016** in 3,274,961 chunks.
Combined verified selected patches, including parents: **1,719,690,240**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5469690240]`.
Local cursor: 5,470,824,832; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 16421.045363624056, 'elapsed_seconds': 45175.05950042303, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6655927203588587, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3278929, 'prepare_wall_seconds': 45154.258970611205, 'producer_wait_capacity_seconds': 2.0834320033318363, 'producer_wait_full_seconds': 7434.518694820639, 'ready': 0, 'ready_depth_seconds': {'0': 31731.71545606258, '1': 4727.830696782621, '2': 806.1799917001044, '3': 7909.333355025679}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 409867, 'flush_seconds': 3295.3213162327884, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,581 patches/s**; new independent GMP audits: 25,617.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
