# Ada combined search

Updated: 2026-11-10T06:21:31.511815+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,030,688,896**.
New replicated logical patches: **399,388,672** in 1,560,112 chunks.
Combined verified selected patches, including parents: **1,280,688,896**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5030688896]`.
Local cursor: 5,031,016,576; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8169.616510165972, 'elapsed_seconds': 20813.81252710003, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5765574938865596, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1561138, 'prepare_wall_seconds': 20803.90658359474, 'producer_wait_capacity_seconds': 0.9896628250135109, 'producer_wait_full_seconds': 3011.0225307319197, 'ready': 0, 'ready_depth_seconds': {'0': 15510.8317413787, '1': 1829.6729044143576, '2': 249.23695722967386, '3': 3224.0709233252564}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 195142, 'flush_seconds': 1080.8322400528705, 'pending_bytes': 36841, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,201 patches/s**; new independent GMP audits: 12,197.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
