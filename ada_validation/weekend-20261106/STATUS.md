# Ada combined search

Updated: 2026-11-11T01:24:17.418490+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,230,061,952**.
New replicated logical patches: **342,726,656** in 1,338,776 chunks.
Combined verified selected patches, including parents: **2,480,061,952**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6230061952]`.
Local cursor: 6,230,313,856; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 4308.958504231239, 'elapsed_seconds': 18351.91673511901, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3497899198742161, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 83698, 'prepare_wall_seconds': 18349.062628406857, 'producer_wait_capacity_seconds': 0.08310387161327526, 'producer_wait_full_seconds': 3476.6298422081163, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 11932.601248028455, '1': 6419.315484315564}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 167392, 'flush_seconds': 1085.8984733908437, 'pending_bytes': 18414, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,680 patches/s**; new independent GMP audits: 10,463.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
