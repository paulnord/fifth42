# Ada combined search

Updated: 2026-11-10T13:22:39.363485+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,486,107,008**.
New replicated logical patches: **854,806,784** in 3,339,089 chunks.
Combined verified selected patches, including parents: **1,736,107,008**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5486107008]`.
Local cursor: 5,486,743,936; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 16754.44793298142, 'elapsed_seconds': 46078.18238681799, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6669438835130973, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3341082, 'prepare_wall_seconds': 46056.98952211486, 'producer_wait_capacity_seconds': 2.122774349350948, 'producer_wait_full_seconds': 7615.860168610408, 'ready': 0, 'ready_depth_seconds': {'0': 32363.268504346313, '1': 4798.228070865676, '2': 816.7235969885369, '3': 8099.962213815481}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 417636, 'flush_seconds': 3339.95213359216, 'pending_bytes': 18416, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,562 patches/s**; new independent GMP audits: 26,103.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
