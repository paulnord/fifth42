# Ada combined search

Updated: 2026-11-10T00:50:18.929870+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,648,278,144**.
New replicated logical patches: **16,977,920** in 66,320 chunks.
Combined verified selected patches, including parents: **898,278,144**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4648278144]`.
Local cursor: 4,649,441,408; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 404.8995930554811, 'elapsed_seconds': 942.1893726330018, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481991, 'mean_ready_depth': 0.5148876471402781, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 70660, 'prepare_wall_seconds': 941.5040037709405, 'producer_wait_capacity_seconds': 0.04523236339446157, 'producer_wait_full_seconds': 118.80179915757617, 'ready': 3, 'ready_depth_seconds': {'0': 724.703583133989, '1': 78.33576078288024, '2': 10.664175052777864, '3': 128.4858527823817}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 8832, 'flush_seconds': 46.94741411844734, 'pending_bytes': 18415, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,198 patches/s**; new independent GMP audits: 553.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
