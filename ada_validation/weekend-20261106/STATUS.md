# Ada combined search

Updated: 2026-11-10T22:53:51.863505+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,063,983,488**.
New replicated logical patches: **176,648,192** in 690,032 chunks.
Combined verified selected patches, including parents: **2,313,983,488**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6063983488]`.
Local cursor: 6,064,511,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2229.1612930221017, 'elapsed_seconds': 9331.641013876011, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681797, 'mean_ready_depth': 0.3416343846974706, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 43243, 'prepare_wall_seconds': 9330.422876395285, 'producer_wait_capacity_seconds': 0.042943570646457374, 'producer_wait_full_seconds': 1676.823387370503, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 6143.63157617976, '1': 3188.009435993212}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 86482, 'flush_seconds': 560.6689343227772, 'pending_bytes': 18413, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,980 patches/s**; new independent GMP audits: 5,406.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
