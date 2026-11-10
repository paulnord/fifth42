# Ada combined search

Updated: 2026-11-10T06:06:28.178905+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,012,846,720**.
New replicated logical patches: **381,546,496** in 1,490,416 chunks.
Combined verified selected patches, including parents: **1,262,846,720**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5012846720]`.
Local cursor: 5,014,063,232; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7820.089250573015, 'elapsed_seconds': 19909.166234427015, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5747157231110886, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1494788, 'prepare_wall_seconds': 19899.398807916907, 'producer_wait_capacity_seconds': 0.9476252916501835, 'producer_wait_full_seconds': 2866.1817968318937, 'ready': 3, 'ready_depth_seconds': {'0': 14846.579568987421, '1': 1753.5015463903546, '2': 238.64603184448788, '3': 3070.439086292754}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 186848, 'flush_seconds': 1034.9188587875105, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,221 patches/s**; new independent GMP audits: 11,679.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
