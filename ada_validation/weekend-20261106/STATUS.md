# Ada combined search

Updated: 2026-11-10T01:05:22.266315+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,667,070,592**.
New replicated logical patches: **35,770,368** in 139,728 chunks.
Combined verified selected patches, including parents: **917,070,592**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4667070592]`.
Local cursor: 4,667,207,808; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 760.4620462566381, 'elapsed_seconds': 1843.9349618480192, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481991, 'mean_ready_depth': 0.5282035349351389, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 139938, 'prepare_wall_seconds': 1843.0373197599547, 'producer_wait_capacity_seconds': 0.08893880905816332, 'producer_wait_full_seconds': 237.4573611948872, 'ready': 0, 'ready_depth_seconds': {'0': 1404.3069776796037, '1': 161.6001918843249, '2': 21.7106018649647, '3': 256.31718980812}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 17492, 'flush_seconds': 94.8392228842713, 'pending_bytes': 36836, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,428 patches/s**; new independent GMP audits: 1,094.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
