# Ada combined search

Updated: 2026-11-11T15:35:20.450230+00:00

State: **running**. Run **ada-preparation-rotation-01-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,857,038,976**.
New replicated logical patches: **14,385,152** in 56,192 chunks.
Combined verified selected patches, including parents: **3,107,038,976**.
Fresh interval: `[6842653824, 7000000000]`; replicated: `[6842653824, 6857038976]`.
Local cursor: 6,857,718,912; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 175.25618115003454, 'elapsed_seconds': 914.8562480420223, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680188, 'mean_ready_depth': 0.437009896595375, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3650, 'prepare_wall_seconds': 914.0191938425414, 'producer_wait_capacity_seconds': 0.0034155252506025136, 'producer_wait_full_seconds': 271.56480186997214, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 515.0550109605538, '1': 399.8012343564769}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7296, 'flush_seconds': 45.94255125976633, 'pending_bytes': 18427, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **16,333 patches/s**; new independent GMP audits: 457.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
