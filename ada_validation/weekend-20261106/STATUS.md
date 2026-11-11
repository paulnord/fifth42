# Ada combined search

Updated: 2026-11-11T04:55:17.121791+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,453,132,160**.
New replicated logical patches: **565,796,864** in 2,210,144 chunks.
Combined verified selected patches, including parents: **2,703,132,160**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6453132160]`.
Local cursor: 6,454,385,536; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 7099.772132686514, 'elapsed_seconds': 31012.844191426004, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3611334240650066, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 138415, 'prepare_wall_seconds': 31008.955608724325, 'producer_wait_capacity_seconds': 0.1372804611455649, 'producer_wait_full_seconds': 6305.289121003065, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 19813.069577038754, '1': 11199.774612844223}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 276828, 'flush_seconds': 1796.745658456639, 'pending_bytes': 18418, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,281 patches/s**; new independent GMP audits: 17,302.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
