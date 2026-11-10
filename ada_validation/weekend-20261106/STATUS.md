# Ada combined search

Updated: 2026-11-10T13:52:45.842486+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,517,435,008**.
New replicated logical patches: **886,134,784** in 3,461,464 chunks.
Combined verified selected patches, including parents: **1,767,435,008**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5517435008]`.
Local cursor: 5,518,499,968; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 17416.941649976827, 'elapsed_seconds': 47884.40940826002, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6696582425521104, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3465112, 'prepare_wall_seconds': 47862.427857108705, 'producer_wait_capacity_seconds': 2.201492152933497, 'producer_wait_full_seconds': 7981.6835237536, 'ready': 0, 'ready_depth_seconds': {'0': 33623.50483173266, '1': 4939.472021455702, '2': 837.5802339235088, '3': 8483.852320226142}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 433142, 'flush_seconds': 3429.9148784148856, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,525 patches/s**; new independent GMP audits: 27,072.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
