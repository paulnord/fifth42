# Ada combined search

Updated: 2026-11-10T20:23:17.014166+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **5,892,207,488**.
New replicated logical patches: **4,872,192** in 19,032 chunks.
Combined verified selected patches, including parents: **2,142,207,488**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 5892207488]`.
Local cursor: 5,893,135,232; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 70.08470423502149, 'elapsed_seconds': 293.47750647197245, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7679899, 'mean_ready_depth': 0.3369471966776372, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 1386, 'prepare_wall_seconds': 293.02150154317496, 'producer_wait_capacity_seconds': 0.001379779598210007, 'producer_wait_full_seconds': 50.5467383377254, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 194.59108027332695, '1': 98.88642309367424}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 2768, 'flush_seconds': 19.716950164642185, 'pending_bytes': 18414, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,316 patches/s**; new independent GMP audits: 174.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
