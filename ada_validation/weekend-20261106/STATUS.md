# Ada combined search

Updated: 2026-11-10T15:07:57.669002+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,596,078,464**.
New replicated logical patches: **964,778,240** in 3,768,665 chunks.
Combined verified selected patches, including parents: **1,846,078,464**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5596078464]`.
Local cursor: 5,597,137,280; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 19057.43746374268, 'elapsed_seconds': 52396.08788573602, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6770063438896651, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3772292, 'prepare_wall_seconds': 52371.75519105967, 'producer_wait_capacity_seconds': 2.397042576398235, 'producer_wait_full_seconds': 8919.382800876221, 'ready': 3, 'ready_depth_seconds': {'0': 36747.84809930477, '1': 5291.007961016905, '2': 890.2195406701649, '3': 9467.01228376216}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 471557, 'flush_seconds': 3655.8264071441954, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,431 patches/s**; new independent GMP audits: 29,472.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
