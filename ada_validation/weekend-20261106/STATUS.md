# Ada combined search

Updated: 2026-11-11T06:25:33.647819+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,546,033,536**.
New replicated logical patches: **658,698,240** in 2,573,040 chunks.
Combined verified selected patches, including parents: **2,796,033,536**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6546033536]`.
Local cursor: 6,547,282,816; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 8251.518787915353, 'elapsed_seconds': 36432.511231740005, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3660636181931466, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 161106, 'prepare_wall_seconds': 36427.38953899231, 'producer_wait_capacity_seconds': 0.15978196170181036, 'producer_wait_full_seconds': 7622.9999138579005, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 23095.8943472518, '1': 13336.616881353199}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 322208, 'flush_seconds': 2095.7900996835087, 'pending_bytes': 18413, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,112 patches/s**; new independent GMP audits: 20,139.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
