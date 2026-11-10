# Ada combined search

Updated: 2026-11-10T19:39:39.131728+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,872,920,960**.
New replicated logical patches: **1,241,620,736** in 4,850,081 chunks.
Combined verified selected patches, including parents: **2,122,920,960**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5872920960]`.
Local cursor: 5,873,699,200; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 24886.16228940821, 'elapsed_seconds': 68704.34901526402, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.7070950354395951, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4853112, 'prepare_wall_seconds': 68673.53878114134, 'producer_wait_capacity_seconds': 3.08573099313071, 'producer_wait_full_seconds': 12596.221217002661, 'ready': 0, 'ready_depth_seconds': {'0': 47811.00350693165, '1': 6510.42989208881, '2': 1078.6726368239615, '3': 13304.242978688562}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 606751, 'flush_seconds': 4461.745900274487, 'pending_bytes': 128924, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,083 patches/s**; new independent GMP audits: 37,915.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
