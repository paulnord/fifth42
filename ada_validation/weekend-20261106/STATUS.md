# Ada combined search

Updated: 2026-11-11T10:56:17.311407+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,815,847,552**.
New replicated logical patches: **928,512,256** in 3,627,001 chunks.
Combined verified selected patches, including parents: **3,065,847,552**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6815847552]`.
Local cursor: 6,816,056,448; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 11503.541082970158, 'elapsed_seconds': 52678.73139004997, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.38074245360274267, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 226736, 'prepare_wall_seconds': 52672.34318374918, 'producer_wait_capacity_seconds': 0.22480404836824164, 'producer_wait_full_seconds': 11938.58026690752, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 32621.701945687528, '1': 20057.029442127445}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 453471, 'flush_seconds': 2947.0178804488387, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,630 patches/s**; new independent GMP audits: 28,342.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
