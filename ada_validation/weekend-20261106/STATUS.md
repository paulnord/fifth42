# Ada combined search

Updated: 2026-11-10T10:07:04.753408+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,279,373,440**.
New replicated logical patches: **648,073,216** in 2,531,536 chunks.
Combined verified selected patches, including parents: **1,529,373,440**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5279373440]`.
Local cursor: 5,279,764,608; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 13058.007368300983, 'elapsed_seconds': 34343.001655536005, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6183697038501086, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2532532, 'prepare_wall_seconds': 34326.94495110714, 'producer_wait_capacity_seconds': 1.6077254335978068, 'producer_wait_full_seconds': 5332.7046882997965, 'ready': 0, 'ready_depth_seconds': {'0': 24963.41813099361, '1': 3208.93086041708, '2': 484.21708721248433, '3': 5686.435576071846}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 316566, 'flush_seconds': 2039.4213222822873, 'pending_bytes': 73665, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,878 patches/s**; new independent GMP audits: 19,786.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
