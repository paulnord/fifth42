# Ada combined search

Updated: 2026-11-11T05:25:24.428524+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,485,379,968**.
New replicated logical patches: **598,044,672** in 2,336,112 chunks.
Combined verified selected patches, including parents: **2,735,379,968**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6485379968]`.
Local cursor: 6,485,580,672; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 7484.746310077724, 'elapsed_seconds': 32824.41576278402, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.36288234979380846, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 146045, 'prepare_wall_seconds': 32820.314129410894, 'producer_wait_capacity_seconds': 0.1447912564035505, 'producer_wait_full_seconds': 6741.511962371063, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 20913.01463794202, '1': 11911.40112260799}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 292088, 'flush_seconds': 1898.8510259022005, 'pending_bytes': 18416, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,224 patches/s**; new independent GMP audits: 18,256.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
