# Ada combined search

Updated: 2026-11-11T02:39:39.941738+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,310,239,104**.
New replicated logical patches: **422,903,808** in 1,651,968 chunks.
Combined verified selected patches, including parents: **2,560,239,104**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6310239104]`.
Local cursor: 6,311,504,768; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 5322.946320507501, 'elapsed_seconds': 22874.444485343003, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.353889137865693, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 103523, 'prepare_wall_seconds': 22871.521465604543, 'producer_wait_capacity_seconds': 0.10272207210073248, 'producer_wait_full_seconds': 4449.085850303702, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 14779.427046046301, '1': 8095.01743807469}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 207042, 'flush_seconds': 1343.1365126474993, 'pending_bytes': 73663, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,537 patches/s**; new independent GMP audits: 12,941.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
