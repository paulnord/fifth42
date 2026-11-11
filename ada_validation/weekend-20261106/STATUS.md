# Ada combined search

Updated: 2026-11-11T05:55:26.441408+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,516,353,920**.
New replicated logical patches: **629,018,624** in 2,457,104 chunks.
Combined verified selected patches, including parents: **2,766,353,920**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6516353920]`.
Local cursor: 6,516,515,712; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 7869.2192519172095, 'elapsed_seconds': 34629.06967213401, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3644492146260516, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 153610, 'prepare_wall_seconds': 34624.18602846237, 'producer_wait_capacity_seconds': 0.15231914265314117, 'producer_wait_full_seconds': 7179.688019324967, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 22008.53242444893, '1': 12620.537245240062}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 307216, 'flush_seconds': 1997.004593634687, 'pending_bytes': 18422, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,169 patches/s**; new independent GMP audits: 19,202.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
