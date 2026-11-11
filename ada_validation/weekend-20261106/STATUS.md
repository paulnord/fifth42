# Ada combined search

Updated: 2026-11-11T04:40:13.428329+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,438,552,448**.
New replicated logical patches: **551,217,152** in 2,153,192 chunks.
Combined verified selected patches, including parents: **2,688,552,448**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6438552448]`.
Local cursor: 6,438,722,432; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 6904.929508809233, 'elapsed_seconds': 30111.939781275985, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3603420164499436, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 134599, 'prepare_wall_seconds': 30108.161468423496, 'producer_wait_capacity_seconds': 0.13352569803828374, 'producer_wait_full_seconds': 6093.032580585335, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 19261.342679969734, '1': 10850.597100004263}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 269196, 'flush_seconds': 1747.6313231172971, 'pending_bytes': 18422, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,309 patches/s**; new independent GMP audits: 16,825.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
