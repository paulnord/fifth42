# Ada combined search

Updated: 2026-11-10T07:51:46.228085+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,130,629,248**.
New replicated logical patches: **499,329,024** in 1,950,504 chunks.
Combined verified selected patches, including parents: **1,380,629,248**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5130629248]`.
Local cursor: 5,131,872,384; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 10246.854292773409, 'elapsed_seconds': 26225.78281607601, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5875157009849299, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1954933, 'prepare_wall_seconds': 26213.384961283824, 'producer_wait_capacity_seconds': 1.240257250785362, 'producer_wait_full_seconds': 3899.204918591713, 'ready': 0, 'ready_depth_seconds': {'0': 19463.827752235404, '1': 2282.458798161708, '2': 312.8884176100255, '3': 4166.60784722789}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 244366, 'flush_seconds': 1355.2049324557302, 'pending_bytes': 92098, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,083 patches/s**; new independent GMP audits: 15,273.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
