# Ada combined search

Updated: 2026-11-11T08:40:55.543855+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,682,450,816**.
New replicated logical patches: **795,115,520** in 3,105,920 chunks.
Combined verified selected patches, including parents: **2,932,450,816**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6682450816]`.
Local cursor: 6,683,532,160; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 9908.579498203355, 'elapsed_seconds': 44556.91196071799, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3735082226770479, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 194378, 'prepare_wall_seconds': 44550.815358474385, 'producer_wait_capacity_seconds': 0.19272996234940365, 'producer_wait_full_seconds': 9716.090672462713, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 27914.538962946506, '1': 16642.372994425474}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 388752, 'flush_seconds': 2526.885128090973, 'pending_bytes': 18414, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,868 patches/s**; new independent GMP audits: 24,298.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
