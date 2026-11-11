# Ada combined search

Updated: 2026-11-11T02:09:27.934481+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,278,650,752**.
New replicated logical patches: **391,315,456** in 1,528,576 chunks.
Combined verified selected patches, including parents: **2,528,650,752**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6278650752]`.
Local cursor: 6,279,136,128; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 4918.131937685888, 'elapsed_seconds': 21060.748572438024, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.352246504943633, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 95610, 'prepare_wall_seconds': 21057.543692910695, 'producer_wait_capacity_seconds': 0.09488475165562704, 'producer_wait_full_seconds': 4053.2808987515164, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 13642.173493164068, '1': 7418.575076137902}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 191216, 'flush_seconds': 1240.8901355449925, 'pending_bytes': 18419, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,594 patches/s**; new independent GMP audits: 11,952.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
