# Ada combined search

Updated: 2026-11-11T02:54:43.495913+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,327,278,464**.
New replicated logical patches: **439,943,168** in 1,718,528 chunks.
Combined verified selected patches, including parents: **2,577,278,464**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6327278464]`.
Local cursor: 6,327,569,280; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 5521.9013788069715, 'elapsed_seconds': 23776.979351358023, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.35468326592499727, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 107440, 'prepare_wall_seconds': 23773.888488121273, 'producer_wait_capacity_seconds': 0.10663112136535347, 'producer_wait_full_seconds': 4647.585009369359, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 15343.682658703125, '1': 8433.296690170886}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 214879, 'flush_seconds': 1395.0495383754023, 'pending_bytes': 55250, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,508 patches/s**; new independent GMP audits: 13,430.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
