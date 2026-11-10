# Ada combined search

Updated: 2026-11-10T18:39:10.661222+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,812,476,032**.
New replicated logical patches: **1,181,175,808** in 4,613,968 chunks.
Combined verified selected patches, including parents: **2,062,476,032**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5812476032]`.
Local cursor: 5,813,012,608; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 23602.887021107657, 'elapsed_seconds': 65075.74993096903, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.7000204089744373, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4616040, 'prepare_wall_seconds': 65046.44390897575, 'producer_wait_capacity_seconds': 2.9349206753540784, 'producer_wait_full_seconds': 11739.062523614732, 'ready': 0, 'ready_depth_seconds': {'0': 45381.31884258898, '1': 6245.998695530521, '2': 1036.9427899878938, '3': 12411.489601829613}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 577099, 'flush_seconds': 4283.234773411066, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,159 patches/s**; new independent GMP audits: 36,063.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
