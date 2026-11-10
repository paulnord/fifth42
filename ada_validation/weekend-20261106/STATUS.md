# Ada combined search

Updated: 2026-11-10T05:36:21.578417+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,978,804,864**.
New replicated logical patches: **347,504,640** in 1,357,440 chunks.
Combined verified selected patches, including parents: **1,228,804,864**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4978804864]`.
Local cursor: 4,980,037,760; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7120.23710973555, 'elapsed_seconds': 18097.937116620014, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5709046391497646, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1361540, 'prepare_wall_seconds': 18089.009439045447, 'producer_wait_capacity_seconds': 0.8629626226611435, 'producer_wait_full_seconds': 2580.8425589591498, 'ready': 3, 'ready_depth_seconds': {'0': 13516.53239143436, '1': 1597.40390791971, '2': 217.21009791246615, '3': 2766.7907183914795}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 170192, 'flush_seconds': 941.9931482964312, 'pending_bytes': 18422, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,259 patches/s**; new independent GMP audits: 10,638.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
